# Análise de rede textual — Capítulo 4

> Análise de rede textual (*text network analysis*, Paranyushkin 2019)
> aplicada ao arquivo `ex_cap4.tex`. O texto foi limpo de comandos LaTeX,
> citações e notas de rodapé foram reincorporadas; janela deslizante de
> 4 *tokens* com pesos decrescentes pela distância (3-2-1). Comunidades
> detectadas por Louvain ponderado. Esta versão acrescenta duas métricas
> *informativas* que não dependem da frequência bruta: **PageRank** dos
> nós e **NPMI** das arestas. As métricas baseadas em frequência são
> mantidas em paralelo, para comparação.

## 1. Resumo quantitativo
- Tokens significativos: **30,954**
- Grafo bruto: **6636** nós · **75148** arestas
- Grafo analítico (top 180 nós, peso ≥ 2, maior componente): **180** nós · **3851** arestas
- Tópicos detectados (Louvain): **7**

## 2. Conceitos mais influentes (degree ponderado · *baseline* frequentista)
| # | termo | grau ponderado |
|---|-------|----------------|
| 1 | `spira` | 1708 |
| 2 | `covideiro` | 1077 |
| 3 | `rede` | 1042 |
| 4 | `inscricao` | 988 |
| 5 | `cadeia` | 849 |
| 6 | `artigo` | 798 |
| 7 | `objeto` | 738 |
| 8 | `dado` | 689 |
| 9 | `respiratoria` | 655 |
| 10 | `insuficiencia` | 632 |
| 11 | `projeto` | 621 |
| 12 | `marcelo` | 612 |
| 13 | `modelo` | 577 |
| 14 | `artigos` | 520 |
| 15 | `espectrograma` | 504 |
| 16 | `coleta` | 504 |
| 17 | `actante` | 403 |
| 18 | `pratica` | 397 |
| 19 | `covid` | 380 |
| 20 | `partir` | 364 |
| 21 | `ruido` | 364 |
| 22 | `sinal` | 362 |
| 23 | `condicoes` | 358 |
| 24 | `pacientes` | 356 |
| 25 | `analise` | 355 |
| 26 | `torna` | 347 |
| 27 | `cientifico` | 331 |
| 28 | `dataset` | 329 |
| 29 | `ponto` | 328 |
| 30 | `paciente` | 325 |

## 3. Conceitos mais influentes (PageRank · centralidade na rede)
PageRank pondera a importância de um nó pela importância dos seus
vizinhos. Termos pouco frequentes mas bem posicionados na rede sobem;
termos frequentes mas perifericamente conectados descem.

| # | termo | PageRank |
|---|-------|----------|
| 1 | `spira` | 0.0365 |
| 2 | `covideiro` | 0.0233 |
| 3 | `rede` | 0.0225 |
| 4 | `inscricao` | 0.0218 |
| 5 | `cadeia` | 0.0187 |
| 6 | `artigo` | 0.0175 |
| 7 | `objeto` | 0.0163 |
| 8 | `dado` | 0.0151 |
| 9 | `projeto` | 0.0137 |
| 10 | `marcelo` | 0.0135 |
| 11 | `respiratoria` | 0.0133 |
| 12 | `modelo` | 0.0131 |
| 13 | `insuficiencia` | 0.0128 |
| 14 | `coleta` | 0.0114 |
| 15 | `espectrograma` | 0.0114 |
| 16 | `artigos` | 0.0113 |
| 17 | `actante` | 0.0094 |
| 18 | `pratica` | 0.0093 |
| 19 | `ruido` | 0.0087 |
| 20 | `sinal` | 0.0085 |
| 21 | `covid` | 0.0085 |
| 22 | `partir` | 0.0084 |
| 23 | `torna` | 0.0084 |
| 24 | `condicoes` | 0.0082 |
| 25 | `pacientes` | 0.0082 |
| 26 | `analise` | 0.0080 |
| 27 | `ponto` | 0.0077 |
| 28 | `dataset` | 0.0076 |
| 29 | `paciente` | 0.0076 |
| 30 | `laboratorio` | 0.0075 |

## 4. Termos mais subvalorizados pela frequência (degree → PageRank)
Diferença de posição (rank por degree) − (rank por PageRank). Valor
positivo = o termo é *mais central na rede* do que sugere sua frequência.

