#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tese_network_chapters.py
========================
Gera, para CADA capítulo, uma rede de co-ocorrência + comunidades de Louvain
*próprias do capítulo* — no MESMO formato do `netdata` da capa
(`tese_network.py`) — para que o grafo interativo do site possa alternar entre
a tese inteira e cada capítulo.

Diferença em relação a `tese_network.py`: aqui o Louvain roda separadamente
por capítulo (comunidades específicas de cada um), em vez de uma única vez
sobre a tese concatenada.

Saídas:
  - rede_textual/<slug>/netdata_<slug>.json   (um por capítulo, para inspeção)
  - injeta um <script id="netdata-chapters"> em index.html com {slug: payload}

Uso:
    python3 rede_textual/tese_network_chapters.py --source-root /caminho/tese --inject index.html
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import tese_network as TN
from rede_textual_capitulo import (extract_tokens, build_graph, compute_npmi,
                             annotate_npmi, prune_graph, compute_metrics,
                             detect_topics, label_topic, collect_surface_forms)

THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parent

# capítulos com rede própria (a Apresentação e as Considerações finais ficam
# de fora: a leitura por capítulo cobre o corpo argumentativo da tese).
CHAPTER_SLUGS = ["cap1", "cap2", "cap3", "cap4"]
SLUG_TO_TEX = {cid: fname for fname, _label, cid in TN.CHAPTERS}
SLUG_TO_LABEL = {cid: label for fname, label, cid in TN.CHAPTERS}

# parâmetros do recorte por capítulo (corpora menores que a tese inteira)
TOP_N = 180
MIN_EDGE = 2
EDGES_PER_NODE = 14
CORE = 60


