# {tecnografia} — Rede textual da tese

> **Uso na tese.** Quais figuras e tabelas da tese (capítulos 1 a 5) vêm deste repositório, com o script e os dados de origem de cada uma, estão em [`docs/USO_NA_TESE.md`](docs/USO_NA_TESE.md) (versão tabular em [`docs/uso_na_tese.csv`](docs/uso_na_tese.csv)).


Site interativo que acompanha a tese de doutorado **"{tecnografia} de um
centro de inteligência artificial: seguindo cientistas e engenheiros —
universidade afora"** (Juliane Helanski · PPGCS/IFCH · Unicamp · 2026).

A página principal é uma **rede textual da tese**: um grafo de co-ocorrência de
termos gerado a partir do `.tex`, organizado em agrupamentos temáticos
(comunidades detectadas por Louvain). Pela
aba **`{a tese}`** abre-se um modal com resumo, sumário comentado, as galerias
de figuras de cada capítulo e as listas de ilustrações e tabelas.

## Como ler a rede

Cada **nó** é um termo recorrente no texto; uma **aresta** liga dois termos
que tendem a aparecer juntos (co-ocorrência), com peso dado pelo **NPMI**
(*normalized pointwise mutual information*) — quanto mais a dupla co-ocorre acima
do que o acaso explicaria, mais forte a ligação.

Os **agrupamentos temáticos** (cada cor) não são definidos à mão: são
**comunidades** detectadas automaticamente pelo algoritmo de **Louvain** sobre a
rede — ele reúne no mesmo grupo os termos que mais co-ocorrem entre si. O
tamanho de cada nó reflete sua **centralidade (PageRank)**. Essa nota técnica
aparece também na **legenda** do site e no painel de cada termo, para situar o
leitor. O pipeline completo (co-ocorrência · NPMI · Louvain · PageRank) está em
[`infranodus/tese_network.py`](infranodus/tese_network.py).

### A rede por capítulo (seletor da capa)

No alto da página há um **seletor** (`\rede{…}`) que troca o mapa entre a **tese
inteira** e cada **capítulo** (1 a 4). Cada capítulo tem a sua **própria** rede de
co-ocorrência e o seu **próprio Louvain** — ou seja, as comunidades são
recalculadas dentro do capítulo, não herdadas da tese inteira. É a mesma análise
da capa, aplicada ao recorte de cada capítulo (com painel de termo, associações
NPMI e trechos do próprio capítulo). Esses conjuntos de dados são gerados por
[`infranodus/tese_network_chapters.py`](infranodus/tese_network_chapters.py) e
embutidos no `index.html` (`<script id="netdata-chapters">`); os arquivos por
capítulo ficam em `infranodus/<cap>/netdata_<cap>.json`.

### Para que serve esta análise — e por que nesta tese

Ler uma tese inteira como uma rede de termos é um **dispositivo heurístico**:
não substitui a leitura nem produz "a verdade" do texto, mas oferece *portas de
entrada*. A rede torna visível a **arquitetura conceitual** do trabalho — os
eixos em torno dos quais ele gira, os termos que funcionam como **pontes**
(alta intermediação / *betweenness*) traduzindo entre o vocabulário teórico e a
descrição empírica, e as **lacunas** (ligações fracas) que apontam onde o
argumento ainda pode ser costurado. É exatamente esse tipo de leitura que a
interpretação do capítulo 1 ensaia (ver
[`infranodus/interpretation_cap1.md`](infranodus/interpretation_cap1.md)).

Mais do que um enfeite, a escolha é **coerente com a própria tese**. O trabalho
propõe uma *tecnografia*: descrever práticas tecnocientíficas **sem apagar a
técnica** que as sustenta, seguindo a teoria ator-rede e a noção latouriana de
**inscrição** — os diagramas, gráficos e representações que fazem o conhecimento
circular. Esta rede é, ela mesma, uma inscrição tecnocientífica aplicada
**reflexivamente** ao texto da tese: o aparato fica à vista (co-ocorrência ·
NPMI · Louvain · PageRank), não escondido. A interface pratica o que a tese
argumenta.