| # | termo | degree-rank | pagerank-rank | salto |
|---|-------|-------------|----------------|-------|
| 1 | `microfone` | 79 | 65 | +14 |
| 2 | `escala` | 110 | 99 | +11 |
| 3 | `grade` | 136 | 127 | +9 |
| 4 | `visivel` | 75 | 67 | +8 |
| 5 | `processamento` | 78 | 71 | +7 |
| 6 | `resultado` | 95 | 88 | +7 |
| 7 | `diante` | 105 | 98 | +7 |
| 8 | `fapesp` | 124 | 117 | +7 |
| 9 | `padrao` | 152 | 146 | +6 |
| 10 | `saude` | 155 | 149 | +6 |
| 11 | `pesquisa` | 81 | 76 | +5 |
| 12 | `relatorios` | 98 | 93 | +5 |
| 13 | `argumento` | 114 | 109 | +5 |
| 14 | `carrega` | 115 | 110 | +5 |
| 15 | `diferenca` | 116 | 111 | +5 |

## 5. Pontes conceituais (betweenness — termos que costuram tópicos)
| # | termo | betweenness |
|---|-------|-------------|
| 1 | `spira` | 0.5467 |
| 2 | `covideiro` | 0.1944 |
| 3 | `inscricao` | 0.1384 |
| 4 | `rede` | 0.1254 |
| 5 | `cadeia` | 0.1118 |
| 6 | `artigo` | 0.0995 |
| 7 | `objeto` | 0.0964 |
| 8 | `dado` | 0.0751 |
| 9 | `respiratoria` | 0.0629 |
| 10 | `modelo` | 0.0619 |
| 11 | `espectrograma` | 0.0522 |
| 12 | `projeto` | 0.0511 |
| 13 | `sinal` | 0.0419 |
| 14 | `pratica` | 0.0353 |
| 15 | `coleta` | 0.0341 |
| 16 | `ruido` | 0.0305 |
| 17 | `covid` | 0.0252 |
| 18 | `marcelo` | 0.0236 |
| 19 | `actante` | 0.0186 |
| 20 | `artigos` | 0.0174 |

## 6. Pares de termos com associação mais surpreendente (NPMI)
NPMI mede *quão surpreendente* é a co-ocorrência de duas palavras dadas
suas frequências individuais. Diferente do peso bruto, ele faz aparecer
pares semanticamente fortes mesmo quando os termos co-ocorrem poucas
vezes.

| # | termo A | termo B | NPMI | co-ocorr. (peso) |
|---|---------|---------|------|------------------|
| 1 | `imutavel` | `movel` | 0.844 | 75 |
| 2 | `respiratoria` | `insuficiencia` | 0.841 | 288 |
| 3 | `grupo` | `controle` | 0.667 | 46 |
| 4 | `escuta` | `clinica` | 0.620 | 39 |
| 5 | `neural` | `rede` | 0.578 | 126 |
| 6 | `linguagem` | `processamento` | 0.575 | 33 |
| 7 | `acao` | `programa` | 0.567 | 30 |
| 8 | `diante` | `microfone` | 0.561 | 30 |
| 9 | `sinal` | `acustico` | 0.527 | 49 |
| 10 | `tornou` | `possivel` | 0.524 | 32 |
| 11 | `entrevista` | `marcelo` | 0.499 | 92 |
| 12 | `acesso` | `disponivel` | 0.487 | 25 |
| 13 | `enfermaria` | `ruido` | 0.484 | 62 |
| 14 | `publico` | `repositorio` | 0.483 | 24 |
| 15 | `fonoaudiologos` | `medicos` | 0.478 | 22 |
| 16 | `torna` | `visivel` | 0.474 | 37 |
| 17 | `covideiro` | `pandemico` | 0.467 | 85 |
| 18 | `pessoas` | `voz` | 0.459 | 26 |
| 19 | `controles` | `pacientes` | 0.444 | 40 |
| 20 | `textual` | `analise` | 0.444 | 27 |
| 21 | `publico` | `saude` | 0.436 | 18 |
| 22 | `tornou` | `visivel` | 0.432 | 18 |
| 23 | `saude` | `pesquisa` | 0.431 | 20 |
| 24 | `cadeia` | `translacao` | 0.428 | 65 |
| 25 | `condicoes` | `producao` | 0.418 | 36 |

## 7. Tópicos latentes (comunidades Louvain)
- **Tópico 1** (32 termos): inscricao, cadeia, ponto, secao, dispositivo, latour
- **Tópico 2** (32 termos): espectrograma, partir, sinal, torna, paciente, audio
- **Tópico 3** (30 termos): spira, projeto, marcelo, artigos, dataset, entrevista
- **Tópico 4** (30 termos): covideiro, artigo, coleta, actante, condicoes, cientifico
- **Tópico 5** (20 termos): rede, objeto, pratica, analise, condicao, neural
- **Tópico 6** (20 termos): respiratoria, insuficiencia, covid, ruido, pacientes, enfermaria
- **Tópico 7** (16 termos): dado, modelo, repositorio, computacional, treinamento, coeficientes

