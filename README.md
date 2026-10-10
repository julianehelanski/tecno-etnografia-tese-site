# Rede textual da tese

Este repositório reúne o *pipeline* de análise de rede textual e o site que acompanham a minha tese de doutorado, *Tecnografias de um centro de inteligência artificial: seguindo cientistas e engenheiros universidade afora* (Programa de Pós-Graduação em Ciências Sociais, IFCH, Unicamp, 2026). O *pipeline* lê o código-fonte LaTeX da tese (repositório [`tecno-etnografia-centro-ia`](https://github.com/julianehelanski/tecno-etnografia-centro-ia)) e transforma o próprio texto em inscrições: redes de co-ocorrência de termos e trajetórias dos conceitos ao longo da leitura. O site publica essas redes junto com o resumo, o sumário comentado e as galerias de figuras de cada capítulo.

## O que fiz

Escrevi um *pipeline* que aplica ao texto da tese o tipo de operação que a tese descreve no campo, a passagem de um material a uma inscrição que circula:

- **Rede textual.** Depois de retirar os comandos LaTeX e lematizar o texto (com as notas de rodapé reincorporadas), ligo os termos que coocorrem numa janela deslizante de quatro *tokens*, com pesos decrescentes pela distância (3, 2, 1). A rede mantém os termos mais frequentes no maior componente conexo; as comunidades de termos são detectadas por Louvain ponderado e a força das associações é medida pelo NPMI (*normalized pointwise mutual information*). No site, o tamanho dos nós é dado pelo PageRank; nas figuras da tese, pelo grau ponderado ou pelo PageRank, conforme a vista. Faço isso para a tese inteira e para cada capítulo, com comunidades recalculadas dentro de cada um. O agrupamento do vocabulário bibliométrico numa comunidade própria é uma curadoria minha, documentada em `rede_textual/tese_network.py`.
- **Trajetória narrativa.** Divido cada capítulo pela ordem dos parágrafos e produzo três vistas diacrônicas: o Gantt lexical (entrada, permanência e saída dos conceitos), o fluxo aluvial (termos dominantes em cada trecho) e a trajetória semântica (os momentos do capítulo projetados num plano por TF-IDF, LSA e PCA).
- **Site.** `index.html` apresenta a rede da tese e de cada capítulo, com painel por termo (métricas, associações e trechos da tese), e uma aba com o resumo, o sumário, as figuras e as referências citadas, tudo extraído do `.tex`.

Os parâmetros exatos estão em [`docs/PARAMETROS.md`](docs/PARAMETROS.md) e uma visão geral do método em [`docs/VISAO-GERAL.md`](docs/VISAO-GERAL.md).

## O que entra na tese

As inscrições do próprio texto entram nos capítulos 1 a 4, cada um com a sua rede textual completa, o núcleo da rede, o núcleo ponderado por PageRank e NPMI, e as três vistas de trajetória; no capítulo 1 elas abrem a discussão sobre tecnografia. As considerações finais trazem a rede da tese inteira (`figuras/rede_tese_inteira.png`, gerada por `rede_textual/render_tese_network_figura.py`). As interpretações que escrevi das redes de cada capítulo estão em `rede_textual/interpretation_cap*.md`.

A correspondência figura a figura está em [`docs/USO_NA_TESE.md`](docs/USO_NA_TESE.md) (versão tabular em [`docs/uso_na_tese.csv`](docs/uso_na_tese.csv)). As demais imagens de `figuras/` espelham as figuras da tese para as galerias do site.

## Como reproduzir

```bash
git clone https://github.com/julianehelanski/tecno-etnografia-tese-site.git
cd tecno-etnografia-tese-site
git clone https://github.com/julianehelanski/tecno-etnografia-centro-ia.git _tex
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONHASHSEED=0                         # saída determinística

python rede_textual/run_all.py --source-root _tex                                # redes e trajetórias por capítulo
python rede_textual/tese_network.py --source-root _tex --inject index.html       # rede da tese
python rede_textual/tese_network_chapters.py --source-root _tex --inject index.html
```

O roteiro completo, com a sincronização das figuras e a publicação do site, está em [`docs/COMO-RODAR.md`](docs/COMO-RODAR.md). O mesmo fluxo roda no GitHub Actions (`.github/workflows/analyze.yml`) quando o texto da tese é atualizado, e o site é publicado pelo GitHub Pages (`pages.yml`); os *commits* de autor `github-actions[bot]` são essas regenerações automáticas.

## Estrutura

```
index.html      o site (rede textual e aba da tese)
rede_textual/     pipeline de rede textual e de trajetória, resultados por capítulo (cap1 a cap4)
figuras/        figuras da tese exibidas nas galerias
audio/          gravações do dataset SPIRA tocadas na galeria do capítulo 4
scripts/        sincronização de figuras com a tese e cache-busting
docs/           parâmetros, visão geral, roteiros de execução e uso na tese
```

## Uso de inteligência artificial generativa

Fiz o site e o *pipeline* da rede textual com o Claude Code. O Claude Code é a interface de linha de comando da Anthropic que dá ao modelo de linguagem acesso aos arquivos do projeto, para ler, escrever e executar *scripts*. Com ele escrevi os *scripts* de co-ocorrência, NPMI, Louvain, PageRank e trajetória, a página `index.html` e a sincronização das figuras com o repositório da tese. São minhas a escolha das métricas, a leitura das redes e a interpretação que delas faço nos capítulos.

**Modelos registrados no histórico de versões:** Claude Opus 4.8, Claude Opus 5.5 e Claude Sonnet 5.5 (junho a outubro de 2026). Parte do *pipeline* foi escrita no repositório da tese antes de vir para este.

Os *commits* com autor `Claude`, ou com a linha `Co-Authored-By: Claude …`, foram feitos em sessões do Claude Code; a marcação é gerada pela ferramenta e registra em que pontos do histórico o modelo participou do trabalho. A autoria e a responsabilidade pelo conteúdo são minhas e, conforme a Deliberação CONSU-A-005/2026 da Unicamp, as ferramentas de IA generativa não figuram como coautoras. A declaração formal de uso de IA generativa da tese está no [Anexo 1](https://github.com/julianehelanski/tecno-etnografia-centro-ia/blob/main/ex_ane1.tex).

## Licença

Código sob licença [MIT](LICENSE); redes, tabelas e figuras que produzi sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.pt-br), conforme [`LICENSE-DADOS.md`](LICENSE-DADOS.md), que lista as exceções (texto da tese reproduzido no site, gravações do SPIRA, imagens de terceiros, fontes e bibliotecas).

## Citação

> CARDOSO, Juliane Cristina Helanski. *Rede textual da tese*: *pipeline* e site. Campinas: Unicamp, 2026. Disponível em: https://github.com/julianehelanski/tecno-etnografia-tese-site.

> CARDOSO, Juliane Cristina Helanski. *Tecnografias de um centro de inteligência artificial*: seguindo cientistas e engenheiros universidade afora. Orientadora: Maria Suely Kofes. 2026. Tese (Doutorado em Ciências Sociais) – Instituto de Filosofia e Ciências Humanas, Universidade Estadual de Campinas, Campinas, 2026.

ORCID da autora: https://orcid.org/0000-0001-8649-8986.

Metadados de citação em [`CITATION.cff`](CITATION.cff).