Há ainda um eco com o objeto empírico. Assim como o projeto SPIRA converte
voz → espectrograma → rede neural, este site converte tese → tokens → rede de
co-ocorrência: a mesma lógica de **cadeia de translações** que a etnografia
descreve, agora voltada sobre o próprio texto. Seguir os termos pela rede é
uma versão, em miniatura, do gesto que organiza a tese — *seguir os atores por
onde quer que vão*.

Ao **clicar em um termo**, abre-se à direita um painel (*drawer*) com suas
métricas, as associações mais fortes (NPMI), trechos da tese e os capítulos em
que ele aparece. O painel é **redimensionável**: arraste a alça na sua borda
esquerda para alargá-lo (duplo-clique restaura a largura padrão), e a largura
escolhida fica salva entre visitas.

### O peso (tamanho) dos nós é o PageRank

O tamanho de cada nó é dado **exclusivamente pelo PageRank** do termo
(`nx.pagerank(G, weight="weight", alpha=0.85)` em
[`infranodus/infranodus_cap1.py`](infranodus/infranodus_cap1.py); o raio é uma
escala de raiz quadrada do PageRank, de 3,2 a 22 px, em
[`index.html`](index.html)). PageRank mede **importância recursiva**: um termo
pesa mais não por ter muitas ligações, mas por estar ligado a outros termos que
também são importantes — ponderado pelo peso das arestas (co-ocorrência em janela
de 4 palavras, com mais peso para pares mais próximos). O PageRank também governa
o tamanho do rótulo e a repulsão do nó no layout.

As demais métricas exibidas no painel do termo — **grau** (soma dos pesos de
co-ocorrência), **betweenness** (ponte entre assuntos) e **frequência** — são
calculadas, mas **não** definem o tamanho do nó. Quais termos viram nós é
decidido pela poda: mantêm-se os ~180 mais frequentes, removem-se as arestas
fracas e fica-se com o maior componente conexo.

### Peso ≠ comunidade: a curadoria do agrupamento bibliométrico

Vale distinguir duas camadas independentes: o **peso** de um nó (PageRank, acima)
e a **comunidade** (cor/agrupamento) a que ele pertence (Louvain). A inserção da
análise bibliométrica atua **apenas na segunda** — ela reagrupa termos, não muda
o peso de ninguém.

O vocabulário bibliométrico (`capes`, `producao`, `distribuicao`, `frequencia`,
`area`, `base`, `corpus`, `brasileira`) já estava na rede como nós e com seu
tamanho próprio (PageRank), mas o Louvain o **dispersava** pelos demais
agrupamentos em vez de isolá-lo. Por curadoria
([`carve_bibliometric_territory`](infranodus/tese_network.py)), esses termos são
retirados das comunidades onde caíram e reunidos em um agrupamento dedicado —
**"Bibliometria · panorama do campo"** — desde que ao menos três deles estejam
presentes (caso contrário, não se força o agrupamento, para não criar um polo
artificial). Ou seja: a inserção bibliométrica mudou **a que cor** esses termos
pertencem, não **o tamanho** deles.

## Identidade visual: a sintaxe LaTeX é proposital

Os títulos e subtítulos do site são escritos na **sintaxe de comandos LaTeX**
(`\title{…}`, `\chapter{…}`, `\section{…}`, `\subsection{…}`), com a estética
do editor onde a tese é escrita — comandos e chaves em **azul neon**, texto do
autor em **preto**, tudo **monoespaçado**, como no Overleaf. Isso não é
decoração: é uma escolha que **marca três coisas ao mesmo tempo**:

1. **O Overleaf / o LaTeX** como o ambiente material em que a tese é, de fato,
   escrita e composta — a infraestrutura técnica fica à vista, não escondida.
2. **O próprio conceito de _tecnografia_** que a tese propõe e desenvolve:
   descrever práticas tecnocientíficas sem apagar a técnica que as sustenta.
   A interface pratica o que a tese argumenta.