## 8. Lacunas estruturais (pares de tópicos fracamente conectados)
Lacunas estruturais sinalizam *espaços de ideia* pouco articulados no
texto — candidatos a aprofundamento argumentativo.

- Lacuna entre **Tópico 2** [espectrograma, partir, sinal] e **Tópico 3** [spira, projeto, marcelo] — densidade ponderada de ligação = 0.7438
- Lacuna entre **Tópico 1** [inscricao, cadeia, ponto] e **Tópico 2** [espectrograma, partir, sinal] — densidade ponderada de ligação = 0.7510
- Lacuna entre **Tópico 2** [espectrograma, partir, sinal] e **Tópico 5** [rede, objeto, pratica] — densidade ponderada de ligação = 0.7797
- Lacuna entre **Tópico 2** [espectrograma, partir, sinal] e **Tópico 4** [covideiro, artigo, coleta] — densidade ponderada de ligação = 0.8271
- Lacuna entre **Tópico 4** [covideiro, artigo, coleta] e **Tópico 5** [rede, objeto, pratica] — densidade ponderada de ligação = 0.9917
- Lacuna entre **Tópico 1** [inscricao, cadeia, ponto] e **Tópico 3** [spira, projeto, marcelo] — densidade ponderada de ligação = 1.0333

## 9. Leitura interpretativa
**O que a rede mostra.** O capítulo organiza-se em torno do projeto SPIRA (a
maior ponte do grafo, betweenness 0,60) e do aparato latouriano da
*inscrição*: os pares de maior associação são exatamente os conceitos-chave
— `caixa ↔ preta` (a caixa-preta) e `imutavel ↔ movel` (o *móvel imutável*
de Latour). A `cadeia` de translações percorre a cena clínica
(`respiratoria`, `insuficiencia`, `covid`, `enfermaria`, `ruido`), passa pelo
sinal (`espectrograma`, `sinal`, `acustico`), pelo dado e pelo modelo
(`dado`, `modelo`, `treinamento`, `rede neural`) e chega ao `artigo`.

**Pontes (`betweenness`).** Além de `spira`, são pontes `inscricao`,
`covideiro`, `cadeia`, `objeto`, `rede` e `artigo`. Vale notar `covideiro` —
o neologismo/actante cunhado no capítulo — operando como conector: a própria
invenção lexical do texto faz trabalho de tradução na rede.

**Lacunas a desenvolver.** As ligações mais fracas caem justamente nas
*juntas* da cadeia: entre a teoria da inscrição (`inscricao`, `cadeia`,
`dispositivo`) e o par dado/modelo é a lacuna mais forte; e seguem fracas as
costuras entre o espectrograma/sinal e o artigo/dado. Os pontos onde a rede é
mais rala são exatamente as translações que o capítulo narra — um convite a
tornar explícito *como* cada elo converte um estado no seguinte (voz → sinal
→ espectrograma → dado → modelo → artigo).

## 10. Arquivos gerados
**Visões frequentistas**
- `infranodus_cap4_network.png` — rede completa, tamanho por degree.
- `infranodus_cap4_focus.png` — núcleo (top-100, peso ≥ 3).

**Visões informativas**
- `infranodus_cap4_pmi.png` — rede completa, tamanho por **PageRank**,
  arestas filtradas por **NPMI ≥ 0,20**.
- `infranodus_cap4_focus_pmi.png` — núcleo, NPMI ≥ 0,25.

**Dados**
- `infranodus_cap4_metrics.json` — métricas brutas (degree, betweenness,
  PageRank, NPMI, comunidades, lacunas).
- `infranodus_cap4.gexf` / `infranodus_cap4_focus.gexf` — grafos para Gephi
  já com `community`, `frequency`, `degree_weighted`, `betweenness`,
  `pagerank` (nós) e `weight`, `npmi` (arestas).
- `infranodus_cap4_nodes.csv` / `infranodus_cap4_edges.csv` (e `_focus_*`)
  — fallback em planilha; CSVs trazem todas as colunas acima.

## 11. Como abrir no Gephi
1. Instale Gephi (≥ 0.10): https://gephi.org/users/download/
2. `File → Open…` → selecione `infranodus_cap4.gexf` (ou `_focus.gexf`).
3. No painel **Appearance**: já vem com cor por `community` e tamanho por
   `degree_weighted` (embutidos via atributos `viz`). Ajuste se quiser.
4. Em **Layout**: aplique *ForceAtlas 2* (ative *Prevent Overlap* e
   *Dissuade Hubs*) por ~30 s; ou *Fruchterman-Reingold* para algo mais rápido.
5. Em **Statistics**: rode *Modularity* e *Average Path Length* se quiser
   recalcular comunidades dentro do Gephi (resultados serão semelhantes).
6. Em **Preview**: ative *Node Labels*, escolha fonte e exporte para PDF/SVG.
