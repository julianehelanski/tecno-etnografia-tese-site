# Análise de rede textual — Capítulo 1

> Análise de rede textual (*text network analysis*, Paranyushkin 2019)
> aplicada ao arquivo `ex_cap1.tex`. O texto foi limpo de comandos LaTeX,
> citações e notas de rodapé foram reincorporadas; janela deslizante de
> 4 *tokens* com pesos decrescentes pela distância (3-2-1). Comunidades
> detectadas por Louvain ponderado. Esta versão acrescenta duas métricas
> *informativas* que não dependem da frequência bruta: **PageRank** dos
> nós e **NPMI** das arestas. As métricas baseadas em frequência são
> mantidas em paralelo, para comparação.

## 1. Resumo quantitativo
- Tokens significativos: **23,205**
- Grafo bruto: **6595** nós · **58663** arestas
- Grafo analítico (top 180 nós, peso ≥ 2, maior componente): **180** nós · **3291** arestas
- Tópicos detectados (Louvain): **8**

## 2. Conceitos mais influentes (degree ponderado · *baseline* frequentista)
| # | termo | grau ponderado |
|---|-------|----------------|
| 1 | `rede` | 1296 |
| 2 | `pesquisa` | 985 |
| 3 | `etnografia` | 838 |
| 4 | `artificial` | 708 |
| 5 | `inteligencia` | 697 |
| 6 | `ciencia` | 614 |
| 7 | `latour` | 609 |
| 8 | `campo` | 587 |
| 9 | `metodo` | 538 |
| 10 | `objeto` | 495 |
| 11 | `corte` | 471 |
| 12 | `humano` | 445 |
| 13 | `descricao` | 415 |
| 14 | `pratica` | 397 |
| 15 | `inscricao` | 389 |
| 16 | `strathern` | 387 |
| 17 | `modelo` | 372 |
| 18 | `relacao` | 354 |
| 19 | `ator` | 350 |
| 20 | `analise` | 344 |
| 21 | `gesto` | 339 |
| 22 | `dado` | 325 |
| 23 | `parte` | 320 |
| 24 | `maquina` | 319 |
| 25 | `haraway` | 308 |
| 26 | `teoria` | 305 |
| 27 | `conceito` | 304 |
| 28 | `escrita` | 286 |
| 29 | `descreve` | 274 |
| 30 | `sociais` | 270 |

## 3. Conceitos mais influentes (PageRank · centralidade na rede)
PageRank pondera a importância de um nó pela importância dos seus
vizinhos. Termos pouco frequentes mas bem posicionados na rede sobem;
termos frequentes mas perifericamente conectados descem.

| # | termo | PageRank |
|---|-------|----------|
| 1 | `rede` | 0.0331 |
| 2 | `pesquisa` | 0.0256 |
| 3 | `etnografia` | 0.0220 |
| 4 | `artificial` | 0.0166 |
| 5 | `inteligencia` | 0.0163 |
| 6 | `latour` | 0.0163 |
| 7 | `ciencia` | 0.0160 |
| 8 | `campo` | 0.0158 |
| 9 | `metodo` | 0.0146 |
| 10 | `objeto` | 0.0132 |
| 11 | `corte` | 0.0127 |
| 12 | `humano` | 0.0123 |
| 13 | `descricao` | 0.0113 |
| 14 | `inscricao` | 0.0108 |
| 15 | `pratica` | 0.0108 |
| 16 | `strathern` | 0.0108 |
| 17 | `modelo` | 0.0104 |
| 18 | `relacao` | 0.0099 |
| 19 | `analise` | 0.0093 |
| 20 | `gesto` | 0.0092 |
| 21 | `maquina` | 0.0090 |
| 22 | `parte` | 0.0090 |
| 23 | `dado` | 0.0089 |
| 24 | `haraway` | 0.0089 |
| 25 | `ator` | 0.0088 |
| 26 | `conceito` | 0.0087 |
| 27 | `escrita` | 0.0081 |
| 28 | `teoria` | 0.0078 |
| 29 | `descreve` | 0.0078 |
| 30 | `claude` | 0.0074 |

## 4. Termos mais subvalorizados pela frequência (degree → PageRank)
Diferença de posição (rank por degree) − (rank por PageRank). Valor
positivo = o termo é *mais central na rede* do que sugere sua frequência.

| # | termo | degree-rank | pagerank-rank | salto |
|---|-------|-------------|----------------|-------|
| 1 | `cientifico` | 140 | 125 | +15 |
| 2 | `computacional` | 114 | 100 | +14 |
| 3 | `tecnica` | 105 | 93 | +12 |
| 4 | `instituicao` | 96 | 86 | +10 |
| 5 | `infraestrutura` | 74 | 66 | +8 |
| 6 | `cortes` | 106 | 99 | +7 |
| 7 | `condicoes` | 103 | 97 | +6 |
| 8 | `termos` | 46 | 41 | +5 |
| 9 | `actante` | 52 | 47 | +5 |
| 10 | `subsecao` | 97 | 92 | +5 |
| 11 | `funcionam` | 115 | 110 | +5 |
| 12 | `ausencia` | 56 | 52 | +4 |
| 13 | `spira` | 62 | 58 | +4 |
| 14 | `modos` | 67 | 63 | +4 |
| 15 | `associacao` | 78 | 74 | +4 |

