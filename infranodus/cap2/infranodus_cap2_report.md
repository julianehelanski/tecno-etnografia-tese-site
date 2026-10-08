# Análise de rede textual — Capítulo 2

> Análise de rede textual (*text network analysis*, Paranyushkin 2019)
> aplicada ao arquivo `ex_cap2.tex`. O texto foi limpo de comandos LaTeX,
> citações e notas de rodapé foram reincorporadas; janela deslizante de
> 4 *tokens* com pesos decrescentes pela distância (3-2-1). Comunidades
> detectadas por Louvain ponderado. Esta versão acrescenta duas métricas
> *informativas* que não dependem da frequência bruta: **PageRank** dos
> nós e **NPMI** das arestas. As métricas baseadas em frequência são
> mantidas em paralelo, para comparação.

## 1. Resumo quantitativo
- Tokens significativos: **28,378**
- Grafo bruto: **7056** nós · **66548** arestas
- Grafo analítico (top 180 nós, peso ≥ 2, maior componente): **180** nós · **3617** arestas
- Tópicos detectados (Louvain): **8**

## 2. Conceitos mais influentes (degree ponderado · *baseline* frequentista)
| # | termo | grau ponderado |
|---|-------|----------------|
| 1 | `artificial` | 1861 |
| 2 | `inteligencia` | 1844 |
| 3 | `latour` | 1156 |
| 4 | `militar` | 1089 |
| 5 | `ciencia` | 1016 |
| 6 | `rotulo` | 861 |
| 7 | `rede` | 817 |
| 8 | `analise` | 806 |
| 9 | `vocabulario` | 769 |
| 10 | `campo` | 675 |
| 11 | `humano` | 671 |
| 12 | `figuracao` | 610 |
| 13 | `rotulos` | 564 |
| 14 | `aime` | 564 |
| 15 | `teoria` | 535 |
| 16 | `catalogo` | 517 |
| 17 | `ocorrencias` | 501 |
| 18 | `tecnologia` | 501 |
| 19 | `science` | 491 |
| 20 | `tecnociencia` | 475 |
| 21 | `ator` | 466 |
| 22 | `action` | 465 |
| 23 | `descreve` | 456 |
| 24 | `objeto` | 455 |
| 25 | `leitura` | 443 |
| 26 | `obras` | 436 |
| 27 | `partir` | 436 |
| 28 | `figuracoes` | 428 |
| 29 | `dado` | 417 |
| 30 | `capes` | 410 |

## 3. Conceitos mais influentes (PageRank · centralidade na rede)
PageRank pondera a importância de um nó pela importância dos seus
vizinhos. Termos pouco frequentes mas bem posicionados na rede sobem;
termos frequentes mas perifericamente conectados descem.

| # | termo | PageRank |
|---|-------|----------|
| 1 | `artificial` | 0.0319 |
| 2 | `inteligencia` | 0.0317 |
| 3 | `latour` | 0.0211 |
| 4 | `militar` | 0.0186 |
| 5 | `ciencia` | 0.0183 |
| 6 | `rede` | 0.0154 |
| 7 | `rotulo` | 0.0152 |
| 8 | `analise` | 0.0152 |
| 9 | `vocabulario` | 0.0139 |
| 10 | `campo` | 0.0130 |
| 11 | `humano` | 0.0124 |
| 12 | `figuracao` | 0.0113 |
| 13 | `aime` | 0.0107 |
| 14 | `rotulos` | 0.0105 |
| 15 | `catalogo` | 0.0098 |
| 16 | `teoria` | 0.0098 |
| 17 | `tecnologia` | 0.0097 |
| 18 | `tecnociencia` | 0.0095 |
| 19 | `ocorrencias` | 0.0092 |
| 20 | `descreve` | 0.0090 |
| 21 | `leitura` | 0.0089 |
| 22 | `science` | 0.0089 |
| 23 | `objeto` | 0.0088 |
| 24 | `partir` | 0.0088 |
| 25 | `dado` | 0.0088 |
| 26 | `ator` | 0.0087 |
| 27 | `obras` | 0.0086 |
| 28 | `figuracoes` | 0.0084 |
| 29 | `action` | 0.0084 |
| 30 | `capes` | 0.0082 |

## 4. Termos mais subvalorizados pela frequência (degree → PageRank)
Diferença de posição (rank por degree) − (rank por PageRank). Valor
positivo = o termo é *mais central na rede* do que sugere sua frequência.

