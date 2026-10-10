# Visão geral: do automático ao manual

Resumo didático de como as análises que hoje rodam **automaticamente**
(Overleaf + GitHub + site) podem ser reproduzidas **à mão** em outros
programas. Para o passo a passo detalhado, veja
[`COMO-RODAR.md`](COMO-RODAR.md) e [`PARAMETROS.md`](PARAMETROS.md).

Pense no que está montado como uma **esteira automática** com três
estações — e cada uma tem um equivalente "feito à mão".

## As 3 peças automáticas

1. **Overleaf** → onde a tese é *escrita* em LaTeX. É a **fonte** do texto.
2. **GitHub (Actions)** → o "robô" que, quando a tese muda, **roda a
   análise** (rede de termos, palavras-chave, figuras).
3. **Site (GitHub Pages)** → **publica** o resultado: a rede textual no
   navegador.

Fluxo: **escrever (Overleaf) → analisar (GitHub) → publicar (site)**.

## Cada estação, manualmente

| Estação | Automático hoje | Equivalente manual |
|---|---|---|
| **Ter o texto** | Overleaf | Qualquer editor LaTeX (TeXstudio, VS Code, Kile) — ou só os arquivos `.tex` como texto puro. *A análise só lê o texto; não precisa compilar o PDF.* |
| **Rodar a análise** | GitHub Actions | **Python** no seu computador: Anaconda Prompt, **Spyder**, Jupyter ou terminal (scripts em `rede_textual/` e `scripts/`). |
| **Ver / publicar** | GitHub Pages | Abrir o `index.html` no navegador (duplo-clique) para ver; `git push` (ou GitHub Desktop) para publicar. |

## O mínimo a fazer à mão

1. **Dois ingredientes na mesma pasta:** os scripts (este repositório) e o
   texto da tese (pasta `_tex`).
2. **Instalar o Python uma vez** (Anaconda) + bibliotecas
   (`pip install -r requirements.txt`).
3. **Rodar os dois comandos principais:**
   - `python rede_textual/run_all.py --source-root _tex` → análise por capítulo;
   - `python rede_textual/tese_network.py --source-root _tex --inject index.html`
     → a rede do mapa, já colocada no site.
4. **Ver:** abrir o `index.html` no navegador.
5. **(Opcional) Publicar:** `git push`.

## Três ideias-chave

- **A automação não faz mágica nova** — ela só roda sozinha os mesmos
  scripts Python que você pode rodar à mão. Tirar o "robô" do meio não muda
  o resultado.
- **Sempre use `PYTHONHASHSEED=0`** antes de rodar: garante que a análise dê
  **sempre o mesmo resultado** (senão o agrupamento de comunidades pode
  variar).
- **Duas camadas:** o que é **gerado por script** (rede, contagens, figuras)
  e o que é **escrito à mão** (textos, cores, layout). A reprodução manual
  recria a primeira; a segunda é edição direta nos arquivos `.html`.
