# scripts/

Utilitários para manter o site (`index.html`) sincronizado com a tese.

- **`sync_tese_figuras.py`** — copia para `figuras/` as figuras de conteúdo
  geradas no repositório da tese (`--source-root`).
- **`cache_busting_figuras.py`** — atualiza os sufixos `?v=` das imagens em
  `index.html` para os bytes reais, forçando o GitHub Pages a baixar as
  versões novas (página alvo via env `SITE_INDEX`, padrão `index.html`).
- **`relatorio_divergencia_tese.py`** — gera `docs/divergencia-tese.md`
  comparando seções/figuras da tese com o que o site exibe.
- **`renomear_figuras_tese.py`** — utilitário de renomeação de figuras.

> O resto do site (nós, links entre capítulos, textos dos nós, seções, e os
> arrays de figuras por capítulo) é editorial e não é gerado por script —
> atualizo-o com o Claude quando a estrutura da tese muda.
