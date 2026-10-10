#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_tese_network_figura.py
=============================
Gera a figura estática da rede textual da TESE INTEIRA a partir de
``tese_network.json`` (o mesmo grafo que a capa do site renderiza de forma
interativa), reaproveitando o estilo das figuras por capítulo: arestas
arqueadas e coloridas pela mistura das cores de comunidade das pontas.

Não reconstrói o grafo a partir do ``.tex``: lê o JSON já computado por
``tese_network.py``, de modo que a figura do texto impresso e o grafo do
site partem exatamente dos mesmos nós, arestas e comunidades.

Saída:
    figuras/rede_tese_inteira.png

Uso:
    python3 rede_textual/render_tese_network_figura.py
"""
from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

from rede_textual_capitulo import render_network

THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parent

# Poda de legibilidade para a versão estática: o grafo interativo do site
# suporta as 3092 arestas, mas em papel elas viram borrão. Mantenho as
# arestas de peso mais alto (co-ocorrência frequente) e removo nós que
# ficam sem ligação, preservando o núcleo denso e legível da tese.
MIN_EDGE_WEIGHT = 15


def carregar_grafo(json_path: Path) -> tuple[nx.Graph, list[set[str]], dict[str, float]]:
    """Lê ``tese_network.json`` e devolve (grafo, comunidades, degrees)."""
    data = json.loads(json_path.read_text(encoding="utf-8"))
    nodes = data["nodes"]
    edges = data["edges"]
    comunidades = data["communities"]

    G = nx.Graph()
    for n in nodes:
        G.add_node(n["id"], freq=n.get("freq", 0))
    for e in edges:
        G.add_edge(e["s"], e["t"], weight=float(e["w"]), npmi=float(e.get("npmi", 0.0)))

    deg = {n["id"]: float(n.get("degree", 0.0)) for n in nodes}

    # Comunidades na ordem do JSON (maior para menor), como lista de conjuntos.
    id_por_comm: dict[int, set[str]] = {}
    for n in nodes:
        id_por_comm.setdefault(int(n["community"]), set()).add(n["id"])
    ordem = [int(c["id"]) for c in sorted(comunidades, key=lambda z: z.get("size", 0),
                                          reverse=True)]
    comms = [id_por_comm.get(cid, set()) for cid in ordem if id_por_comm.get(cid)]
    return G, comms, deg


def main() -> None:
    json_path = THIS_DIR / "tese_network.json"
    if not json_path.exists():
        raise FileNotFoundError(
            f"{json_path} não existe. Rode antes tese_network.py "
            "(no pipeline, com o .tex da tese)."
        )
    G, comms, deg = carregar_grafo(json_path)

    # Poda para a versão estática.
    G.remove_edges_from([(u, v) for u, v, d in G.edges(data=True)
                         if d["weight"] < MIN_EDGE_WEIGHT])
    G.remove_nodes_from(list(nx.isolates(G)))

    out = REPO_ROOT / "figuras" / "rede_tese_inteira.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    render_network(G, comms, deg, out,
                   title="Rede textual da tese inteira (Apresentação, "
                         "capítulos 1 a 4 e Considerações finais)",
                   label_top=32)
    print(f"Figura gerada: {out} "
          f"({G.number_of_nodes()} nós, {G.number_of_edges()} arestas)")


if __name__ == "__main__":
    main()
