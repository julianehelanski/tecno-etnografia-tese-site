# Linhas do tempo (roadmaps de capítulo) — padrão de estilo

Cada capítulo da tese pode abrir (ou fechar) com uma **linha do tempo**: um
diagrama temporal (Mermaid `gantt`) que dispõe marcos, durações e rupturas sobre
um eixo de anos. É o par cronológico do **texto-mapa** (ver `../mapas/`): onde o
mapa relaciona elementos numa superfície, a linha do tempo os ordena no tempo.

O padrão é único para que a banca aprenda o código **uma vez** e ele valha para
todos os capítulos. Editáveis no [MermaidChart](https://www.mermaidchart.com/).

## Arquivos

- `linha-do-tempo-capitulo{N}.mmd` — código-fonte Mermaid (versionado, editável).
- `linha-do-tempo-capitulo{N}.svg` — exportação vetorial (backup offline + PDF).
- Versão interativa (pan/zoom, para a defesa): publicada no MermaidChart. O link
  **vive na própria tese** — basta pôr um `\href{https://mermaid.ai/d/...}{...}`
  na legenda (`\caption`) da figura. O gerador `rede_textual/tese_documento.py`
  extrai esse link para `DOC.figuras[].link` e o site acende sozinho o selinho
  "ver diagrama ↗" na lista de ilustrações (sem manter URL à mão no site).

## Cabeçalho-padrão (idêntico em todos)

```yaml
---
config:
  theme: base
  themeVariables:
    fontFamily: "Helvetica Neue, Arial, sans-serif"
    primaryColor: '#f8fafc'
    primaryTextColor: '#374151'
    primaryBorderColor: '#9ca3af'
    lineColor: '#6b7280'
    secondaryColor: '#e5e7eb'
    tertiaryColor: '#f3f4f6'
    taskBkgColor: '#f1f5f9'
    taskBorderColor: '#94a3b8'
    taskTextColor: '#374151'
    doneTaskBkgColor: '#ede9fe'
    doneTaskBorderColor: '#7c3aed'
    activeTaskBkgColor: '#dbeafe'
    activeTaskBorderColor: '#3b82f6'
    critBkgColor: '#fee2e2'
    critBorderColor: '#dc2626'
    gridColor: '#e5e7eb'
    todayLineColor: '#6b7280'
    sectionBkgColor: '#fafafa'
    altSectionBkgColor: '#f5f5f5'
---
gantt
    dateFormat YYYY-MM-DD
    axisFormat %Y
    todayMarker off
```

> Mesma família tipográfica dos texto-mapas (Helvetica/Arial sem serifa, em
> contraste com o corpo serifado da tese). `todayMarker off` porque a tese é um
> recorte fechado no tempo — não queremos a linha do "hoje" atravessando o gráfico.
> `axisFormat %Y` mantém o eixo em anos, legível mesmo em recortes longos.

## O código de estado (cor = situação do evento no tempo)

Ao contrário do texto-mapa — onde a cor indica o **tipo** de elemento (eixo,
teoria, campo, inscrição, dobra) — na linha do tempo a cor indica o **estado
temporal** do evento. São códigos distintos e propositais: o mapa é temático, a
linha do tempo é cronológica.

| Marcação Mermaid | Aparência | Significado |
|---|---|---|
| `:milestone` (`0d`) | losango cinza-ardósia | **marco** — evento pontual datado |
| `:active`            | barra azul            | **em curso** — processo aberto, ainda não estabilizado (ex.: observação participante) |
| `:done`              | barra roxa            | **concluído/estabilizado** — fase encerrada com êxito |
| `:crit`              | barra vermelha        | **ruptura/tensão** — encerramento, eliminação, não renovação |
| (padrão)             | barra cinza-clara     | duração neutra, sem estado marcado |

Nem todo estado aparece em toda linha do tempo (a ausência de uma cor é
informativa, como nos mapas). A legenda permanece a mesma.

## Legenda

O `gantt` não embute uma legenda como o `flowchart` dos texto-mapas. Por isso a
legenda do código de cores vai na **legenda da figura** (caption) e neste README.
Texto sugerido para o caption:

> Losango = marco pontual · barra azul = processo em curso · barra roxa =
> fase concluída · barra vermelha = ruptura institucional.

## Seções (`section`)

Agrupam os eventos por camada de análise, não por estado. No cap. 3:
`Histórica` (genealogia IBM, 1890–2019), `Institucional` (C4AI-IBM, 2016–2025) e
`Pesquisa de campo` (trabalho de campo, 2022–2025). Cada capítulo nomeia suas
próprias seções conforme o material.

## Convenções de redação

- Rótulo no formato `Descrição do evento · data por extenso` — a data textual
  duplica a posição no eixo e sobrevive à exportação em preto e branco.
- IDs curtos e estáveis por seção (`h01`, `i01`, `c01`…) para facilitar edição.
- Marcos pontuais usam duração `0d` (`:milestone`); processos usam data de início
  e fim (`2022-03-01, 2025-12-31`) ou duração (`90d`).

## Fluxo de trabalho

1. Editar o `.mmd` ou colar no MermaidChart.
2. No MermaidChart: publicar e pôr o link no `\href{...}` da legenda da figura,
   na própria tese (`.tex`). O site lê esse link sozinho na próxima regeneração.
3. Exportar SVG → salvar aqui como `linha-do-tempo-capituloN.svg` (backup/PDF).
4. Todo diagrama com link mostra o mesmo selinho "ver diagrama ↗" na lista de
   ilustrações. O título "Mapa do capítulo capituloN" também alimenta o botão
   "abrir o mapa do capítulo" no card do capítulo.