def build_chapter_payload(slug: str, source_root: Path) -> dict | None:
    fname = SLUG_TO_TEX[slug]
    src = source_root / fname
    if not src.exists():
        print(f"[chap] aviso: {fname} não encontrado, pulando {slug}.")
        return None

    raw = src.read_text(encoding="utf-8")
    surface: dict = {}
    collect_surface_forms(raw, surface)
    tokens = extract_tokens(raw)

    G_full = build_graph(tokens, window=4)
    npmi = compute_npmi(tokens, window=4)
    annotate_npmi(G_full, npmi)

    G = prune_graph(G_full, top_n=TOP_N, min_edge_weight=MIN_EDGE)
    annotate_npmi(G, npmi)

    deg, btw, pr = compute_metrics(G)
    comms = detect_topics(G)
    comms, forced_names = TN.carve_bibliometric_territory(comms)

    # densidade controlada: mantém as K arestas mais fortes por termo (união)
    keep_edges: set = set()
    for n in G.nodes():
        nbr = sorted(G[n].items(), key=lambda kv: kv[1].get("weight", 0), reverse=True)
        for m, _ in nbr[:EDGES_PER_NODE]:
            keep_edges.add((n, m) if n < m else (m, n))
    drop = [(u, v) for u, v in G.edges()
            if (u, v) not in keep_edges and (v, u) not in keep_edges]
    G.remove_edges_from(drop)

    comm_of: dict = {}
    for i, c in enumerate(comms):
        for n in c:
            comm_of[n] = i

    core = set(sorted(G.nodes(), key=lambda n: pr.get(n, 0), reverse=True)[:CORE])

    # trechos reais do capítulo por termo: restringe collect_passages a este
    # capítulo monkeypatchando TN.CHAPTERS temporariamente.
    npmi_neighbors: dict = {}
    for n in G.nodes():
        nbr = sorted(G[n].items(),
                     key=lambda kv: (kv[1].get("npmi", 0), kv[1].get("weight", 0)),
                     reverse=True)
        npmi_neighbors[n] = {m: float(d.get("npmi", 0)) for m, d in nbr[:12]}
    saved_chapters = TN.CHAPTERS
    TN.CHAPTERS = [(fname, SLUG_TO_LABEL[slug], slug)]
    try:
        passages = TN.collect_passages(set(G.nodes()), source_root,
                                       npmi_neighbors, per_term=4)
    finally:
        TN.CHAPTERS = saved_chapters

    def display_label(node_id: str) -> str:
        c = surface.get(node_id)
        return c.most_common(1)[0][0] if c else node_id

    nodes = []
    for n in G.nodes():
        nodes.append({
            "id": n,
            "label": display_label(n),
            "community": comm_of.get(n, 0),
            "freq": int(G.nodes[n].get("freq", 0)),
            "degree": round(float(deg.get(n, 0)), 1),
            "pagerank": round(float(pr.get(n, 0)), 5),
            "betweenness": round(float(btw.get(n, 0)), 4),
            "chapters": [slug],
            "core": n in core,
            "passages": passages.get(n, []),
        })

    edges = []
    for u, v, d in G.edges(data=True):
        edges.append({"s": u, "t": v,
                      "w": round(float(d.get("weight", 0)), 1),
                      "npmi": round(float(d.get("npmi", 0)), 3)})

    communities = []
    used_names: set = set()
    for i, c in enumerate(comms):
        communities.append({
            "id": i,
            "size": len(c),
            "name": forced_names.get(i) or TN.name_territory(c, used_names),
            "label": [display_label(t) for t in label_topic(c, deg, k=5)],
            "color": TN.PALETTE[i % len(TN.PALETTE)],
        })

    payload = {
        "generated_from": f"{SLUG_TO_LABEL[slug]} (rede do capítulo)",
        "slug": slug,
        "params": {"window": 4, "top_n": TOP_N, "min_edge": MIN_EDGE,
                   "edges_per_node": EDGES_PER_NODE, "core": CORE},
        # lista completa de capítulos (para os rótulos do painel resolverem)
        "chapters": [{"id": cid, "label": label} for _f, label, cid in TN.CHAPTERS],
        "communities": communities,
        "nodes": nodes,
        "edges": edges,
    }
    big = sum(1 for cc in communities if cc["size"] >= 3)
    print(f"[chap] {slug}: {len(nodes)} nós, {len(edges)} arestas, "
          f"{len(communities)} comunidades ({big} ≥3), núcleo={len(core)}")
    for cc in communities:
        if cc["size"] >= 3:
            print(f"        T{cc['id']} ({cc['size']}): "
                  f"{cc['name'] or ' · '.join(cc['label'])}")
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", type=Path, default=Path("/tmp/tese"))
    ap.add_argument("--inject", type=Path, default=None,
                    help="reinjeta {slug: payload} no <script id=netdata-chapters>")
    ap.add_argument("--only", type=str, default="",
                    help="lista separada por vírgula (cap1,cap2,...)")
    args = ap.parse_args()

    slugs = [s.strip() for s in args.only.split(",") if s.strip()] or CHAPTER_SLUGS
    bundle: dict = {}
    for slug in slugs:
        payload = build_chapter_payload(slug, args.source_root)
        if payload is None:
            continue
        bundle[slug] = payload
        out = THIS_DIR / slug / f"netdata_{slug}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False,
                                  separators=(",", ":")), encoding="utf-8")
        kb = out.stat().st_size / 1024
        print(f"        → {out.relative_to(REPO_ROOT)} ({kb:.0f} KB)")

    if not bundle:
        print("[chap] nada gerado.")
        return 1

    data_str = json.dumps(bundle, ensure_ascii=False, separators=(",", ":"))
    print(f"[chap] bundle total: {len(data_str) / 1024:.0f} KB "
          f"({len(bundle)} capítulos)")

    if args.inject:
        import re
        html = args.inject.read_text(encoding="utf-8")
        tag_open = '<script type="application/json" id="netdata-chapters">'
        new_tag = tag_open + data_str + "</script>"
        if 'id="netdata-chapters"' in html:
            html = re.sub(
                r'<script type="application/json" id="netdata-chapters">.*?</script>',
                lambda _m: new_tag, html, flags=re.DOTALL)
            print(f"[chap] <script id=netdata-chapters> substituído em {args.inject}")
        else:
            # insere logo após o <script id="netdata">…</script>
            anchor = re.search(
                r'(<script type="application/json" id="netdata">.*?</script>)',
                html, flags=re.DOTALL)
            if not anchor:
                print("[chap] ERRO: <script id=netdata> não encontrado para ancorar.")
                return 2
            html = html[:anchor.end()] + "\n" + new_tag + html[anchor.end():]
            print(f"[chap] <script id=netdata-chapters> inserido em {args.inject}")
        args.inject.write_text(html, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
