# Como rodar as análises e atualizar o site (manual)

Guia para regenerar **lexicometria, bibliometria, figuras e o site** sem
depender de ajuda externa. Todo o pipeline está definido em
[`.github/workflows/analyze.yml`](../.github/workflows/analyze.yml); este
documento espelha aquele fluxo.

Há **dois caminhos**: o fácil (botão no GitHub) e o completo (local).

---

## Caminho 1 — sem instalar nada (recomendado)

No GitHub: **Actions → "Analisa capítulos da tese" → Run workflow**.

Isso roda **todo** o pipeline, faz commit dos resultados e o
[`pages.yml`](../.github/workflows/pages.yml) **republica o site** sozinho.

- Campo opcional `only`: limita a capítulos (ex.: `cap1,cap2`).
- Também roda **automaticamente** todo dia às 6h17 UTC e quando a tese é
  atualizada (evento `repository_dispatch: thesis-updated`).
- A regeneração é **determinística** (`PYTHONHASHSEED=0`): se a tese não
  mudou, não há commit.

---

## Caminho 2 — rodar local, manualmente

### Pré-requisitos

- Python 3.11 e git.
- A análise lê o código-fonte `.tex` da tese, que mora em **outro
  repositório**: `julianehelanski/tecno-etnografia-centro-ia`.

### Preparação

```bash
# 1) clonar o site e a tese lado a lado (a tese vai em _tex/)
git clone https://github.com/julianehelanski/tecno-etnografia-tese-site.git
cd tecno-etnografia-tese-site
git clone https://github.com/julianehelanski/tecno-etnografia-centro-ia.git _tex

# 2) ambiente Python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3) mesma saída determinística do CI (IMPORTANTE)
export PYTHONHASHSEED=0
```

### Pipeline (na mesma ordem do CI)

```bash
# (A) LEXICOMETRIA por capítulo: análise de rede textual (co-ocorrência · NPMI · Louvain
#     · PageRank) + trajetória narrativa. Saídas em rede_textual/<cap>/
python rede_textual/run_all.py --source-root _tex            # ou: --only cap1,cap2

# (B) REDE TEXTUAL principal e injeção no mapa (index.html)
python rede_textual/tese_network.py --source-root _tex --inject index.html

# (B2) REDES POR CAPÍTULO (Louvain próprio de cada capítulo) -> seletor da capa
#      injeta <script id="netdata-chapters"> em index.html
python rede_textual/tese_network_chapters.py --source-root _tex --inject index.html

# (C) Imagens da análise -> figuras/
python rede_textual/sync_site_figuras.py

# (D) Figuras de conteúdo da tese -> figuras/
python scripts/sync_tese_figuras.py --source-root _tex

# (E) Cache-busting das figuras -> index.html
SITE_INDEX=index.html python scripts/cache_busting_figuras.py

# (F) Relatório de divergência tese <-> site
python scripts/relatorio_divergencia_tese.py --source-root _tex

# (G) Documento da tese (resumo · sumário · ilustrações · tabelas) -> index.html
python rede_textual/tese_documento.py --source-root _tex --inject index.html

# (H) Referências (bibliografia citada) -> index.html
#     lê tese.tex + tese.bib, extrai só as obras com \textcite/\parencite e
#     reinjeta o <script id="refsdata"> (seção "Referências" da aba "A tese").
python rede_textual/tese_referencias.py --source-root _tex --inject index.html
```

### Publicar (atualizar o site)

```bash
git add rede_textual/ figuras/ index.html \
        docs/divergencia-tese.md scripts/tex_structure_snapshot.json
git commit -m "Regenera redes + figuras/keywords a partir da tese"
git push        # o push na main dispara o pages.yml e republica o site
```

---

## Onde fica cada "análise"

| Análise | Script | Observação |
|---|---|---|
| **Lexicométrica** (rede de termos) | `rede_textual/tese_network.py` (mapa) e `rede_textual/run_all.py` → `rede_textual_capitulo.py` (por capítulo) | núcleo do site |
| **Bibliométrica** (CAPES/SciELO) | as figuras (`figuras/cap2/cap2-bib-*`) são geradas no **repositório da tese** e só **sincronizadas** aqui por `scripts/sync_tese_figuras.py`; o agrupamento "Bibliometria · panorama do campo" é curado em `tese_network.py` (`carve_bibliometric_territory`) | a geração dos gráficos bibliométricos está no repo `.tex`, não aqui |
| **Trajetória narrativa** | `rede_textual/narrative_trajectory.py` (via `run_all.py`) | alluvial / gantt / semântico |
| **Atualização do site** | injeção via `--inject` + `git push` → `pages.yml` | deploy automático |

