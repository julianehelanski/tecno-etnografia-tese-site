# Análise de rede textual — Capítulo 3

> Análise de rede textual (*text network analysis*, Paranyushkin 2019)
> aplicada ao arquivo `ex_cap3.tex`. O texto foi limpo de comandos LaTeX,
> citações e notas de rodapé foram reincorporadas; janela deslizante de
> 4 *tokens* com pesos decrescentes pela distância (3-2-1). Comunidades
> detectadas por Louvain ponderado. Esta versão acrescenta duas métricas
> *informativas* que não dependem da frequência bruta: **PageRank** dos
> nós e **NPMI** das arestas. As métricas baseadas em frequência são
> mantidas em paralelo, para comparação.

## 1. Resumo quantitativo
- Tokens significativos: **19,074**
- Grafo bruto: **5713** nós · **49584** arestas
- Grafo analítico (top 180 nós, peso ≥ 2, maior componente): **180** nós · **2627** arestas
- Tópicos detectados (Louvain): **7**

## 2. Conceitos mais influentes (degree ponderado · *baseline* frequentista)
| # | termo | grau ponderado |
|---|-------|----------------|
| 1 | `claudio` | 887 |
| 2 | `pesquisa` | 736 |
| 3 | `rede` | 568 |
| 4 | `fabio` | 528 |
| 5 | `centro` | 514 |
| 6 | `seguir` | 363 |
| 7 | `inteligencia` | 346 |
| 8 | `artificial` | 345 |
| 9 | `arranjo` | 340 |
| 10 | `publico` | 336 |
| 11 | `brasil` | 333 |
| 12 | `corporacao` | 333 |
| 13 | `tecnologia` | 319 |
| 14 | `fapesp` | 309 |
| 15 | `maquina` | 303 |
| 16 | `ecossistema` | 297 |
| 17 | `ator` | 286 |
| 18 | `hollerith` | 274 |
| 19 | `laboratorio` | 271 |
| 20 | `dado` | 265 |
| 21 | `modelo` | 264 |
| 22 | `empresa` | 257 |
| 23 | `informacao` | 236 |
| 24 | `universidade` | 235 |
| 25 | `campo` | 221 |
| 26 | `trajetoria` | 218 |
| 27 | `instituicao` | 218 |
| 28 | `associacao` | 218 |
| 29 | `pergunta` | 218 |
| 30 | `verbal` | 208 |

## 3. Conceitos mais influentes (PageRank · centralidade na rede)
PageRank pondera a importância de um nó pela importância dos seus
vizinhos. Termos pouco frequentes mas bem posicionados na rede sobem;
termos frequentes mas perifericamente conectados descem.

| # | termo | PageRank |
|---|-------|----------|
| 1 | `claudio` | 0.0300 |
| 2 | `pesquisa` | 0.0265 |
| 3 | `rede` | 0.0207 |
| 4 | `centro` | 0.0185 |
| 5 | `fabio` | 0.0177 |
| 6 | `seguir` | 0.0134 |
| 7 | `arranjo` | 0.0128 |
| 8 | `corporacao` | 0.0127 |
| 9 | `tecnologia` | 0.0125 |
| 10 | `brasil` | 0.0125 |
| 11 | `publico` | 0.0124 |
| 12 | `inteligencia` | 0.0120 |
| 13 | `artificial` | 0.0120 |
| 14 | `fapesp` | 0.0119 |
| 15 | `maquina` | 0.0115 |
| 16 | `ecossistema` | 0.0109 |
| 17 | `hollerith` | 0.0108 |
| 18 | `ator` | 0.0108 |
| 19 | `dado` | 0.0106 |
| 20 | `modelo` | 0.0104 |
| 21 | `laboratorio` | 0.0101 |
| 22 | `empresa` | 0.0099 |
| 23 | `universidade` | 0.0089 |
| 24 | `trajetoria` | 0.0086 |
| 25 | `campo` | 0.0086 |
| 26 | `pergunta` | 0.0085 |
| 27 | `associacao` | 0.0084 |
| 28 | `instituicao` | 0.0084 |
| 29 | `infraestrutura` | 0.0083 |
| 30 | `informacao` | 0.0081 |

## 4. Termos mais subvalorizados pela frequência (degree → PageRank)
Diferença de posição (rank por degree) − (rank por PageRank). Valor
positivo = o termo é *mais central na rede* do que sugere sua frequência.