3. **A lógica de "chamada" do LaTeX**, transposta para o site. Em LaTeX, um
   comando como `\chapter{…}` *chama* e estrutura um trecho do documento. Aqui,
   transpondo essa lógica, os comandos **chamam a própria tese**: `\title{…}`
   chama o trabalho, `\chapter{…}` os capítulos, `\section{…}` as seções,
   `\subsection{…}` as subseções, `\palavraschave{…}` as palavras-chave — e
   `\url{…}` os mapas de cada capítulo.

Convenção de cores (estilo editor LaTeX):

| Elemento | Estilo |
| --- | --- |
| Sintaxe LaTeX (comando + chaves) | azul neon, monoespaçado, sem negrito |
| Texto do autor (argumento) | preto, monoespaçado, sem negrito |
| Título do trabalho | preto, monoespaçado, **negrito** |

A tela de abertura reforça a metáfora ao apresentar a capa como o preâmbulo de
um documento: `\documentclass[doutorado]{tese}`, `\title{…}`, `\author{…}`,
`\begin{document}`.

## Figuras sincronizadas da tese

As figuras exibidas no site são sincronizadas a partir dos arquivos da tese e
versionadas por hash de conteúdo (cache-busting), para que atualizações na tese
se reflitam aqui sem cache obsoleto. Detalhes em
[`docs/sync-figuras-tese.md`](docs/sync-figuras-tese.md) e no script
[`scripts/cache_busting_figuras.py`](scripts/cache_busting_figuras.py).

## Estrutura

- `index.html` — o site (rede textual + modal da tese).
- `figuras/` — figuras da tese exibidas nas galerias por capítulo.
- `audio/` — gravação de voz do capítulo 4 (SPIRA).
- `infranodus/` — análise de rede textual e materiais de apoio.
- `docs/` — documentação de manutenção (sincronização de figuras, setup etc.).
  Veja [`docs/COMO-RODAR.md`](docs/COMO-RODAR.md) para rodar as análises e atualizar o site manualmente.
  Para regenerar **todas** as análises (site + bibliometrias + figurações), veja [`docs/ATUALIZAR-TUDO.md`](docs/ATUALIZAR-TUDO.md).
- `scripts/` — utilitários (cache-busting das figuras).

## Uso de inteligência artificial generativa

Desenvolvi o site e o *pipeline* da rede textual da tese (`infranodus/`) com o Claude Code. O Claude Code é a interface de linha de comando da Anthropic que dá ao modelo de linguagem acesso aos arquivos do projeto, para ler, escrever e executar *scripts*. Com ele escrevi os *scripts* de co-ocorrência, NPMI, Louvain, PageRank e trajetória lexical, a página `index.html` e a sincronização das figuras com o repositório da tese. Os *commits* de autor `github-actions[bot]` são regenerações automáticas da rede disparadas por atualizações do texto da tese. São minhas a escolha das métricas, a leitura das redes e a interpretação que delas faço nos capítulos.

**Modelos registrados no histórico de versões:** Claude Opus 4.8 (junho e julho de 2026), Claude Opus 5.5 e Claude Sonnet 5.5 (outubro de 2026). Parte do *pipeline* foi escrita no repositório da tese antes de vir para este.

**Sobre o autor `Claude` e a linha `Co-Authored-By: Claude …` nos *commits*.** Os *commits* com autor `Claude`, ou com essa linha no fim da mensagem, foram feitos em sessões do Claude Code. A marcação é gerada pela própria ferramenta e funciona como registro técnico de rastreabilidade: indica em que pontos do histórico o modelo de linguagem participou do trabalho. A autoria e a responsabilidade pelo conteúdo deste repositório são minhas. Conforme a Deliberação CONSU-A-005/2026 da Unicamp, as ferramentas de IA generativa não figuram como coautoras.

A declaração formal de uso de IA generativa da tese, no modelo da Pró-Reitoria de Pós-Graduação da Unicamp, está no [Anexo 1 da tese](https://github.com/julianehelanski/tecno-etnografia-centro-ia/blob/main/ex_ane1.tex). Este texto também serve à descrição do depósito no Repositório de Dados de Pesquisa da Unicamp (REDU).
