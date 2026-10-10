"""
Narrative trajectory analysis of a thesis chapter.

Three complementary views, all answering questions about *order* and
*flow* rather than aggregate co-occurrence:

  1. Gantt lexical (`trajectory_gantt.png`):
     for each top concept, draws a horizontal life-span from its first
     paragraph to its last; ticks mark every occurrence. Sorted by
     entry order — answers "where does each idea enter and exit?".

  2. Alluvial / Sankey (`trajectory_alluvial.png`):
     splits the chapter into K sequential segments, ranks the top
     concepts per segment, and connects them across adjacent segments
     when they persist — answers "what links to what across the chapter?".

  3. Semantic trajectory (`trajectory_semantic.png`):
     embeds each paragraph with a multilingual sentence-transformer,
     projects to 2D with PCA, draws the path through that space colored
     by reading order — answers "what arc does the chapter trace?".

Reuses tokenization / lemmatization from `rede_textual_capitulo.py`.

CLI:
    python narrative_trajectory.py                           # cap1 default
    python narrative_trajectory.py --chapter PATH --slug X --title "Capítulo X"
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

from rede_textual_capitulo import (  # noqa: E402
    LATEX_CMD_TOKENS,
    PT_STOPWORDS,
    DEFAULT_SRC,
    lemma,
    normalize_token,
    strip_latex,
)
from estilo_rede import (  # noqa: E402
    COR_BORDA_NO, COR_FIM, COR_INICIO, COR_NOTA, COR_TEXTO, cor_texto_sobre,
    cores_categoricas, nota_rodape, num_ptbr, pct_ptbr,
)


# ---------------------------------------------------------------------------
# 1. Paragraph extraction (preserves reading order)
# ---------------------------------------------------------------------------

def extract_paragraphs(raw: str, min_chars: int = 120) -> list[str]:
    """Split chapter into paragraphs after LaTeX cleanup, keeping order.

    LaTeX environments like figure/citacaoabnt produce short or empty
    paragraphs after stripping; we filter those out by character length.
    """
    cleaned = strip_latex(raw)
    paras = [p.strip() for p in re.split(r"\n{2,}", cleaned)]
    paras = [re.sub(r"\s+", " ", p) for p in paras]
    return [p for p in paras if len(p) >= min_chars]


def tokenize(text: str) -> list[str]:
    out: list[str] = []
    for tok in re.findall(r"[A-Za-zÁ-ÿ]+", text):
        n = normalize_token(tok)
        if not n or len(n) < 4:
            continue
        if n in PT_STOPWORDS or n in LATEX_CMD_TOKENS:
            continue
        out.append(lemma(n))
    return out


# ---------------------------------------------------------------------------
# 2. Gantt lexical
# ---------------------------------------------------------------------------

def render_gantt(paras: list[str], para_tokens: list[list[str]],
                  top_concepts: list[str], path: Path, title: str):
    info = {}
    for c in top_concepts:
        positions = [i for i, ts in enumerate(para_tokens) if c in ts]
        if not positions:
            continue
        info[c] = {
            "first": positions[0],
            "last": positions[-1],
            "all": positions,
            "count": sum(ts.count(c) for ts in para_tokens),
        }

    concepts_sorted = sorted(info.items(), key=lambda kv: kv[1]["first"])

    fig, ax = plt.subplots(figsize=(17, max(8, 0.42 * len(concepts_sorted) + 2)))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    palette = cores_categoricas(len(concepts_sorted))
    n_paras = len(paras)

    for i, (c, d) in enumerate(concepts_sorted):
        col = palette[i]
        ax.hlines(y=i, xmin=d["first"], xmax=d["last"], colors=col, linewidth=5, alpha=0.40)
        ax.scatter(d["all"], [i] * len(d["all"]), color=col, s=34,
                   edgecolor=COR_BORDA_NO, linewidth=0.8, zorder=3)
        ax.text(d["last"] + 0.6, i, f"  {c}  ({num_ptbr(d['count'])}×)",
                va="center", fontsize=9, color=COR_TEXTO)
        ax.text(d["first"] - 0.6, i, f"¶{d['first']+1}",
                va="center", ha="right", fontsize=8, color="#6b7280")

    ax.set_yticks([])
    ax.set_xlabel("parágrafo (ordem de leitura) →", fontsize=11, color=COR_TEXTO)
    ax.set_xlim(-3, n_paras + 8)
    ax.set_ylim(-1, len(concepts_sorted))
    ax.invert_yaxis()
    nota_rodape(
        ax,
        "Gantt lexical: barra = ‘vida’ do conceito · pontos = ocorrências · "
        "ordenado por entrada",
    )
    ax.grid(axis="x", alpha=0.2)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor="#ffffff")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Alluvial / Sankey across K segments
# ---------------------------------------------------------------------------

def render_alluvial(paras: list[str], para_tokens: list[list[str]],
                     path: Path, title: str, K: int = 8, top_per_seg: int = 5):
    """Fluxo de tópicos por segmento em faixas horizontais fixas por termo.

    Cada termo que entra no top-``top_per_seg`` de algum segmento ganha uma
    faixa (linha) própria, rotulada uma única vez à esquerda; nos segmentos em
    que é top, desenha-se um bloco com a sua contagem local, e blocos de
    segmentos consecutivos são unidos por uma fita contínua da cor do termo.
    Assim cada termo se lê como um rio horizontal, e a persistência aparece
    como faixa ininterrupta, em vez dos blocos que trocavam de linha a cada
    mudança de ranking na versão anterior.
    """
    n = len(paras)
    bounds = [(round(k * n / K), round((k + 1) * n / K)) for k in range(K)]

    seg_counts = []
    for s, e in bounds:
        toks = [t for i in range(s, e) for t in para_tokens[i]]
        seg_counts.append(Counter(toks))
    seg_top = [[w for w, _ in c.most_common(top_per_seg)] for c in seg_counts]

    # Presença de cada termo: em quais segmentos é top-5 e com que contagem.
    present: dict[str, dict[int, int]] = {}
    for k, top in enumerate(seg_top):
        for c in top:
            present.setdefault(c, {})[k] = seg_counts[k][c]

    def first_seg(c: str) -> int:
        return min(present[c])

    def total(c: str) -> int:
        return sum(present[c].values())

    # Ordena as faixas pela ordem de entrada na cadeia e, em empate, pelo peso.
    universe = sorted(present, key=lambda c: (first_seg(c), -total(c)))
    L = len(universe)
    cmap = plt.cm.tab20(np.linspace(0, 1, 20))
    color = {c: cmap[i % 20] for i, c in enumerate(universe)}
    lane = {c: i for i, c in enumerate(universe)}

    row_h, row_gap = 0.62, 0.5
    step = row_h + row_gap
    lane_y = {c: -lane[c] * step for c in universe}
    col_x = np.arange(K) * 3.0
    box_w = 1.0

    fig, ax = plt.subplots(figsize=(19, max(7.0, 0.52 * L + 1.5)))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # Fitas de persistência (segmentos consecutivos) — horizontais, na faixa do termo.
    for c in universe:
        segs = sorted(present[c])
        for a, b in zip(segs, segs[1:]):
            if b == a + 1:
                x1, x2 = col_x[a] + box_w / 2, col_x[b] - box_w / 2
                y = lane_y[c]
                ax.fill_between([x1, x2], y - row_h * 0.42, y + row_h * 0.42,
                                color=color[c], alpha=0.38, linewidth=0)

    # Blocos por segmento, com a contagem local dentro.
    for c in universe:
        y = lane_y[c]
        for k, cnt in present[c].items():
            ax.add_patch(plt.Rectangle(
                (col_x[k] - box_w / 2, y - row_h / 2), box_w, row_h,
                facecolor=color[c], edgecolor="#1a1d22", linewidth=0.6))
            ax.text(col_x[k], y, str(cnt), ha="center", va="center",
                    fontsize=8, color="#0e1116")

    # Rótulo e amostra de cor de cada faixa, à esquerda (uma vez por termo).
    x_label = col_x[0] - box_w / 2 - 0.35
    for c in universe:
        y = lane_y[c]
        ax.add_patch(plt.Rectangle((x_label - 0.28, y - row_h / 2), 0.24, row_h,
                                   facecolor=color[c], edgecolor="none"))
        ax.text(x_label - 0.36, y, c, ha="right", va="center",
                fontsize=10, color="#0e1116", fontweight="bold")
        # Marcador de estreia (primeira aparição na cadeia).
        k0 = first_seg(c)
        ax.plot([col_x[k0] - box_w / 2 - 0.24, col_x[k0] - box_w / 2], [y, y],
                color=color[c], lw=2)
        ax.plot(col_x[k0] - box_w / 2 - 0.24, y, marker=">", markersize=7,
                color=color[c])

    # Cabeçalhos dos segmentos.
    y_head = row_h / 2 + 0.5
    for k, (s, e) in enumerate(bounds):
        ax.text(col_x[k], y_head, f"Seg. {k+1}\n¶{s+1}–{e}",
                ha="center", va="bottom", fontsize=10, color="#374151",
                fontweight="bold")

    ax.set_xlim(x_label - 3.2, col_x[-1] + box_w)
    ax.set_ylim(-(L - 1) * step - row_h, y_head + 1.4)
    ax.axis("off")
    ax.set_title(
        f"{title} · fluxo de tópicos por segmento (top-{top_per_seg} em {K} segmentos sequenciais)\n"
        "cada faixa é um termo · bloco = presença no top-5 (número = contagem local) · "
        "fita = persistência entre segmentos vizinhos · ▶ = estreia na cadeia",
        fontsize=13, color="#0e1116", pad=14,
    )
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor="#ffffff")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Semantic trajectory (paragraph embeddings → PCA 2D)
# ---------------------------------------------------------------------------

def _dodge_labels(fig, ax, texts, anchors, *, pad_px: float = 3.0,
                  anchor_pad_px: float = 12.0, point_pad_px: float = 7.0,
                  special_pad_px: float = 22.0, special_idx=(),
                  obstacle_pad_px: float = 6.0, obstacles=None,
                  iterations: int = 1400,
                  connector_color: str = "#94a3b8") -> None:
    """Separa rótulos sobrepostos por repulsão iterativa em coordenadas de tela.

    Substitui a dependência externa ``adjustText`` (ausente no ambiente local
    da Juliane, o que fazia o código cair num deslocamento radial fraco e
    deixar os rótulos empilhados). O algoritmo lê a caixa real de cada texto
    a partir do renderer e empurra, por repulsão iterativa ao longo do eixo de
    menor penetração: (1) rótulos que se sobrepõem entre si; (2) cada rótulo
    para fora de todas as bolinhas-âncora, com folga maior nos marcadores
    especiais ``special_idx`` (estrela de início e X de fim) para que eles
    fiquem sempre visíveis; (3) rótulos para fora de obstáculos como a caixa
    de legenda. Ao final desenha um conector fino do rótulo ao seu ponto. É
    determinístico (sem aleatoriedade), coerente com a política de seeds fixas.

    Deve ser chamado depois de ``fig.tight_layout()`` e antes de ``savefig``,
    para que as caixas medidas correspondam ao layout final salvo.
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pts = ax.transData.transform(np.asarray(anchors, dtype=float))

    n = len(texts)
    m = len(pts)
    centers = np.zeros((n, 2))
    sizes = np.zeros((n, 2))
    for i, t in enumerate(texts):
        # Medir a CAIXA visível (patch do bbox arredondado), não só o texto:
        # o patch é maior que o texto pela folga do boxstyle, e era por isso
        # que rótulos "separados" ainda tinham as caixas brancas sobrepostas.
        patch = t.get_bbox_patch()
        bb = (patch.get_window_extent(renderer)
              if patch is not None else t.get_window_extent(renderer=renderer))
        centers[i] = [(bb.x0 + bb.x1) / 2.0, (bb.y0 + bb.y1) / 2.0]
        sizes[i] = [bb.width, bb.height]

    special = set(special_idx)
    obstacle_boxes = []
    for ob in (obstacles or []):
        try:
            obstacle_boxes.append(ob.get_window_extent(renderer=renderer))
        except Exception:
            pass

    def separate_labels() -> bool:
        """Empurra pares de rótulos sobrepostos (caixas visíveis) ao longo do
        eixo de menor penetração. É a restrição prioritária."""
        moved = False
        for i in range(n):
            for j in range(i + 1, n):
                dx = centers[i, 0] - centers[j, 0]
                dy = centers[i, 1] - centers[j, 1]
                ox = (sizes[i, 0] + sizes[j, 0]) / 2.0 + pad_px - abs(dx)
                oy = (sizes[i, 1] + sizes[j, 1]) / 2.0 + pad_px - abs(dy)
                if ox > 0 and oy > 0:
                    moved = True
                    if ox <= oy:
                        s = ox / 2.0 * (1.0 if dx >= 0 else -1.0)
                        centers[i, 0] += s
                        centers[j, 0] -= s
                    else:
                        s = oy / 2.0 * (1.0 if dy >= 0 else -1.0)
                        centers[i, 1] += s
                        centers[j, 1] -= s
        return moved

    def repel_points() -> bool:
        """Afasta cada rótulo de TODAS as bolinhas (mantém marcadores à vista);
        folga maior na própria âncora e maior ainda em início/fim."""
        moved = False
        for i in range(n):
            for p in range(m):
                if p == i:
                    pad = anchor_pad_px
                elif p in special:
                    pad = special_pad_px
                else:
                    pad = point_pad_px
                dx = centers[i, 0] - pts[p, 0]
                dy = centers[i, 1] - pts[p, 1]
                ox = sizes[i, 0] / 2.0 + pad - abs(dx)
                oy = sizes[i, 1] / 2.0 + pad - abs(dy)
                if ox > 0 and oy > 0:
                    moved = True
                    if ox <= oy:
                        centers[i, 0] += ox * (1.0 if dx >= 0 else -1.0)
                    else:
                        centers[i, 1] += oy * (1.0 if dy >= 0 else -1.0)
        return moved

    def repel_obstacles() -> bool:
        """Afasta rótulos de obstáculos (ex.: caixa de legenda)."""
        moved = False
        for i in range(n):
            for bb in obstacle_boxes:
                lx0 = centers[i, 0] - sizes[i, 0] / 2.0 - obstacle_pad_px
                lx1 = centers[i, 0] + sizes[i, 0] / 2.0 + obstacle_pad_px
                ly0 = centers[i, 1] - sizes[i, 1] / 2.0 - obstacle_pad_px
                ly1 = centers[i, 1] + sizes[i, 1] / 2.0 + obstacle_pad_px
                ox = min(lx1, bb.x1) - max(lx0, bb.x0)
                oy = min(ly1, bb.y1) - max(ly0, bb.y0)
                if ox > 0 and oy > 0:
                    moved = True
                    cx = (bb.x0 + bb.x1) / 2.0
                    cy = (bb.y0 + bb.y1) / 2.0
                    if ox <= oy:
                        centers[i, 0] += ox * (1.0 if centers[i, 0] >= cx else -1.0)
                    else:
                        centers[i, 1] += oy * (1.0 if centers[i, 1] >= cy else -1.0)
        return moved

    # Fase 1: todas as restrições. A separação rótulo-rótulo vem por último
    # para que o estado de saída tenda a não ter sobreposição entre rótulos.
    for _ in range(iterations):
        moved = repel_points()
        moved = repel_obstacles() or moved
        moved = separate_labels() or moved
        if not moved:
            break

    # Fase 2: limpeza dedicada. Sem a repulsão dos pontos (que poderia reabrir
    # colisões), garante zero sobreposição entre rótulos e fora da legenda. Os
    # marcadores de início/fim seguem visíveis pelo zorder, mesmo se um rótulo
    # encostar numa bolinha comum.
    for _ in range(800):
        moved = repel_obstacles()
        moved = separate_labels() or moved
        if not moved:
            break

    inv = ax.transData.inverted()
    new_pos = inv.transform(centers)
    anchors_data = np.asarray(anchors, dtype=float)
    for i, t in enumerate(texts):
        t.set_position((new_pos[i, 0], new_pos[i, 1]))
        t.set_ha("center")
        t.set_va("center")
        ax.annotate("", xy=(anchors_data[i, 0], anchors_data[i, 1]),
                    xytext=(new_pos[i, 0], new_pos[i, 1]),
                    xycoords="data", textcoords="data",
                    arrowprops=dict(arrowstyle="-", color=connector_color,
                                    lw=0.6, alpha=0.8), zorder=4)