| # | termo | degree-rank | pagerank-rank | salto |
|---|-------|-------------|----------------|-------|
| 1 | `conta` | 141 | 127 | +14 |
| 2 | `vida` | 164 | 151 | +13 |
| 3 | `linguas` | 109 | 98 | +11 |
| 4 | `mostra` | 137 | 126 | +11 |
| 5 | `cadeia` | 99 | 89 | +10 |
| 6 | `censo` | 140 | 130 | +10 |
| 7 | `indigenas` | 102 | 93 | +9 |
| 8 | `estados` | 64 | 56 | +8 |
| 9 | `estatistica` | 114 | 106 | +8 |
| 10 | `tecnica` | 71 | 64 | +7 |
| 11 | `tecnociencia` | 110 | 103 | +7 |
| 12 | `objeto` | 150 | 144 | +6 |
| 13 | `descreve` | 55 | 50 | +5 |
| 14 | `escala` | 67 | 62 | +5 |
| 15 | `pratica` | 78 | 73 | +5 |

## 5. Pontes conceituais (betweenness — termos que costuram tópicos)
| # | termo | betweenness |
|---|-------|-------------|
| 1 | `pesquisa` | 0.3150 |
| 2 | `centro` | 0.2669 |
| 3 | `claudio` | 0.2163 |
| 4 | `rede` | 0.1683 |
| 5 | `fabio` | 0.1292 |
| 6 | `tecnologia` | 0.0758 |
| 7 | `dado` | 0.0700 |
| 8 | `seguir` | 0.0688 |
| 9 | `fapesp` | 0.0678 |
| 10 | `inteligencia` | 0.0667 |
| 11 | `hollerith` | 0.0651 |
| 12 | `ator` | 0.0614 |
| 13 | `ecossistema` | 0.0558 |
| 14 | `brasil` | 0.0503 |
| 15 | `empresa` | 0.0426 |
| 16 | `corporacao` | 0.0424 |
| 17 | `artificial` | 0.0421 |
| 18 | `maquina` | 0.0416 |
| 19 | `trajetoria` | 0.0402 |
| 20 | `arranjo` | 0.0346 |

## 6. Pares de termos com associação mais surpreendente (NPMI)
NPMI mede *quão surpreendente* é a co-ocorrência de duas palavras dadas
suas frequências individuais. Diferente do peso bruto, ele faz aparecer
pares semanticamente fortes mesmo quando os termos co-ocorrem poucas
vezes.

| # | termo A | termo B | NPMI | co-ocorr. (peso) |
|---|---------|---------|------|------------------|
| 1 | `informacao` | `verbal` | 0.873 | 83 |
| 2 | `inteligencia` | `artificial` | 0.864 | 150 |
| 3 | `unidos` | `estados` | 0.851 | 54 |
| 4 | `linguas` | `indigenas` | 0.782 | 40 |
| 5 | `linguagem` | `natural` | 0.750 | 46 |
| 6 | `aberto` | `codigo` | 0.734 | 54 |
| 7 | `processamento` | `natural` | 0.696 | 28 |
| 8 | `linguagem` | `processamento` | 0.677 | 40 |
| 9 | `maquina` | `aprendizado` | 0.648 | 53 |
| 10 | `acesso` | `disponivel` | 0.646 | 40 |
| 11 | `historica` | `investigacao` | 0.620 | 24 |
| 12 | `claudio` | `fabio` | 0.579 | 183 |
| 13 | `research` | `brasil` | 0.574 | 51 |
| 14 | `inovacao` | `ecossistema` | 0.551 | 58 |
| 15 | `laboratorio` | `fechamento` | 0.517 | 34 |
| 16 | `hollerith` | `tabulacao` | 0.513 | 39 |
| 17 | `comercial` | `tecnica` | 0.508 | 19 |
| 18 | `claudio` | `informacao` | 0.491 | 72 |
| 19 | `sistema` | `tabulacao` | 0.488 | 24 |
| 20 | `gente` | `dinheiro` | 0.488 | 15 |
| 21 | `fapesp` | `convenio` | 0.482 | 23 |
| 22 | `entrevistas` | `observacao` | 0.482 | 20 |
| 23 | `documentos` | `entrevistas` | 0.480 | 21 |
| 24 | `linguas` | `projeto` | 0.458 | 12 |
| 25 | `cientifico` | `producao` | 0.457 | 22 |

## 7. Tópicos latentes (comunidades Louvain)
- **Tópico 1** (46 termos): pesquisa, centro, publico, corporacao, fapesp, universidade
- **Tópico 2** (45 termos): rede, seguir, arranjo, ator, trajetoria, associacao
- **Tópico 3** (31 termos): tecnologia, maquina, hollerith, dado, tabulacao, ciencia
- **Tópico 4** (16 termos): modelo, codigo, linguagem, aberto, processamento, natural
- **Tópico 5** (15 termos): claudio, fabio, informacao, campo, pergunta, verbal
- **Tópico 6** (14 termos): inteligencia, artificial, ecossistema, empresa, inovacao, relacao
- **Tópico 7** (13 termos): brasil, laboratorio, vinculo, pesquisador, acesso, research