| # | termo | degree-rank | pagerank-rank | salto |
|---|-------|-------------|----------------|-------|
| 1 | `press` | 154 | 96 | +58 |
| 2 | `university` | 168 | 121 | +47 |
| 3 | `traducao` | 135 | 111 | +24 |
| 4 | `joler` | 161 | 140 | +21 |
| 5 | `crawford` | 176 | 155 | +21 |
| 6 | `quadro` | 85 | 71 | +14 |
| 7 | `brasileira` | 84 | 72 | +12 |
| 8 | `cadeia` | 88 | 78 | +10 |
| 9 | `brasil` | 119 | 110 | +9 |
| 10 | `modelo` | 59 | 51 | +8 |
| 11 | `producao` | 57 | 50 | +7 |
| 12 | `forsythe` | 130 | 123 | +7 |
| 13 | `conhecimento` | 37 | 31 | +6 |
| 14 | `pesquisa` | 39 | 34 | +5 |
| 15 | `scielo` | 50 | 45 | +5 |

## 5. Pontes conceituais (betweenness — termos que costuram tópicos)
| # | termo | betweenness |
|---|-------|-------------|
| 1 | `latour` | 0.3180 |
| 2 | `inteligencia` | 0.1988 |
| 3 | `artificial` | 0.1957 |
| 4 | `militar` | 0.1468 |
| 5 | `vocabulario` | 0.1400 |
| 6 | `ciencia` | 0.1279 |
| 7 | `rotulo` | 0.0956 |
| 8 | `analise` | 0.0923 |
| 9 | `capes` | 0.0736 |
| 10 | `rede` | 0.0714 |
| 11 | `figuracoes` | 0.0642 |
| 12 | `conceito` | 0.0621 |
| 13 | `catalogo` | 0.0609 |
| 14 | `campo` | 0.0582 |
| 15 | `teoria` | 0.0499 |
| 16 | `aime` | 0.0493 |
| 17 | `descreve` | 0.0475 |
| 18 | `figuracao` | 0.0464 |
| 19 | `tecnociencia` | 0.0456 |
| 20 | `humano` | 0.0402 |

## 6. Pares de termos com associação mais surpreendente (NPMI)
NPMI mede *quão surpreendente* é a co-ocorrência de duas palavras dadas
suas frequências individuais. Diferente do peso bruto, ele faz aparecer
pares semanticamente fortes mesmo quando os termos co-ocorrem poucas
vezes.

| # | termo A | termo B | NPMI | co-ocorr. (peso) |
|---|---------|---------|------|------------------|
| 1 | `laboratory` | `life` | 0.872 | 109 |
| 2 | `hope` | `pandora` | 0.869 | 123 |
| 3 | `inteligencia` | `artificial` | 0.828 | 819 |
| 4 | `press` | `university` | 0.818 | 64 |
| 5 | `taxa` | `interna` | 0.803 | 54 |
| 6 | `action` | `science` | 0.790 | 171 |
| 7 | `crawford` | `joler` | 0.740 | 41 |
| 8 | `quadro` | `conclusao` | 0.722 | 62 |
| 9 | `mediacao` | `tecnica` | 0.714 | 96 |
| 10 | `maquina` | `aprendizado` | 0.711 | 126 |
| 11 | `teoria` | `ator` | 0.705 | 152 |
| 12 | `textil` | `topologico` | 0.644 | 46 |
| 13 | `lexicometrica` | `analise` | 0.618 | 95 |
| 14 | `modelo` | `linguagem` | 0.597 | 63 |
| 15 | `ator` | `rede` | 0.592 | 154 |
| 16 | `recalling` | `clarifications` | 0.572 | 27 |
| 17 | `traducao` | `brasileira` | 0.563 | 27 |
| 18 | `action` | `pandora` | 0.563 | 54 |
| 19 | `industria` | `militar` | 0.553 | 89 |
| 20 | `acesso` | `disponivel` | 0.534 | 15 |
| 21 | `stengers` | `haraway` | 0.528 | 29 |
| 22 | `vocabulario` | `topologico` | 0.519 | 58 |
| 23 | `ciencia` | `humano` | 0.517 | 177 |
| 24 | `lexical` | `catalogo` | 0.514 | 43 |
| 25 | `action` | `hope` | 0.512 | 40 |

## 7. Tópicos latentes (comunidades Louvain)
- **Tópico 1** (45 termos): leitura, obras, dado, capes, artigos, distribuicao
- **Tópico 2** (41 termos): latour, militar, rotulo, vocabulario, figuracao, aime
- **Tópico 3** (26 termos): ciencia, campo, humano, tecnologia, antropologia, conhecimento
- **Tópico 4** (24 termos): artificial, inteligencia, objeto, pesquisa, maquina, conceito
- **Tópico 5** (22 termos): rede, teoria, tecnociencia, ator, descreve, pratica
- **Tópico 6** (15 termos): analise, partir, figuracoes, secao, haraway, lexicometrica
- **Tópico 7** (5 termos): quadro, modos, conclusao, investigacao, grupo
- **Tópico 8** (2 termos): joler, crawford

