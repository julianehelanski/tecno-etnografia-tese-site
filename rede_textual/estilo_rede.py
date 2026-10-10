# -*- coding: utf-8 -*-
"""Identidade visual compartilhada das figuras de rede e trajetória da tese.

Alinha as redes da análise de rede textual e os diagramas de trajetória à paleta-mestra
adotada nas figuras do capítulo 2 (Okabe-Ito categórico, viridis sequencial,
marcador "bolinha" com borda branca, notação numérica pt-BR). Mantido
autônomo para os scripts continuarem reproduzíveis sem dependência externa.
"""
from __future__ import annotations

import numpy as np

# Núcleo categórico Okabe-Ito (à prova de daltonismo) na ordem de melhor
# separação para comunidades de rede.
OKABE_ITO_ORD = [
    "#0072B2",  # azul
    "#E69F00",  # laranja
    "#009E73",  # verde
    "#CC79A7",  # magenta
    "#56B4E9",  # azul claro
    "#D55E00",  # vermelho
    "#F0E442",  # amarelo
    "#999999",  # cinza
]
# Extensão para quando há mais comunidades/conceitos que o núcleo comporta
# (Gantt e alluvial chegam a 20), sem cair no arco-íris saturado.
_EXTENSAO = OKABE_ITO_ORD + [
    "#3a5fa0", "#b5651d", "#1b7a5a", "#8e4585", "#7fb2d6", "#a04000",
    "#c9b037", "#5a5a5a", "#264f78", "#d98c5f", "#2e8b57", "#b76e9b",
]

# Cores fixas de marcação na trajetória semântica (início/fim), do Okabe-Ito.
COR_INICIO = "#009E73"   # verde: início da leitura
COR_FIM = "#D55E00"      # vermelho: fim da leitura

# Tons neutros do desenho (fundo, arestas, borda da bolinha, texto).
# Texto em cinza escuro suave (nada de preto puro), sem negrito; nota em
# cinza médio itálico. Sem título embutido (a legenda do LaTeX titula).
COR_FUNDO = "#ffffff"
COR_ARESTA = "#9aa3ad"
COR_BORDA_NO = "#ffffff"  # borda branca da bolinha (identidade visual)
COR_TEXTO = "#404040"
COR_NOTA = "#8a8a8a"
FONTE = "DejaVu Sans"

# Curvatura das arestas (arc3 rad): leve arqueamento no lugar da linha reta,
# na mesma lógica da rede interativa do site.
RAD_ARESTA = 0.16


def aplicar_fonte() -> None:
    """Fonte sans-serif única em todas as figuras de rede/trajetória."""
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = FONTE


def cor_texto_sobre(fundo) -> str:
    """Branco sobre fundo escuro, cinza escuro sobre fundo claro (contraste
    legível sem negrito, para rótulos dentro de blocos coloridos)."""
    from matplotlib.colors import to_rgb
    r, g, b = to_rgb(fundo)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return "#ffffff" if lum < 0.55 else "#404040"


def nota_rodape(ax, texto: str) -> None:
    """Nota curta em itálico cinza no rodapé (substitui o título embutido)."""
    ax.text(0, -0.02, texto, transform=ax.transAxes, fontsize=9,
            style="italic", color=COR_NOTA, va="top")


def cores_categoricas(n: int) -> list[str]:
    """Devolve ``n`` cores categóricas a partir do Okabe-Ito (cicla se faltar)."""
    if n <= 0:
        return []
    return [_EXTENSAO[i % len(_EXTENSAO)] for i in range(n)]


def paleta_rgba(n: int):
    """Versão RGBA (0--1) das cores categóricas, p/ APIs que pedem array."""
    from matplotlib.colors import to_rgba
    return np.array([to_rgba(c) for c in cores_categoricas(max(n, 1))])


def cor_aresta_mistura(rgba_u, rgba_v):
    """Cor da aresta como mistura (média RGB) das cores dos dois nós que ela
    liga: arestas internas a uma comunidade herdam sua cor; arestas entre
    comunidades exibem a transição das duas cores. Equivalente estático ao
    degradê origem→destino da rede interativa do site."""
    from matplotlib.colors import to_rgba
    a = np.array(to_rgba(rgba_u))
    b = np.array(to_rgba(rgba_v))
    return tuple((a + b) / 2.0)


def cores_arestas(G, node_color_map):
    """Lista de cores RGBA, uma por aresta de ``G``, na ordem de ``G.edges()``,
    misturando as cores dos nós de cada extremidade (ver ``cor_aresta_mistura``)."""
    return [cor_aresta_mistura(node_color_map[u], node_color_map[v])
            for u, v in G.edges()]


def num_ptbr(valor) -> str:
    """Inteiro pt-BR: ponto como separador de milhar."""
    return f"{int(round(valor)):,}".replace(",", ".")


def pct_ptbr(valor, casas: int = 1) -> str:
    """Número pt-BR com vírgula decimal, sem o símbolo '%'."""
    return f"{valor:,.{casas}f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")