## 8. Lacunas estruturais (pares de tópicos fracamente conectados)
Lacunas estruturais sinalizam *espaços de ideia* pouco articulados no
texto — candidatos a aprofundamento argumentativo.

- Lacuna entre **Tópico 2** [rede, seguir, arranjo] e **Tópico 4** [modelo, codigo, linguagem] — densidade ponderada de ligação = 0.1847
- Lacuna entre **Tópico 3** [tecnologia, maquina, hollerith] e **Tópico 5** [claudio, fabio, informacao] — densidade ponderada de ligação = 0.2946
- Lacuna entre **Tópico 2** [rede, seguir, arranjo] e **Tópico 3** [tecnologia, maquina, hollerith] — densidade ponderada de ligação = 0.3584
- Lacuna entre **Tópico 3** [tecnologia, maquina, hollerith] e **Tópico 4** [modelo, codigo, linguagem] — densidade ponderada de ligação = 0.3629
- Lacuna entre **Tópico 4** [modelo, codigo, linguagem] e **Tópico 5** [claudio, fabio, informacao] — densidade ponderada de ligação = 0.3667
- Lacuna entre **Tópico 1** [pesquisa, centro, publico] e **Tópico 4** [modelo, codigo, linguagem] — densidade ponderada de ligação = 0.3804

## 9. Leitura interpretativa
**O que a rede mostra.** O capítulo segue o arranjo do C4AI em três planos
que o grafo separa nitidamente. Há a infraestrutura histórica (`tecnologia`,
`hollerith`, `infraestrutura`, `empresa`, `maquina`, `trajetoria`) — a longa
trajetória das máquinas até a IBM; há o arranjo público-privado do presente
(`publico`, `arranjo`, `corporacao`, `universidade`, `brasil`); e há o
vocabulário do método (`rede`, `ator`, `associacao`, `sigo`, `descrevo`),
que forma comunidade própria — o gesto de "seguir os atores" é lexicalmente
distinto. Os atores seguidos no campo aparecem como uma dupla forte:
`claudio ↔ fabio` (NPMI 0,58).

**Pontes (`betweenness`).** `centro` e `pesquisa` são as maiores pontes,
seguidas de `rede`, `claudio`, `publico`, `corporacao` e `fabio`. O centro e
a pesquisa funcionam como termos-coringa que circulam entre a história
infraestrutural, o arranjo institucional e o trabalho de campo.

**Lacunas a desenvolver.** A ligação mais fraca está entre o vocabulário do
centro de pesquisa (`pesquisa`, `centro`, `cientifico`, `fapesp`) e o
vocabulário do método ator-rede (`rede`, `ator`, `associacao`): a instituição
descrita e o método que a descreve correm lado a lado. Fraca também é a
costura entre a infraestrutura histórica IBM/Hollerith e o centro do presente
— a história profunda das máquinas e o presente etnográfico pedem uma ponte
mais explícita.

## 10. Arquivos gerados
**Visões frequentistas**
- `infranodus_cap3_network.png` — rede completa, tamanho por degree.
- `infranodus_cap3_focus.png` — núcleo (top-100, peso ≥ 3).

**Visões informativas**
- `infranodus_cap3_pmi.png` — rede completa, tamanho por **PageRank**,
  arestas filtradas por **NPMI ≥ 0,20**.
- `infranodus_cap3_focus_pmi.png` — núcleo, NPMI ≥ 0,25.

**Dados**
- `infranodus_cap3_metrics.json` — métricas brutas (degree, betweenness,
  PageRank, NPMI, comunidades, lacunas).
- `infranodus_cap3.gexf` / `infranodus_cap3_focus.gexf` — grafos para Gephi
  já com `community`, `frequency`, `degree_weighted`, `betweenness`,
  `pagerank` (nós) e `weight`, `npmi` (arestas).
- `infranodus_cap3_nodes.csv` / `infranodus_cap3_edges.csv` (e `_focus_*`)
  — fallback em planilha; CSVs trazem todas as colunas acima.

## 11. Como abrir no Gephi
1. Instale Gephi (≥ 0.10): https://gephi.org/users/download/
2. `File → Open…` → selecione `infranodus_cap3.gexf` (ou `_focus.gexf`).
3. No painel **Appearance**: já vem com cor por `community` e tamanho por
   `degree_weighted` (embutidos via atributos `viz`). Ajuste se quiser.
4. Em **Layout**: aplique *ForceAtlas 2* (ative *Prevent Overlap* e
   *Dissuade Hubs*) por ~30 s; ou *Fruchterman-Reingold* para algo mais rápido.
5. Em **Statistics**: rode *Modularity* e *Average Path Length* se quiser
   recalcular comunidades dentro do Gephi (resultados serão semelhantes).
6. Em **Preview**: ative *Node Labels*, escolha fonte e exporte para PDF/SVG.