## 8. Lacunas estruturais (pares de tópicos fracamente conectados)
Lacunas estruturais sinalizam *espaços de ideia* pouco articulados no
texto — candidatos a aprofundamento argumentativo.

- Lacuna entre **Tópico 2** [latour, militar, rotulo] e **Tópico 4** [artificial, inteligencia, objeto] — densidade ponderada de ligação = 0.4644
- Lacuna entre **Tópico 1** [leitura, obras, dado] e **Tópico 5** [rede, teoria, tecnociencia] — densidade ponderada de ligação = 0.4646
- Lacuna entre **Tópico 2** [latour, militar, rotulo] e **Tópico 3** [ciencia, campo, humano] — densidade ponderada de ligação = 0.4972
- Lacuna entre **Tópico 1** [leitura, obras, dado] e **Tópico 2** [latour, militar, rotulo] — densidade ponderada de ligação = 0.8244
- Lacuna entre **Tópico 1** [leitura, obras, dado] e **Tópico 3** [ciencia, campo, humano] — densidade ponderada de ligação = 0.8906
- Lacuna entre **Tópico 1** [leitura, obras, dado] e **Tópico 4** [artificial, inteligencia, objeto] — densidade ponderada de ligação = 0.9250

## 9. Leitura interpretativa
**O que a rede mostra.** O capítulo trama três vocabulários. O primeiro é
a leitura conceitual das *figurações* em Latour, cujos próprios livros
aparecem como duplas de altíssima associação (NPMI): `laboratory ↔ life`,
`hope ↔ pandora`, `science ↔ action` — *Laboratory Life*, *A Esperança de
Pandora* e *Science in Action* condensados em pares lexicais. O segundo é a
genealogia militar-industrial da IA (`militar`, `industria`, `inteligencia`,
`artificial`). O terceiro é o panorama bibliométrico do campo brasileiro
(`capes`, `scielo`, `producao`, `obras`, `dado`).

**Pontes (`betweenness`).** `latour` é a grande ponte do capítulo
(betweenness 0,33), seguido de `inteligencia`, `artificial`, `ciencia`,
`militar` e `vocabulario`: são os termos que costuram a teoria às
descrições. Que `vocabulario` apareça como ponte é coerente com o gesto do
capítulo, que é ele mesmo um exercício de vocabulário — as figurações.

**Lacunas a desenvolver.** As ligações mais fracas estão entre o tópico
bibliométrico (`obras`, `dado`, `capes`) e o tópico das obras de Latour
lidas no original (`science`, `action`, `pandora`, `hope`); e entre o tópico
da IA (`artificial`, `inteligencia`) e essas mesmas obras. O mapeamento
quantitativo do campo e a leitura cerrada das figurações correm em paralelo
sem se costurarem — um convite a explicitar como a análise lexicométrica das
obras conversa com o panorama bibliométrico do campo.

## 10. Arquivos gerados
**Visões frequentistas**
- `infranodus_cap2_network.png` — rede completa, tamanho por degree.
- `infranodus_cap2_focus.png` — núcleo (top-100, peso ≥ 3).

**Visões informativas**
- `infranodus_cap2_pmi.png` — rede completa, tamanho por **PageRank**,
  arestas filtradas por **NPMI ≥ 0,20**.
- `infranodus_cap2_focus_pmi.png` — núcleo, NPMI ≥ 0,25.

**Dados**
- `infranodus_cap2_metrics.json` — métricas brutas (degree, betweenness,
  PageRank, NPMI, comunidades, lacunas).
- `infranodus_cap2.gexf` / `infranodus_cap2_focus.gexf` — grafos para Gephi
  já com `community`, `frequency`, `degree_weighted`, `betweenness`,
  `pagerank` (nós) e `weight`, `npmi` (arestas).
- `infranodus_cap2_nodes.csv` / `infranodus_cap2_edges.csv` (e `_focus_*`)
  — fallback em planilha; CSVs trazem todas as colunas acima.

## 11. Como abrir no Gephi
1. Instale Gephi (≥ 0.10): https://gephi.org/users/download/
2. `File → Open…` → selecione `infranodus_cap2.gexf` (ou `_focus.gexf`).
3. No painel **Appearance**: já vem com cor por `community` e tamanho por
   `degree_weighted` (embutidos via atributos `viz`). Ajuste se quiser.
4. Em **Layout**: aplique *ForceAtlas 2* (ative *Prevent Overlap* e
   *Dissuade Hubs*) por ~30 s; ou *Fruchterman-Reingold* para algo mais rápido.
5. Em **Statistics**: rode *Modularity* e *Average Path Length* se quiser
   recalcular comunidades dentro do Gephi (resultados serão semelhantes).
6. Em **Preview**: ative *Node Labels*, escolha fonte e exporte para PDF/SVG.
