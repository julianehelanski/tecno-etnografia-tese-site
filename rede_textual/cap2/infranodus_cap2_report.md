# Análise de rede textual — Capítulo 2

> Análise de rede textual (*text network analysis*; PARANYUSHKIN, Dmitry. InfraNodus: generating insight
> using text network analysis. In: *The World Wide Web Conference (WWW '19)*. New York: ACM, 2019.
> p. 3584–3589. DOI: https://doi.org/10.1145/3308558.3314123)
> aplicada ao arquivo `ex_cap2.tex`. O texto foi limpo de comandos LaTeX,
> citações e notas de rodapé foram reincorporadas; janela deslizante de
> 4 *tokens* com pesos decrescentes pela distância (3-2-1). Comunidades
> detectadas por Louvain ponderado. Esta versão acrescenta duas métricas
> *informativas* que não dependem da frequência bruta: **PageRank** dos
> nós e **NPMI** das arestas. As métricas baseadas em frequência são
> mantidas em paralelo, para comparação.

## 1. Resumo quantitativo
- Tokens significativos: **28,404**
- Grafo bruto: **7064** nós · **66643** arestas
- Grafo analítico (top 180 nós, peso ≥ 2, maior componente): **180** nós · **3609** arestas
- Tópicos detectados (Louvain): **7**

## 2. Conceitos mais influentes (degree ponderado · *baseline* frequentista)
| # | termo | grau ponderado |
|---|-------|----------------|
| 1 | `artificial` | 1861 |
| 2 | `inteligencia` | 1844 |
| 3 | `latour` | 1155 |
| 4 | `militar` | 1086 |
| 5 | `ciencia` | 1016 |
| 6 | `rotulo` | 860 |
| 7 | `rede` | 817 |
| 8 | `analise` | 806 |
| 9 | `vocabulario` | 769 |
| 10 | `campo` | 675 |
| 11 | `humano` | 671 |
| 12 | `figuracao` | 610 |
| 13 | `rotulos` | 562 |
| 14 | `aime` | 558 |
| 15 | `teoria` | 535 |
| 16 | `catalogo` | 517 |
| 17 | `tecnologia` | 501 |
| 18 | `science` | 488 |
| 19 | `tecnociencia` | 473 |
| 20 | `ator` | 466 |
| 21 | `action` | 463 |
| 22 | `descreve` | 456 |
| 23 | `objeto` | 455 |
| 24 | `ocorrencias` | 445 |
| 25 | `leitura` | 441 |
| 26 | `partir` | 438 |
| 27 | `obras` | 431 |
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
| 4 | `militar` | 0.0187 |
| 5 | `ciencia` | 0.0184 |
| 6 | `rede` | 0.0155 |
| 7 | `rotulo` | 0.0153 |
| 8 | `analise` | 0.0152 |
| 9 | `vocabulario` | 0.0140 |
| 10 | `campo` | 0.0130 |
| 11 | `humano` | 0.0124 |
| 12 | `figuracao` | 0.0113 |
| 13 | `aime` | 0.0107 |
| 14 | `rotulos` | 0.0105 |
| 15 | `catalogo` | 0.0098 |
| 16 | `teoria` | 0.0098 |
| 17 | `tecnologia` | 0.0097 |
| 18 | `tecnociencia` | 0.0094 |
| 19 | `descreve` | 0.0090 |
| 20 | `leitura` | 0.0089 |
| 21 | `science` | 0.0089 |
| 22 | `objeto` | 0.0088 |
| 23 | `partir` | 0.0088 |
| 24 | `dado` | 0.0088 |
| 25 | `ator` | 0.0087 |
| 26 | `obras` | 0.0085 |
| 27 | `figuracoes` | 0.0085 |
| 28 | `action` | 0.0084 |
| 29 | `ocorrencias` | 0.0082 |
| 30 | `capes` | 0.0082 |

## 4. Termos mais subvalorizados pela frequência (degree → PageRank)
Diferença de posição (rank por degree) − (rank por PageRank). Valor
positivo = o termo é *mais central na rede* do que sugere sua frequência.

| # | termo | degree-rank | pagerank-rank | salto |
|---|-------|-------------|----------------|-------|
| 1 | `press` | 153 | 96 | +57 |
| 2 | `university` | 168 | 121 | +47 |
| 3 | `traducao` | 133 | 111 | +22 |
| 4 | `joler` | 160 | 139 | +21 |
| 5 | `crawford` | 176 | 155 | +21 |
| 6 | `quadro` | 85 | 70 | +15 |
| 7 | `brasileira` | 84 | 72 | +12 |
| 8 | `brasil` | 119 | 110 | +9 |
| 9 | `cadeia` | 88 | 80 | +8 |
| 10 | `modelo` | 59 | 52 | +7 |
| 11 | `conhecimento` | 37 | 31 | +6 |
| 12 | `producao` | 57 | 51 | +6 |
| 13 | `forsythe` | 129 | 123 | +6 |
| 14 | `leitura` | 25 | 20 | +5 |
| 15 | `dado` | 29 | 24 | +5 |

## 5. Pontes conceituais (betweenness — termos que costuram tópicos)
| # | termo | betweenness |
|---|-------|-------------|
| 1 | `latour` | 0.3184 |
| 2 | `inteligencia` | 0.2000 |
| 3 | `artificial` | 0.1962 |
| 4 | `militar` | 0.1461 |
| 5 | `vocabulario` | 0.1406 |
| 6 | `ciencia` | 0.1259 |
| 7 | `rotulo` | 0.0946 |
| 8 | `analise` | 0.0922 |
| 9 | `capes` | 0.0732 |
| 10 | `rede` | 0.0721 |
| 11 | `figuracoes` | 0.0641 |
| 12 | `catalogo` | 0.0625 |
| 13 | `conceito` | 0.0621 |
| 14 | `campo` | 0.0581 |
| 15 | `aime` | 0.0495 |
| 16 | `teoria` | 0.0494 |
| 17 | `descreve` | 0.0476 |
| 18 | `figuracao` | 0.0461 |
| 19 | `tecnociencia` | 0.0456 |
| 20 | `humano` | 0.0380 |

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
| 14 | `modelo` | `linguagem` | 0.598 | 63 |
| 15 | `ator` | `rede` | 0.592 | 154 |
| 16 | `recalling` | `clarifications` | 0.572 | 27 |
| 17 | `traducao` | `brasileira` | 0.563 | 27 |
| 18 | `action` | `pandora` | 0.563 | 54 |
| 19 | `industria` | `militar` | 0.553 | 89 |
| 20 | `acesso` | `disponivel` | 0.534 | 15 |
| 21 | `stengers` | `haraway` | 0.528 | 29 |
| 22 | `ocorrencias` | `palavras` | 0.521 | 58 |
| 23 | `vocabulario` | `topologico` | 0.519 | 58 |
| 24 | `ciencia` | `humano` | 0.517 | 177 |
| 25 | `lexical` | `catalogo` | 0.514 | 43 |

## 7. Tópicos latentes (comunidades Louvain)
- **Tópico 1** (45 termos): rede, teoria, tecnociencia, ator, descreve, conhecimento
- **Tópico 2** (39 termos): leitura, obras, dado, capes, artigos, distribuicao
- **Tópico 3** (35 termos): militar, rotulo, vocabulario, figuracao, rotulos, aime
- **Tópico 4** (19 termos): artificial, inteligencia, objeto, pesquisa, maquina, generativa
- **Tópico 5** (15 termos): ciencia, campo, humano, tecnologia, antropologia, estudos
- **Tópico 6** (14 termos): analise, partir, figuracoes, haraway, lexicometrica, textual
- **Tópico 7** (13 termos): latour, science, action, obra, pandora, hope

## 8. Lacunas estruturais (pares de tópicos fracamente conectados)
Lacunas estruturais sinalizam *espaços de ideia* pouco articulados no
texto — candidatos a aprofundamento argumentativo.

- Lacuna entre **Tópico 3** [militar, rotulo, vocabulario] e **Tópico 4** [artificial, inteligencia, objeto] — densidade ponderada de ligação = 0.3744
- Lacuna entre **Tópico 1** [rede, teoria, tecnociencia] e **Tópico 2** [leitura, obras, dado] — densidade ponderada de ligação = 0.4405
- Lacuna entre **Tópico 3** [militar, rotulo, vocabulario] e **Tópico 5** [ciencia, campo, humano] — densidade ponderada de ligação = 0.4514
- Lacuna entre **Tópico 1** [rede, teoria, tecnociencia] e **Tópico 3** [militar, rotulo, vocabulario] — densidade ponderada de ligação = 0.5625
- Lacuna entre **Tópico 2** [leitura, obras, dado] e **Tópico 3** [militar, rotulo, vocabulario] — densidade ponderada de ligação = 0.8894
- Lacuna entre **Tópico 1** [rede, teoria, tecnociencia] e **Tópico 5** [ciencia, campo, humano] — densidade ponderada de ligação = 1.0267

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
