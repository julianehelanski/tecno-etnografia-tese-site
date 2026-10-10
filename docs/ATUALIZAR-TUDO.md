# Atualizar todas as análises (esquema por pasta)

Colinha para entrar em **cada repositório** e regerar suas análises. Cada
projeto é independente: rode sempre **dentro da pasta dele** (os caminhos
são relativos) e publique por repositório (`git add -A ; git commit ; git push`).

> Caminhos assumem as pastas no Desktop (Windows/PowerShell). Ajuste se as
> suas estiverem em outro lugar. Em macOS/Linux, troque `\` por `/` e
> `$env:VAR = "x"` por `export VAR=x`.

---

## 1) SITE — rede textual (lexicométrica)
📁 `tecno-etnografia-tese-site`

```powershell
cd C:\Users\julia\Desktop\tecno-etnografia-tese-site
$env:PYTHONHASHSEED = "0"
$tese = "..\tecno-etnografia-centro-ia"

python rede_textual\run_all.py --source-root $tese            # PNGs por capítulo
python rede_textual\tese_network.py --source-root $tese --inject index.html  # mapa
python rede_textual\tese_documento.py --source-root $tese --inject index.html # resumo·sumário
python rede_textual\tese_referencias.py --source-root $tese --inject index.html # referências citadas

git add -A ; git commit -m "Atualiza análise textual" ; git push   # publica o site
```
➡️ Atualiza o site (mapa + figuras). O `push` republica online via GitHub Pages.
Detalhes: [`COMO-RODAR.md`](COMO-RODAR.md) · parâmetros: [`PARAMETROS.md`](PARAMETROS.md).

---

## 2) BIBLIOMETRIA C4AI — co-palavras das publicações
📁 `bibliometria-publicacoes-c4ai`

O `coword_analysis.py` é quem **gera os gráficos**, lendo `c4ai_publicacoes.xlsx`
(407 publicações, curadoria manual). O enriquecimento via OpenAlex
(`enrich_metadata.py`) é **opcional** — melhora os termos (usa abstracts/keywords
em vez de só títulos).

**Atualização recomendada (termos mais ricos):**
```powershell
cd C:\Users\julia\Desktop\bibliometria-publicacoes-c4ai
python preparar_base.py                          # _manual.xlsx -> c4ai_publicacoes.xlsx
python enrich_metadata.py --email seu@email.com  # opcional; OpenAlex (internet) -> _enriquecido.xlsx
python coword_analysis.py --input c4ai_publicacoes_enriquecido.xlsx
```

**Versão mínima (só títulos, sem internet):**
```powershell
python preparar_base.py
python coword_analysis.py                        # usa c4ai_publicacoes.xlsx (títulos)
```

**Re-coletar a lista do site do C4AI (opcional, precisa internet):**
```powershell
python scrape_c4ai.py    # Excel bruto; depois há curadoria manual -> c4ai_publicacoes_manual.xlsx
```
➡️ Saídas em `output/coword/` (PNGs `10_`/`11_`, `rede_coword_interativa.html`, planilhas `.xlsx`).

⚡ **Atalho:** salve o `run_coword.py` na raiz do repo e rode `python run_coword.py` (use `--email voce@x.com` para enriquecer, `--scrape` para recoletar).

---

## 3) BIBLIOMETRIA IA-HUMANAS — CAPES / SciELO / OpenAlex
📁 `bibliometria-ia-humanas`

```powershell
cd C:\Users\julia\Desktop\bibliometria-ia-humanas
pip install -r requirements.txt          # só na primeira vez

# CAPES (precisa dos 4 XLSX em dados_capes/ — se for Git LFS: git lfs pull)
python analise_capes_2021_2024.py
python figuras_capes_2021_2024.py
python analise_capes_humanas.py

# SciELO (precisa de internet)
python analise_scielo_articlemeta.py
python figuras_scielo_articlemeta.py

# OpenAlex (internet + seu e-mail)
python analise_openalex.py --modo agregado --mailto SEU_EMAIL@exemplo.com
python figuras_openalex.py