def render_semantic_trajectory(paras: list[str], para_tokens: list[list[str]],
                                 path: Path, title: str, group_size: int | None = None,
                                 target_moments: int = 22):
    """Embed groups of paragraphs ("moments") and project to 2D.

    Tries the multilingual sentence-transformer first; if the model can't
    be downloaded (offline / blocked), falls back to TF-IDF + Truncated SVD
    (Latent Semantic Analysis), which is a respectable in-corpus embedding
    that captures the same notion of paragraph similarity without external
    weights.

    Paragraphs are grouped into windows of `group_size` to produce a
    smoother trajectory; per-paragraph embeddings of a long chapter tend
    to live in a noisy high-dimensional space whose 2D projection is
    visually overcrowded. To keep the labels legible, `group_size` is
    chosen adaptively so the chapter yields ~`target_moments` moments
    (instead of a fixed window that produced 40-50 cramped labels), and
    the moment labels are de-collided with the built-in `_dodge_labels`
    (deterministic, no external dependency).
    """
    from sklearn.decomposition import PCA, TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer

    # Group paragraphs into moments. Adaptive window: aim for ~target_moments
    # so the 2D plot does not overcrowd with overlapping labels.
    n_paras = len(paras)
    if group_size is None:
        group_size = max(5, math.ceil(n_paras / max(1, target_moments)))
    moments_text: list[str] = []
    moments_tokens: list[list[str]] = []
    moments_bounds: list[tuple[int, int]] = []
    for s in range(0, n_paras, group_size):
        e = min(s + group_size, n_paras)
        moments_text.append(" ".join(paras[s:e]))
        moments_tokens.append([t for i in range(s, e) for t in para_tokens[i]])
        moments_bounds.append((s, e))

    method = "sentence-transformer (paraphrase-multilingual-MiniLM-L12-v2)"
    try:
        from sentence_transformers import SentenceTransformer
        print("    [embeddings] tentando sentence-transformer ...")
        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        emb = model.encode(moments_text, show_progress_bar=False, batch_size=16,
                            normalize_embeddings=True)
        pca = PCA(n_components=2)
        coords = pca.fit_transform(emb)
        var_ratio = pca.explained_variance_ratio_
    except Exception as e:
        print(f"    [embeddings] fallback para TF-IDF + LSA ({type(e).__name__})")
        method = "TF-IDF + LSA (Truncated SVD, in-corpus)"
        joined = [" ".join(ts) for ts in moments_tokens]
        vec = TfidfVectorizer(min_df=1, max_df=0.9, ngram_range=(1, 2),
                               sublinear_tf=True)
        X = vec.fit_transform(joined)
        n_components = min(40, X.shape[0] - 1, X.shape[1] - 1)
        svd = TruncatedSVD(n_components=n_components, random_state=7)
        emb = svd.fit_transform(X)
        norms = np.linalg.norm(emb, axis=1, keepdims=True)
        emb = emb / np.maximum(norms, 1e-9)
        pca = PCA(n_components=2)
        coords = pca.fit_transform(emb)
        var_ratio = pca.explained_variance_ratio_

    var1, var2 = var_ratio[0] * 100, var_ratio[1] * 100

    fig, ax = plt.subplots(figsize=(16, 12))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    n = len(coords)
    colors = plt.cm.viridis(np.linspace(0, 1, n))

    # Trajectory arrows
    for i in range(n - 1):
        ax.annotate("", xy=coords[i + 1], xytext=coords[i],
                    arrowprops=dict(arrowstyle="-|>", color=colors[i],
                                     alpha=0.7, lw=1.6,
                                     mutation_scale=14))

    # Points (bolinha com borda branca, identidade visual da tese)
    ax.scatter(coords[:, 0], coords[:, 1], s=160, c=colors,
                edgecolor=COR_BORDA_NO, linewidth=1.2, zorder=3)

    # Label every moment with its dominant term. The de-collision happens
    # later (after tight_layout, via `_dodge_labels`) so the boxes are
    # separated against the final saved layout.
    labels = []
    for i, (s, e) in enumerate(moments_bounds):
        c = Counter(moments_tokens[i])
        top_term = c.most_common(1)[0][0] if c else "—"
        labels.append(f"¶{s+1}–{e} · {top_term}")

    texts = [ax.text(coords[i, 0], coords[i, 1], lab,
                     fontsize=9, color=COR_TEXTO,
                     ha="center", va="center", zorder=5,
                     bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                               edgecolor="#cbd5e1", linewidth=0.6, alpha=0.95))
             for i, lab in enumerate(labels)]

    # Give the labels room to spread without being clipped by the axes.
    span_x = float(coords[:, 0].max() - coords[:, 0].min()) or 1.0
    span_y = float(coords[:, 1].max() - coords[:, 1].min()) or 1.0
    ax.set_xlim(coords[:, 0].min() - 0.22 * span_x,
                coords[:, 0].max() + 0.22 * span_x)
    ax.set_ylim(coords[:, 1].min() - 0.22 * span_y,
                coords[:, 1].max() + 0.22 * span_y)

    # Start / end markers. zorder acima dos rótulos (5) para que a estrela de
    # início e o X de fim fiquem sempre visíveis, mesmo em regiões adensadas.
    ax.scatter(*coords[0], s=520, marker="*", color=COR_INICIO,
                edgecolor="#ffffff", linewidth=1.6, zorder=6,
                label=f"início · ¶1–{moments_bounds[0][1]}")
    ax.scatter(*coords[-1], s=340, marker="X", color=COR_FIM,
                edgecolor="#ffffff", linewidth=1.6, zorder=6,
                label=f"fim · ¶{moments_bounds[-1][0]+1}–{moments_bounds[-1][1]}")

    ax.set_xlabel(f"PC1 ({pct_ptbr(var1)}% da variância)", fontsize=11, color=COR_TEXTO)
    ax.set_ylabel(f"PC2 ({pct_ptbr(var2)}% da variância)", fontsize=11, color=COR_TEXTO)
    nota_rodape(
        ax,
        f"trajetória semântica em {n} momentos (grupos de {group_size} parágrafos) · "
        f"embeddings {method} · projeção PCA 2D · cor = ordem de leitura",
    )
    legend = ax.legend(loc="best", frameon=True, framealpha=0.9)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    # De-collide the moment labels against the final layout: keep them off each
    # other, off every marker (with extra room around the start/end markers) and
    # out of the legend box.
    _dodge_labels(fig, ax, texts, coords, special_idx=(0, n - 1),
                  obstacles=[legend])
    fig.savefig(path, dpi=160, facecolor="#ffffff")
    plt.close(fig)

    return coords


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(src: Path, slug: str, title: str, out: Path) -> None:
    """Generate Gantt, alluvial and semantic trajectory PNGs for one chapter."""
    out.mkdir(parents=True, exist_ok=True)
    raw = src.read_text(encoding="utf-8")
    paras = extract_paragraphs(raw)
    para_tokens = [tokenize(p) for p in paras]
    print(f"[1] [{slug}] Paragraphs extracted: {len(paras)}")
    print(f"    Tokens per paragraph (mean): {np.mean([len(t) for t in para_tokens]):.1f}")

    # Pick concepts to display in the Gantt: top by frequency, but skipping
    # generic ones whose ubiquity drowns the timeline.
    flat = [t for ts in para_tokens for t in ts]
    freq = Counter(flat)
    GANTT_SIZE = 20
    SKIP = {"parte", "modo", "tipo", "questao", "geral", "exemplo",
            "claude"}
    candidates = [w for w, _ in freq.most_common(60) if w not in SKIP]
    top_concepts = candidates[:GANTT_SIZE]

    print(f"[2] Rendering Gantt ({len(top_concepts)} concepts) ...")
    render_gantt(paras, para_tokens, top_concepts,
                 out / "trajectory_gantt.png", title=title)

    print(f"[3] Rendering alluvial flow (K=8 segments) ...")
    render_alluvial(paras, para_tokens, out / "trajectory_alluvial.png",
                    title=title, K=8, top_per_seg=5)

    print(f"[4] Rendering semantic trajectory ...")
    render_semantic_trajectory(paras, para_tokens,
                               out / "trajectory_semantic.png", title=title)

    print(f"[5] [{slug}] Done. Outputs:")
    for n in ["trajectory_gantt.png", "trajectory_alluvial.png", "trajectory_semantic.png"]:
        print("    -", out / n)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--chapter", type=Path, default=DEFAULT_SRC,
                   help=f"Path to the LaTeX chapter file (default: {DEFAULT_SRC}).")
    p.add_argument("--slug", default="cap1",
                   help="Short identifier (default: cap1).")
    p.add_argument("--title", default="Capítulo 1",
                   help="Human-readable label used in figure titles.")
    p.add_argument("--out", type=Path, default=None,
                   help="Output directory. Default: rede_textual/<slug>/.")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    out = args.out if args.out is not None else THIS_DIR / args.slug
    run(src=args.chapter, slug=args.slug, title=args.title, out=out)


if __name__ == "__main__":
    main()
