# Parâmetros da análise textual (rede de termos)

Valores exatos do pipeline que gera as redes de co-ocorrência do site.
Atenção: a **rede do mapa** (`rede_textual/tese_network.py`) e a **rede por
capítulo** (`rede_textual/rede_textual_capitulo.py`) usam valores diferentes.

Método em cadeia: **co-ocorrência → NPMI → poda → PageRank → Louvain**.

---

## Rede do MAPA do site — `rede_textual/tese_network.py`

Ajustáveis por flag (padrão entre parênteses):

| Parâmetro | Flag | Padrão | O que faz |
|---|---|---|---|
| Janela de co-ocorrência | *(fixo no código)* | **4** | desliza uma janela de 4 palavras; cada par dentro dela vira aresta |
| Peso por proximidade | *(fixo)* | `w = janela − distância` | pares mais próximos pesam mais (adjacentes = 3, …) |
| Nós mantidos | `--top-n` | **260** | mantém os 260 termos mais **frequentes** |
| Poda de arestas | `--min-edge` | **3** | remove arestas com peso < 3 |
| Densidade | `--edges-per-node` | **16** | mantém só as 16 arestas mais fortes por termo |
| Vista núcleo (rótulos) | `--core` | **80** | os 80 maiores por PageRank ganham rótulo em destaque |
| NPMI | *(fixo)* | janela **4** | força das ligações (*normalized pointwise mutual information*) |
| PageRank | *(fixo)* | **α = 0.85** | tamanho dos nós (`max_iter=500`, `tol=1e-8`) |
| Louvain | *(fixo)* | **resolution = 1.0**, com `seed` | comunidades (os agrupamentos coloridos) |

Exemplo sobrescrevendo:

```bash
export PYTHONHASHSEED=0
python rede_textual/tese_network.py --source-root _tex \
  --top-n 260 --min-edge 3 --edges-per-node 16 --core 80 --inject index.html
```

---

## Rede por CAPÍTULO — `rede_textual/rede_textual_capitulo.py`

Valores usados na rotina principal (chamada por `run_all.py`):

| Parâmetro | Valor | Observação |
|---|---|---|
| Janela | **4** | igual ao mapa |
| Nós mantidos (`top_n`) | **180** | menor que o mapa (260) |
| Poda (`min_edge_weight`) | **2** | menor que o mapa (3) |
| Vista "focus" | **top 100 por grau** | subgrafo destacado |
| PageRank / Louvain | **α=0.85 / res=1.0** | iguais |

---

## Onde mexer no código

- **Parâmetros do mapa:** defaults no `_parse_args()` de
  `rede_textual/tese_network.py` (≈ linhas 237–244) — ou apenas passe as flags.
- **Janela, NPMI, PageRank, Louvain:** funções `build_graph`,
  `compute_npmi`, `prune_graph`, `compute_metrics` em
  `rede_textual/rede_textual_capitulo.py` (a janela `window=4` é passada nas
  chamadas; α e resolution estão fixos em `compute_metrics`).
- **Stopwords (palavras ignoradas):** conjunto `PT_STOPWORDS` no topo de
  `rede_textual/rede_textual_capitulo.py`.
- **Curadoria da rede da tese:** `CHAPTERS`, `TERRITORY_RULES`, `PALETTE` e
  `carve_bibliometric_territory` no topo de `rede_textual/tese_network.py`.

---

## Notas práticas

- A poda funciona **em cadeia**: frequência (`--top-n`) → peso mínimo de
  aresta (`--min-edge`) → arestas mais fortes por nó (`--edges-per-node`).
  Mexer no `--min-edge` ou `--edges-per-node` muda bastante a densidade
  visual do grafo.
- Rode sempre com **`PYTHONHASHSEED=0`**; sem isso o Louvain pode reagrupar
  de forma diferente entre execuções.
- O tamanho de cada nó reflete **exclusivamente o PageRank**; a cor reflete
  a **comunidade (Louvain)** — são camadas independentes.

> Como executar o pipeline está em [`COMO-RODAR.md`](COMO-RODAR.md).