## 5. Pontes conceituais (betweenness — termos que costuram tópicos)
| # | termo | betweenness |
|---|-------|-------------|
| 1 | `rede` | 0.3822 |
| 2 | `pesquisa` | 0.2727 |
| 3 | `etnografia` | 0.1779 |
| 4 | `latour` | 0.1619 |
| 5 | `campo` | 0.1175 |
| 6 | `corte` | 0.1152 |
| 7 | `ciencia` | 0.0731 |
| 8 | `metodo` | 0.0676 |
| 9 | `descricao` | 0.0548 |
| 10 | `humano` | 0.0531 |
| 11 | `inscricao` | 0.0460 |
| 12 | `objeto` | 0.0425 |
| 13 | `strathern` | 0.0419 |
| 14 | `maquina` | 0.0356 |
| 15 | `claude` | 0.0260 |
| 16 | `modos` | 0.0254 |
| 17 | `dado` | 0.0244 |
| 18 | `parcial` | 0.0227 |
| 19 | `pratica` | 0.0203 |
| 20 | `hinterland` | 0.0198 |

## 6. Pares de termos com associação mais surpreendente (NPMI)
NPMI mede *quão surpreendente* é a co-ocorrência de duas palavras dadas
suas frequências individuais. Diferente do peso bruto, ele faz aparecer
pares semanticamente fortes mesmo quando os termos co-ocorrem poucas
vezes.

| # | termo A | termo B | NPMI | co-ocorr. (peso) |
|---|---------|---------|------|------------------|
| 1 | `ausencia` | `manifesta` | 0.864 | 67 |
| 2 | `inteligencia` | `artificial` | 0.857 | 316 |
| 3 | `existencias` | `parciais` | 0.826 | 84 |
| 4 | `parcial` | `existencia` | 0.745 | 59 |
| 5 | `teoria` | `ator` | 0.728 | 104 |
| 6 | `distribuida` | `agencia` | 0.726 | 52 |
| 7 | `presenca` | `ausencia` | 0.707 | 43 |
| 8 | `otherness` | `manifesta` | 0.684 | 40 |
| 9 | `tecnico` | `letramento` | 0.655 | 46 |
| 10 | `parcial` | `conexao` | 0.634 | 43 |
| 11 | `infraestrutura` | `computacional` | 0.631 | 38 |
| 12 | `presenca` | `manifesta` | 0.622 | 28 |
| 13 | `otherness` | `ausencia` | 0.617 | 34 |
| 14 | `modelo` | `linguagem` | 0.616 | 87 |
| 15 | `heterogeneos` | `materiais` | 0.600 | 36 |
| 16 | `figuracao` | `textil` | 0.597 | 54 |
| 17 | `ciencia` | `sociais` | 0.578 | 94 |
| 18 | `generativa` | `artificial` | 0.559 | 65 |
| 19 | `textual` | `analise` | 0.554 | 49 |
| 20 | `otherness` | `hinterland` | 0.546 | 36 |
| 21 | `otherness` | `presenca` | 0.545 | 25 |
| 22 | `antropologia` | `tecnica` | 0.544 | 21 |
| 23 | `condicoes` | `materiais` | 0.540 | 31 |
| 24 | `cientista` | `computacao` | 0.538 | 22 |
| 25 | `haraway` | `barad` | 0.517 | 29 |

## 7. Tópicos latentes (comunidades Louvain)
- **Tópico 1** (49 termos): latour, metodo, corte, strathern, gesto, haraway
- **Tópico 2** (33 termos): pesquisa, artificial, inteligencia, objeto, pratica, modelo
- **Tópico 3** (24 termos): ciencia, campo, dado, escrita, sociais, tecnologia
- **Tópico 4** (21 termos): humano, relacao, maquina, parcial, plano, agencia
- **Tópico 5** (20 termos): etnografia, descricao, inscricao, parte, descreve, tecnociencia
- **Tópico 6** (18 termos): rede, ator, analise, teoria, termos, actante
- **Tópico 7** (8 termos): materiais, ponto, condicoes, heterogeneos, precisa, tecnicas
- **Tópico 8** (7 termos): hinterland, otherness, ausencia, manifesta, presenca, palavra

## 8. Lacunas estruturais (pares de tópicos fracamente conectados)
Lacunas estruturais sinalizam *espaços de ideia* pouco articulados no
texto — candidatos a aprofundamento argumentativo.