# comparativo final (depois de CAPES + SciELO)
python analise_comparativa_2026.py
```
➡️ Gera tudo em `figuras/`. Regra: `analise_*` **antes** do `figuras_*`;
comparativo **por último**. Versões antigas (`analise_scielo.py`,
`analise_capes.py`, `analise_comparativa.py`) são o recorte histórico.

⚡ **Atalho:** salve o `run_bibliometria.py` na raiz do repo e rode `python run_bibliometria.py` (CAPES + SciELO + comparativo; `--mailto voce@x.com` inclui OpenAlex; `--fontes capes` roda uma base).

---

## 4) FIGURAÇÕES — Latour × Haraway (Cap. 2)
📁 `analise_figuracoes`  ·  scripts numerados em `scripts/` (01→23)

Projeto em **etapas** (Etapa 1: livros · Etapa 2/2-bis: artigos · Etapa 3:
AIME · refinamento). Roda-se **em ordem numérica**, mas **não é um “run all”
cego**: alguns passos geram planilhas que **você preenche à mão** antes do
passo seguinte. A ordem canônica completa está em `plano_de_trabalho.md` e
`docs/decisoes_metodologicas.md` do próprio repo.

Preparação:
```powershell
cd C:\Users\julia\Desktop\analise_figuracoes
pip install -r requirements.txt          # 1ª vez
$env:PYTHONHASHSEED = "0"
```

**Núcleo que regenera figuras/tabelas a partir do texto já commitado**
(`corpus/txt_norm/`) — pode rodar direto:
```powershell
# Etapa 1 (livros)
python scripts\02_kwic.py
python scripts\03_frequencies.py
python scripts\04_visualizations.py     # figuras
python scripts\05_cooccurrence.py       # rede
python scripts\07_trajectory.py
# Refinamento (passagens + gráficos do Cap. 2)
python scripts\10_passo4_kwic_ampliado.py
python scripts\11_passo4_graficos.py    # figuras
# Etapa 2 (artigos)
python scripts\13_audit_articles_etapa2.py
python scripts\14_etapa2_tabela_comparativa.py
python scripts\15_etapa2_desambiguar_militar.py
python scripts\16_etapa2_cocorrencia_comparacao.py
python scripts\17_etapa2_tabelas_finais.py
python scripts\20_etapa2bis_tabela_5_obras.py
# Etapa 3 (AIME)
python scripts\22_etapa3_aime_pipeline.py
python scripts\23_etapa3_aime_visualizacoes.py   # figuras
```
➡️ Saídas em `outputs/<obra>/` (`csv/`, `figuras/`, `relatorios/`) e em
`outputs/etapa2_artigos/`, `outputs/passo4/` etc.

**Passos com PDF ou preenchimento manual (só quando precisar):**
- `01_extract_text.py` + `01b_normalize_text.py` → re-extraem do PDF (precisam dos PDFs + `.env`); o texto normalizado já está commitado, então normalmente **pule**.
- `06_sampling.py`, `08_validate_sample.py`, `18_…`, `19_…`, `21_…` → **validação amostral**: geram/consomem planilhas que **você codifica à mão** (ex.: `19` precisa do `..._PREENCHIDA.csv`). Siga a ordem da Etapa no `plano_de_trabalho.md`.

⚡ **Atalho:** salve o `run_nucleo_figuracoes.py` na raiz do repo e rode `python run_nucleo_figuracoes.py` (roda só o núcleo automático; `--listar` mostra a sequência, `--only 02,03,04,05,07,10,11` roda o núcleo seguro do Cap. 2).

---

## 🔑 Regras de ouro (valem para as 4)

1. **Rode dentro da pasta do próprio repositório** (os caminhos são relativos).
2. **`analise_*` / `0X` vêm antes** dos passos que desenham (figuras/visualizações).
3. **Publicar é por repositório:** `git add -A ; git commit -m "..." ; git push`.
4. **1ª vez em cada repo:** `pip install -r requirements.txt` (se houver).
5. **Determinismo:** `$env:PYTHONHASHSEED = "0"` antes de rodar (importa
   sobretudo no site, por causa do Louvain).

---

## Mundos separados (importante)

- O botão **"Run workflow" do GitHub Actions** atualiza **apenas o site**
  (análise lexicométrica). Os três repositórios de bibliometria/figurações
  são independentes e **não** têm essa automação — cada um se roda por si.
- As figuras geradas nos repositórios de bibliometria/figurações entram na
  tese/site por um passo **manual** de cópia (não automático).
