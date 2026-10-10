# Mapas-capítulo (texto-mapas) — padrão de estilo

Os "texto-mapas" que abrem cada capítulo da tese seguem um padrão único,
para que a banca aprenda o código de cores **uma vez** e ele valha para os
quatro capítulos. Editáveis no [MermaidChart](https://www.mermaidchart.com/).

## Arquivos

- `mapa-capitulo{1..4}.mmd` — código-fonte Mermaid (versionado, editável).
- `mapa-capitulo{1..4}.svg` — exportação vetorial (backup offline + versão impressa/PDF).
- Versão interativa (pan/zoom, para a defesa): publicada no MermaidChart. O link
  **vive na própria tese** — um `\href{https://mermaid.ai/d/...}{...}` na legenda
  (`\caption`) da figura. O gerador `rede_textual/tese_documento.py` o extrai para
  `DOC.figuras[].link`; o site acende o selinho "ver diagrama ↗" na lista de
  ilustrações e o botão "abrir o mapa do capítulo" no card do capítulo
  (sumário da aba "tese"). O card identifica o mapa do capítulo pelo título
  "Mapa do capítulo capituloN".

## Cabeçalho-padrão (idêntico em todos)

```yaml
---
config:
  layout: elk
  look: classic
  theme: base
  themeVariables:
    fontFamily: "Helvetica Neue, Arial, sans-serif"
    fontSize: 15px
    lineColor: '#6b7280'
    primaryTextColor: '#1a1a1a'
---
```

> Corpo da tese em serifada + figuras em sans-serif (Helvetica/Arial) é a
> combinação clássica. Helvetica/Arial embute no PDF sem risco de fallback.

## As 5 classes semânticas (cor = tipo de elemento, não seção)

```
classDef eixo      fill:#EEF1F4,stroke:#37474F,stroke-width:3px,color:#22303a;
classDef teoria    fill:#DCE7F5,stroke:#2E5A87,stroke-width:2px,color:#14304a;
classDef campo     fill:#DDEEDD,stroke:#3F7A3F,stroke-width:2px,color:#1e3a1e;
classDef inscricao fill:#FBEFD0,stroke:#B5860A,stroke-width:2px,color:#5a4205;
classDef dobra     fill:#E8E0F0,stroke:#6A4C93,stroke-width:2px,color:#3a2a52;
```

| Classe | Significado |
|---|---|
| `eixo` | título, pergunta de abertura e cabeçalhos de seção (esqueleto) |
| `teoria` | autores, conceitos e aparato analítico |
| `campo` | material empírico: observação, entrevistas, atores, documentos |
| `inscricao` | dados produzidos: bibliometria, gráficos, espectrogramas, código, diagramas |
| `dobra` | argumento-síntese, achados interpretativos e considerações finais |

Nem toda classe aparece em todo mapa (caps. 1 e 2, teórico-metodológicos, não têm
`campo`; o cap. 4, empírico, é rico em `campo` e `inscricao`). A legenda permanece
igual mesmo assim — a ausência de uma cor é informativa.

## Legenda embutida (mesma em todos, logo após `flowchart TB`)

```
subgraph LEGENDA["<b>LEGENDA &nbsp;·&nbsp; o que cada cor indica</b>"]
    direction LR
    L1["<b>EIXO</b><br>título, pergunta<br>e cabeçalhos de seção"]:::eixo
    L2["<b>TEORIA</b><br>autores, conceitos<br>e aparato analítico"]:::teoria
    L3["<b>CAMPO</b><br>material empírico:<br>observação, entrevistas,<br>documentos"]:::campo
    L4["<b>INSCRIÇÃO</b><br>dados produzidos:<br>bibliometria, gráficos,<br>diagramas"]:::inscricao
    L5["<b>DOBRA</b><br>argumento-síntese<br>e considerações finais"]:::dobra
    L1 ~~~ L2 ~~~ L3 ~~~ L4 ~~~ L5
end
```

Âncora opcional para fixar a legenda no topo: `LEGENDA ~~~ titulo`.

## Caixas (subgraphs)

Borda neutra uniforme — a cor vem dos nós, não das caixas:

```
style <id> fill:transparent,stroke:#b8bec7,stroke-width:1px
```

(`LEGENDA` usa `fill:#fbfbfc,stroke:#9aa2ad`.)

## Fluxo de trabalho

1. Editar o `.mmd` ou colar no MermaidChart.
2. No MermaidChart: publicar (link interativo) → colar o link em `MAPAS` no `index.html`.
3. Exportar SVG → salvar aqui como `mapa-capituloN.svg` (backup offline/PDF).