- Lacuna entre **Tópico 3** [ciencia, campo, dado] e **Tópico 4** [humano, relacao, maquina] — densidade ponderada de ligação = 0.4841
- Lacuna entre **Tópico 1** [latour, metodo, corte] e **Tópico 2** [pesquisa, artificial, inteligencia] — densidade ponderada de ligação = 0.5325
- Lacuna entre **Tópico 1** [latour, metodo, corte] e **Tópico 4** [humano, relacao, maquina] — densidade ponderada de ligação = 0.5442
- Lacuna entre **Tópico 1** [latour, metodo, corte] e **Tópico 3** [ciencia, campo, dado] — densidade ponderada de ligação = 0.5689
- Lacuna entre **Tópico 2** [pesquisa, artificial, inteligencia] e **Tópico 4** [humano, relacao, maquina] — densidade ponderada de ligação = 0.6306
- Lacuna entre **Tópico 4** [humano, relacao, maquina] e **Tópico 5** [etnografia, descricao, inscricao] — densidade ponderada de ligação = 0.6333

## 9. Leitura interpretativa
**O que a rede mostra.** O núcleo do capítulo gira em torno de `rede`,
`etnografia` e `pesquisa`, articulando quatro famílias de termos: a
etnografia e o campo (`etnografia`, `pesquisa`, `campo`, `descricao`,
`pratica`); o método e a teoria ator-rede (`metodo`, `latour`, `corte`,
`strathern`, `haraway`); a inteligência artificial como objeto
(`artificial`, `inteligencia`, `objeto`, `modelo`, `laboratorio`); e a
simetria humano/não-humano (`humano`, `relacao`, `parcial`, `maquina`,
`agencia`). Um pequeno polo teórico denso reúne Law e Mol (`otherness`,
`ausencia`, `presenca`, `manifesta`).

**Pontes (`betweenness`).** As maiores pontes são `rede`, `pesquisa` e
`etnografia` — palavras-coringa que circulam entre os sub-vocabulários —,
seguidas de `corte` (o "corte agencial"), `latour`, `ciencia` e `metodo`. As
associações teoricamente densas aparecem como pares NPMI fortes, ainda que
pouco frequentes: `parcial ↔ existencia` (Strathern, 0,75), `distribuida ↔
agencia` (0,72), `teoria ↔ ator` (0,72), `presenca ↔ ausencia` (Law/Mol,
0,70) e `principio ↔ simetria` (0,56).

**Lacunas a desenvolver.** A ligação mais fraca está entre o tópico do
método/ator-rede (`metodo`, `latour`, `corte`) e o tópico da IA como objeto
(`artificial`, `inteligencia`, `objeto`): o vocabulário com que se promete
descrever e o objeto técnico a descrever ainda não estão suficientemente
costurados. Fraca também é a costura entre a etnografia/campo e a simetria
humano/máquina (`humano`, `parcial`, `agencia`) — exatamente a aposta que o
capítulo seguinte precisa desenvolver.

## 10. Arquivos gerados
**Visões frequentistas**
- `infranodus_cap1_network.png` — rede completa, tamanho por degree.
- `infranodus_cap1_focus.png` — núcleo (top-100, peso ≥ 3).

**Visões informativas**
- `infranodus_cap1_pmi.png` — rede completa, tamanho por **PageRank**,
  arestas filtradas por **NPMI ≥ 0,20**.
- `infranodus_cap1_focus_pmi.png` — núcleo, NPMI ≥ 0,25.

**Dados**
- `infranodus_cap1_metrics.json` — métricas brutas (degree, betweenness,
  PageRank, NPMI, comunidades, lacunas).
- `infranodus_cap1.gexf` / `infranodus_cap1_focus.gexf` — grafos para Gephi
  já com `community`, `frequency`, `degree_weighted`, `betweenness`,
  `pagerank` (nós) e `weight`, `npmi` (arestas).
- `infranodus_cap1_nodes.csv` / `infranodus_cap1_edges.csv` (e `_focus_*`)
  — fallback em planilha; CSVs trazem todas as colunas acima.

## 11. Como abrir no Gephi
1. Instale Gephi (≥ 0.10): https://gephi.org/users/download/
2. `File → Open…` → selecione `infranodus_cap1.gexf` (ou `_focus.gexf`).
3. No painel **Appearance**: já vem com cor por `community` e tamanho por
   `degree_weighted` (embutidos via atributos `viz`). Ajuste se quiser.
4. Em **Layout**: aplique *ForceAtlas 2* (ative *Prevent Overlap* e
   *Dissuade Hubs*) por ~30 s; ou *Fruchterman-Reingold* para algo mais rápido.
5. Em **Statistics**: rode *Modularity* e *Average Path Length* se quiser
   recalcular comunidades dentro do Gephi (resultados serão semelhantes).
6. Em **Preview**: ative *Node Labels*, escolha fonte e exporte para PDF/SVG.
