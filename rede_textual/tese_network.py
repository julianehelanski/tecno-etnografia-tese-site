#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tese_network.py
===============
Gera a rede textual da TESE INTEIRA (Apresentação + capítulos 1–4 +
Considerações Finais) reaproveitando o pipeline de `rede_textual_capitulo.py`
(co-ocorrência · NPMI · Louvain · PageRank). Exporta um JSON compacto
para o site renderizar como grafo principal.

Cada capítulo é tokenizado separadamente e os fluxos são unidos com um
"sentinela" de quebra para impedir arestas espúrias na fronteira entre
capítulos. Registra ainda em quais capítulos cada termo aparece.

Uso:
    python3 rede_textual/tese_network.py --source-root /tmp/tese
Saída:
    rede_textual/tese_network.json
"""
import argparse
import html as _html
import json
import re
from pathlib import Path

from rede_textual_capitulo import (extract_tokens, build_graph, compute_npmi,
                             annotate_npmi, prune_graph, compute_metrics,
                             detect_topics, label_topic,
                             strip_latex, normalize_token, lemma,
                             collect_surface_forms)

THIS_DIR = Path(__file__).resolve().parent

# (arquivo .tex, rótulo de capítulo no site, id curto)
CHAPTERS = [
    ("ex_cap0.tex", "Apresentação", "apresentacao"),
    ("ex_cap1.tex", "Capítulo 1 · método", "cap1"),
    ("ex_cap2.tex", "Capítulo 2 · figurações", "cap2"),
    ("ex_cap3.tex", "Capítulo 3 · C4AI", "cap3"),
    ("ex_cap4.tex", "Capítulo 4 · SPIRA", "cap4"),
    ("ex_cap5.tex", "Considerações finais", "final"),
]

# paleta para as comunidades (Louvain) — tons calmos, estilo cartográfico
PALETTE = ["#6c8ebf", "#9b59c6", "#56b04a", "#ef8a3c", "#27adc4",
           "#d6489b", "#e0a82e", "#8a76c4", "#3fa6bd", "#c0556a",
           "#5f9e6e", "#b07cc6"]

BREAK = "brk"  # sentinela: não colide com nenhum token real

# conceitos-âncora da tese: sempre recebem rótulo no grafo, mesmo quando o
# PageRank os deixaria fora do núcleo (top-N). São termos de peso teórico, não
# de frequência — "tecnografia", conceito central, aparece pouco como palavra e
# co-ocorre com poucos termos, então sua centralidade estrutural é baixa. Fixá-los
# torna o argumento legível sem falsear o tamanho do nó (que segue o PageRank real).
ANCHOR_TERMS = {"tecnografia", "etnografia", "inscricao", "mediacao", "conceito"}

# nomes legíveis dos territórios, por termos-assinatura (ordem = prioridade)
TERRITORY_RULES = [
    (("ator", "actante"), "Teoria Ator-Rede"),
    (("spira", "covideiro", "espectrograma", "voz"), "SPIRA · voz, dados e diagnóstico"),
    (("laboratorio", "centro", "fapesp", "hollerith"), "C4AI · centro, laboratório e pesquisa"),
    (("militar", "vocabulario", "figuracao", "lexicometrica"), "Figurações e lexicometria"),
    (("etnografia", "patchwork", "compostagem"), "Etnografia e método"),
    (("inteligencia", "tecnologia", "algoritmo"), "Inteligência artificial e ciência"),
]


def name_territory(terms: set, used: set) -> str:
    for sig, nm in TERRITORY_RULES:
        if nm in used:
            continue
        if any(s in terms for s in sig):
            used.add(nm)
            return nm
    return ""


# Curadoria: território bibliométrico forçado.
# O mapeamento bibliométrico do campo brasileiro de IA (panorama Capes/SciELO/
# OpenAlex no cap.2 e a produção dos grupos do C4AI no cap.3) não se aglutina
# sozinho via Louvain — seu vocabulário se dispersa pelos demais territórios.
# Reunimos aqui, por curadoria, os termos mais propriamente bibliométricos
# presentes na rede, garantindo o território no mapa.
BIBLIOMETRIC_NAME = "Bibliometria · panorama do campo"
BIBLIOMETRIC_TERMS = [
    "capes", "producao", "distribuicao", "frequencia",
    "area", "base", "corpus", "brasileira",
]


def carve_bibliometric_territory(comms: list[set]) -> tuple[list[set], dict]:
    """Reúne os termos bibliométricos numa comunidade dedicada (curadoria
    forçada), retirando-os das comunidades onde o Louvain os dispersou.
    Retorna (comms_atualizadas, {índice_da_nova: nome_fixo}). Se sobrarem
    poucos termos na rede, não força o território (evita um polo artificial)."""
    present: set = set()
    for c in comms:
        present |= c
    members = {t for t in BIBLIOMETRIC_TERMS if t in present}
    if len(members) < 3:
        return comms, {}
    carved = [c - members for c in comms]
    carved = [c for c in carved if c]  # descarta comunidades esvaziadas
    carved.append(members)
    return carved, {len(carved) - 1: BIBLIOMETRIC_NAME}


def _sentences(tex: str) -> list[str]:
    clean = re.sub(r"\s+", " ", strip_latex(tex)).strip()
    return re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÀÜÇ"])', clean)


# pistas de que a frase é definicional/afirmativa (frase-tópico) e não um
# fragmento narrativo — ganham bônus na pontuação de representatividade.
_DEF_CUES = re.compile(
    r"\b(é|são|consiste|trata-se|ou seja|isto é|define-se|significa|"
    r"caracteriza|entende-se|chama-se|denomina|refere-se|representa|"
    r"corresponde|constitui|implica)\b",
    re.IGNORECASE)
# tamanho "ideal" de um trecho legível no painel (caracteres)
_IDEAL_LEN = 150


def _score_passage(nid: str, text: str, forms: set, present: set,
                   neighbors: dict) -> float:
    """Pontua o quanto uma frase é representativa para o termo `nid`.

    Sinais (em ordem de peso):
    - co-ocorrência com os vizinhos NPMI mais fortes do termo (sinal
      principal: uma boa frase coloca o termo junto de seus associados);
    - pista definicional / frase-tópico;
    - saliência do termo na própria frase (aparece >1 vez, ou perto do início);
    - frase completa e de tamanho legível.
    Penaliza frases sobrecarregadas de números (resíduo de dados/citações)."""
    nbr = neighbors.get(nid, {})
    # 1. co-ocorrência ponderada por NPMI com os vizinhos do termo
    neighbor_score = sum(nbr.get(m, 0.0) for m in present if m != nid)
    # 2. frase definicional / afirmativa
    cue = 0.6 if (_DEF_CUES.search(text) or ":" in text) else 0.0
    # 3. saliência do termo na frase
    low = text.lower()
    occ = sum(low.count(f.lower()) for f in forms)
    salience = (0.3 if occ > 1 else 0.0)
    first = min((low.find(f.lower()) for f in forms if f.lower() in low),
                default=len(text))
    if first >= 0 and first <= 40:
        salience += 0.2
    # 4. densidade temática branda (não premiar frase "empilhada" de termos)
    density = 0.12 * min(len(present), 6)
    # 5. frase completa e bem-dimensionada
    starts_ok = text[:1].isupper() or text[:1] in "\"“"
    complete = 0.25 if (starts_ok and text[-1:] in ".!?") else 0.0
    length_fit = 0.3 * (1 - min(abs(len(text) - _IDEAL_LEN) / _IDEAL_LEN, 1.0))
    # penalidade: muitos grupos de dígitos → tabela/citação/dado solto
    digits = len(re.findall(r"\d+", text))
    digit_pen = 0.4 if digits >= 3 else 0.0
    return (neighbor_score + cue + salience + density
            + complete + length_fit - digit_pen)


def collect_passages(node_ids: set, source_root: Path, neighbors: dict,
                     per_term: int = 4, lo: int = 60, hi: int = 240) -> dict:
    """Para cada termo (lema), até `per_term` frases reais da tese onde ele
    aparece, escolhidas por representatividade (não pela ordem de leitura) e
    com as ocorrências do termo destacadas em <mark>.

    `neighbors[nid]` é um dicionário {lema_vizinho: npmi} com os associados
    mais fortes do termo na rede — usado como sinal principal de relevância."""
    # candidatos por termo: (score, ch, ordem_doc, texto_limpo, forms)
    cand: dict[str, list] = {nid: [] for nid in node_ids}
    seen: dict[str, set] = {nid: set() for nid in node_ids}
    doc_order = 0
    for fname, _label, cid in CHAPTERS:
        src = source_root / fname
        if not src.exists():
            continue
        for sent in _sentences(src.read_text(encoding="utf-8")):
            doc_order += 1
            s = sent.strip()
            # limpa resíduos de comandos removidos (refs/citações)
            s = re.sub(r"\(\s*[,e]?\s*\)", "", s)   # "( )", "(e )", "( , )"
            s = re.sub(r"\(\s+", "(", s)
            s = re.sub(r"\s+\)", ")", s)
            s = re.sub(r"\s+([,.;:!?])", r"\1", s)
            s = re.sub(r"\s{2,}", " ", s).strip()
            if not (lo <= len(s) <= hi):
                continue
            if s.count("(") != s.count(")"):
                continue  # parênteses desbalanceados → frase cortada, pula
            surf: dict[str, set] = {}
            for w in re.findall(r"[A-Za-zÁ-ÿ]+", s):
                n = normalize_token(w)
                if len(n) < 4:
                    continue
                lem = lemma(n)
                if lem in node_ids:
                    surf.setdefault(lem, set()).add(w)
            present = set(surf.keys())
            for nid, forms in surf.items():
                if s in seen[nid]:
                    continue
                seen[nid].add(s)
                sc = _score_passage(nid, s, forms, present, neighbors)
                cand[nid].append((sc, cid, doc_order, s, forms))

    pas = {nid: [] for nid in node_ids}
    for nid, lst in cand.items():
        # melhor pontuação primeiro; desempata por ordem no documento (estável)
        lst.sort(key=lambda c: (-c[0], c[2]))
        used_ch: set = set()
        picked: list = []
        # 1ª passada: prioriza diversidade de capítulos
        for sc, cid, _o, s, forms in lst:
            if len(picked) >= per_term:
                break
            if cid in used_ch:
                continue
            used_ch.add(cid)
            picked.append((cid, s, forms))
        # 2ª passada: completa com os melhores restantes se faltou
        if len(picked) < per_term:
            chosen = {s for _c, s, _f in picked}
            for sc, cid, _o, s, forms in lst:
                if len(picked) >= per_term:
                    break
                if s in chosen:
                    continue
                picked.append((cid, s, forms))
        for cid, s, forms in picked:
            marked = s
            for f in sorted(forms, key=len, reverse=True):
                marked = re.sub(r"(?<!\w)(" + re.escape(f) + r")(?!\w)",
                                "\x01\\1\x02", marked)
            esc = (_html.escape(marked).replace("\x01", "<mark>")
                   .replace("\x02", "</mark>"))
            pas[nid].append({"ch": cid, "t": esc})
    return pas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", type=Path, default=Path("/tmp/tese"))
    ap.add_argument("--top-n", type=int, default=260,
                    help="nós mantidos na rede completa (por frequência)")
    ap.add_argument("--min-edge", type=int, default=3,
                    help="peso mínimo de aresta na poda")
    ap.add_argument("--core", type=int, default=80,
                    help="nº de termos na vista núcleo (por PageRank)")
    ap.add_argument("--edges-per-node", type=int, default=16,
                    help="mantém as N arestas mais fortes por termo (densidade controlada)")
    ap.add_argument("--out", type=Path, default=THIS_DIR / "tese_network.json")
    ap.add_argument("--inject", type=Path, default=None,
                    help="reinjeta o JSON no <script id=netdata> deste HTML "
                         "(ex.: index.html)")
    args = ap.parse_args()

    all_tokens: list[str] = []
    term_chapters: dict[str, set[str]] = {}
    per_chapter_counts: list[tuple[str, int]] = []
    surface: dict = {}  # token normalizado -> Counter de grafias originais

    for fname, label, cid in CHAPTERS:
        src = args.source_root / fname
        if not src.exists():
            print(f"[tese] aviso: {fname} não encontrado, pulando.")
            continue
        raw = src.read_text(encoding="utf-8")
        toks = extract_tokens(raw)
        collect_surface_forms(raw, surface)
        per_chapter_counts.append((cid, len(toks)))
        for t in set(toks):
            term_chapters.setdefault(t, set()).add(cid)
        all_tokens.extend(toks)
        all_tokens.extend([BREAK] * 4)  # impede janela cruzar capítulos

    print(f"[1] Tokens totais: {len(all_tokens):,} "
          f"({', '.join(f'{c}:{n}' for c, n in per_chapter_counts)})")

    G_full = build_graph(all_tokens, window=4)
    npmi = compute_npmi(all_tokens, window=4)
    annotate_npmi(G_full, npmi)
    if BREAK in G_full:
        G_full.remove_node(BREAK)
    print(f"    Rede completa: {G_full.number_of_nodes()} nós, "
          f"{G_full.number_of_edges()} arestas")

    G = prune_graph(G_full, top_n=args.top_n, min_edge_weight=args.min_edge)
    annotate_npmi(G, npmi)
    print(f"[2] Após poda: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")

    deg, btw, pr = compute_metrics(G)
    comms = detect_topics(G)
    comms, forced_names = carve_bibliometric_territory(comms)
    if forced_names:
        print(f"    Curadoria: território bibliométrico forçado com "
              f"{len(comms[-1])} termos ({', '.join(sorted(comms[-1]))})")
    print(f"[3] Comunidades: {len(comms)} | tamanhos: {[len(c) for c in comms]}")

    # densidade controlada: mantém as K arestas mais fortes por termo (união),
    # preservando conectividade e o caráter "panorama" sem virar emaranhado total.
    K = args.edges_per_node
    keep_edges: set = set()
    for n in G.nodes():
        nbr = sorted(G[n].items(), key=lambda kv: kv[1].get("weight", 0), reverse=True)
        for m, _ in nbr[:K]:
            keep_edges.add((n, m) if n < m else (m, n))
    drop = [(u, v) for u, v in G.edges() if (u, v) not in keep_edges
            and (v, u) not in keep_edges]
    G.remove_edges_from(drop)
    print(f"    Densidade: {G.number_of_edges()} arestas após manter top-{K} por termo")

    # id de comunidade por nó
    comm_of: dict[str, int] = {}
    for i, c in enumerate(comms):
        for n in c:
            comm_of[n] = i

    # núcleo: top-N por PageRank
    core = sorted(G.nodes(), key=lambda n: pr.get(n, 0), reverse=True)[:args.core]
    core_set = set(core)

    # trechos reais da tese por termo (com o termo destacado), escolhidos por
    # representatividade: para cada termo, seus vizinhos NPMI mais fortes são o
    # sinal principal — uma boa frase coloca o termo junto de seus associados.
    node_ids = set(G.nodes())
    npmi_neighbors: dict[str, dict] = {}
    for n in G.nodes():
        nbr = sorted(G[n].items(),
                     key=lambda kv: (kv[1].get("npmi", 0), kv[1].get("weight", 0)),
                     reverse=True)
        npmi_neighbors[n] = {m: float(d.get("npmi", 0)) for m, d in nbr[:12]}
    passages = collect_passages(node_ids, args.source_root, npmi_neighbors)
    tot_pas = sum(len(v) for v in passages.values())
    print(f"    Trechos extraídos: {tot_pas} (termos com ≥1 trecho: "
          f"{sum(1 for v in passages.values() if v)})")

    # ordem de capítulo para um termo (menor índice em que aparece) — para cor de origem
    order = {cid: k for k, (_, _, cid) in enumerate(CHAPTERS)}

    def display_label(node_id: str) -> str:
        """Rótulo re-acentuado: grafia de superfície mais frequente cuja forma
        normalizada é exatamente o id do nó; se não houver, usa o próprio id."""
        c = surface.get(node_id)
        return c.most_common(1)[0][0] if c else node_id

    nodes = []
    for n in G.nodes():
        chs = sorted(term_chapters.get(n, set()), key=lambda c: order.get(c, 99))
        nodes.append({
            "id": n,
            "label": display_label(n),
            "community": comm_of.get(n, 0),
            "freq": int(G.nodes[n].get("freq", 0)),
            "degree": round(float(deg.get(n, 0)), 1),
            "pagerank": round(float(pr.get(n, 0)), 5),
            "betweenness": round(float(btw.get(n, 0)), 4),
            "chapters": chs,
            "core": n in core_set,
            "pin": n in ANCHOR_TERMS,
            "passages": passages.get(n, []),
        })

    edges = []
    for u, v, d in G.edges(data=True):
        edges.append({
            "s": u, "t": v,
            "w": round(float(d.get("weight", 0)), 1),
            "npmi": round(float(d.get("npmi", 0)), 3),
        })

    communities = []
    used_names: set = set()
    for i, c in enumerate(comms):
        communities.append({
            "id": i,
            "size": len(c),
            "name": forced_names.get(i) or name_territory(c, used_names),
            "label": [display_label(t) for t in label_topic(c, deg, k=5)],
            "color": PALETTE[i % len(PALETTE)],
        })

    payload = {
        "generated_from": "tese (Apresentação + cap1–4 + Considerações Finais)",
        "params": {"window": 4, "top_n": args.top_n,
                   "min_edge": args.min_edge, "core": args.core},
        "chapters": [{"id": cid, "label": label} for _, label, cid in CHAPTERS],
        "communities": communities,
        "nodes": nodes,
        "edges": edges,
    }
    data_str = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    args.out.write_text(data_str, encoding="utf-8")
    kb = args.out.stat().st_size / 1024
    print(f"[4] JSON: {args.out}  ({kb:.0f} KB)  "
          f"{len(nodes)} nós, {len(edges)} arestas, {len(communities)} comunidades, "
          f"núcleo={len(core)}")
    # prévia das comunidades
    for c in communities:
        print(f"    T{c['id']} ({c['size']}): {c.get('name') or ', '.join(c['label'])}")

    # reinjeta no HTML alvo (substitui o conteúdo de <script id="netdata">)
    if args.inject is not None:
        assert "</script" not in data_str.lower(), "JSON contém </script>"
        html = args.inject.read_text(encoding="utf-8")
        pat = re.compile(
            r'(<script type="application/json" id="netdata">).*?(</script>)',
            re.DOTALL)
        new, n = pat.subn(lambda m: m.group(1) + data_str + m.group(2), html, count=1)
        if n != 1:
            print(f"[inject] ERRO: <script id=netdata> não encontrado em {args.inject}")
            return 1
        args.inject.write_text(new, encoding="utf-8")
        print(f"[5] JSON reinjetado em {args.inject}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