> Parâmetros exatos do pipeline (janela, poda, PageRank, Louvain) em [`PARAMETROS.md`](PARAMETROS.md). Visão geral didática em [`VISAO-GERAL.md`](VISAO-GERAL.md).

---

## Caminho 3 — Anaconda / Spyder

Os scripts são ferramentas de linha de comando (`argparse`). Em IDEs como o
Spyder isso exige passar argumentos e fixar o `PYTHONHASHSEED`. O modo mais
simples é o **Anaconda Prompt**; o Spyder funciona com alguns ajustes.

### Ambiente conda (uma vez)

```bash
conda create -n tese python=3.11
conda activate tese

git clone https://github.com/julianehelanski/tecno-etnografia-tese-site.git
cd tecno-etnografia-tese-site
git clone https://github.com/julianehelanski/tecno-etnografia-centro-ia.git _tex

pip install -r requirements.txt

# determinismo: grava a variável no próprio env (precisa existir ANTES de o
# Python iniciar — definir dentro do script não funciona)
conda env config vars set PYTHONHASHSEED=0
conda activate tese      # reativar para a variável valer
```

### A) Anaconda Prompt (recomendado)

Com o env `tese` ativo e dentro da pasta do repositório, use os mesmos
comandos da seção "Pipeline" acima (`python rede_textual/run_all.py
--source-root _tex`, etc.). Publicar = `git push` no final.

### B) Spyder

1. **Abrir o Spyder do env certo:** `conda activate tese` e então `spyder`
   (ou em *Tools → Preferences → Python interpreter*, apontar para o
   `python` do env `tese`).
2. **Working directory:** defina a raiz do repositório (canto superior
   direito), para `_tex`, `index.html` etc. resolverem certo.
3. **Passar argumentos** — pelo console IPython com `%run`:
   ```python
   %run rede_textual/run_all.py --source-root _tex
   %run rede_textual/tese_network.py --source-root _tex --inject index.html
   %run rede_textual/sync_site_figuras.py
   %run scripts/sync_tese_figuras.py --source-root _tex
   %run rede_textual/tese_documento.py --source-root _tex --inject index.html
   ```
   Cache-busting das figuras (usa a variável `SITE_INDEX`):
   ```python
   import os; os.environ["SITE_INDEX"] = "index.html"
   %run scripts/cache_busting_figuras.py
   ```
   (Alternativa: *Run → Configuration per file* → campo "Command line
   options" com os argumentos, e rodar pelo botão ▶.)
4. **Conferir o determinismo:**
   ```python
   import os; print(os.environ.get("PYTHONHASHSEED"))   # tem que imprimir 0
   ```
   Se vier `None`, feche o Spyder, rode `conda activate tese` e reabra (a
   variável só entra ao iniciar o kernel).
5. **Publicar:** o Spyder não faz `git push` — use o terminal ou o GitHub
   Desktop.

### C) Jupyter Notebook / Lab

Cada passo numa célula, com `!` (subprocesso), prefixando a variável:

```python
# Windows:
!set PYTHONHASHSEED=0 && python rede_textual/run_all.py --source-root _tex
# macOS/Linux:
!PYTHONHASHSEED=0 python rede_textual/run_all.py --source-root _tex
```

### Resumo das diferenças

| | Anaconda Prompt | Spyder | Jupyter |
|---|---|---|---|
| Passar `--args` | direto | `%run script.py --args` ou Run config | `!python script.py --args` |
| `PYTHONHASHSEED=0` | `conda env config vars set` | idem (reabrir Spyder) | prefixar na célula |
| `git push` (publicar) | sim | não (terminal/GitHub Desktop) | `!git push` |

---

## Dois pontos importantes

- **Determinismo:** use sempre `PYTHONHASHSEED=0` (como o CI). Sem isso, a
  saída pode variar e gerar diffs espúrios.
- **O que NÃO é gerado por script:** textos dos nós, ligações editoriais
  entre capítulos, seções escritas à mão — e os ajustes visuais do site
  (cores, capa, fontes, responsividade, QR). Isso é edição direta no
  arquivo `index.html`. O pipeline acima regenera
  **dados e figuras**, preservando o restante.

> Veja também [`scripts/README.md`](../scripts/README.md) e
> [`rede_textual/README.md`](../rede_textual/README.md) para detalhes de cada
> utilitário.
