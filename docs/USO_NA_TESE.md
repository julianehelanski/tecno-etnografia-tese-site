# Relação deste repositório com a tese

Documento gerado em 09/10/2026 a partir da leitura dos arquivos `ex_cap*.tex` do repositório da tese (`julianehelanski/tecno-etnografia-centro-ia`, commit 3f0f671 (2026-10-08)). Repositório descrito: `julianehelanski/tecno-etnografia-tese-site`. A versão tabular está em `docs/uso_na_tese.csv`.

## Papel do repositório

Este repositório é derivado do repositório da tese: o pipeline em `rede_textual/` lê os arquivos `.tex` (`_tex/ex_cap*.tex`) e produz a rede textual da tese inteira e de cada capítulo (co-ocorrência em janela deslizante, peso NPMI, comunidades de Louvain, PageRank), além das figuras de trajetória (Gantt lexical, fluxo aluvial, trajetória semântica). Essas figuras entram na tese como inscrições do próprio texto (capítulos 1 a 4 e capítulo 5), e o site publica a rede, o resumo e as galerias de figuras. Os dados de entrada são o texto da tese e `rede_textual/chapters.yml`.

## Figuras da tese geradas aqui ou cuja cópia consta aqui

| Capítulo | Seção da tese | Rótulo | Arquivo no repositório | Script | Estado da cópia na tese |
|---|---|---|---|---|---|
| capítulo 1 | Tecnografias | `fig:infranodus-cap1-network` | `rede_textual/cap1/infranodus_cap1_network.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 1 | Tecnografias | `fig:infranodus-cap1-focus` | `rede_textual/cap1/infranodus_cap1_focus.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 1 | Tecnografias | `fig:infranodus-cap1-focus-pmi` | `rede_textual/cap1/infranodus_cap1_focus_pmi.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 1 | Tecnografias | `fig:trajectory-gantt` | `rede_textual/cap3/trajectory_gantt.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 1 | Tecnografias | `fig:trajectory-alluvial` | `rede_textual/cap3/trajectory_alluvial.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 1 | Tecnografias | `fig:trajectory-semantic` | `rede_textual/cap3/trajectory_semantic.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 2 | Arremate: figurações e análise computacional | `fig:infranodus-cap2-network` | `rede_textual/cap2/infranodus_cap2_network.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 2 | Arremate: figurações e análise computacional | `fig:infranodus-cap2-focus` | `rede_textual/cap2/infranodus_cap2_focus.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 2 | Arremate: figurações e análise computacional | `fig:infranodus-cap2-pmi` | `rede_textual/cap2/infranodus_cap2_focus_pmi.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 2 | Arremate: figurações e análise computacional | `fig:trajectory-cap2-gantt` | `rede_textual/cap3/trajectory_gantt.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 2 | Arremate: figurações e análise computacional | `fig:trajectory-cap2-alluvial` | `rede_textual/cap3/trajectory_alluvial.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 2 | Arremate: figurações e análise computacional | `fig:trajectory-cap2-semantic` | `rede_textual/cap3/trajectory_semantic.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 3 | (Co)relações parciais: o fim da "parceria" C4AI-IBM-FAPESP, ecossistem | `fig:infranodus-cap3-network` | `rede_textual/cap3/infranodus_cap3_network.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 3 | (Co)relações parciais: o fim da "parceria" C4AI-IBM-FAPESP, ecossistem | `fig:infranodus-cap3-focus` | `rede_textual/cap3/infranodus_cap3_focus.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 3 | (Co)relações parciais: o fim da "parceria" C4AI-IBM-FAPESP, ecossistem | `fig:infranodus-cap3-pmi` | `rede_textual/cap3/infranodus_cap3_focus_pmi.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 3 | (Co)relações parciais: o fim da "parceria" C4AI-IBM-FAPESP, ecossistem | `fig:trajectory-cap3-gantt` | `rede_textual/cap3/trajectory_gantt.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 3 | (Co)relações parciais: o fim da "parceria" C4AI-IBM-FAPESP, ecossistem | `fig:trajectory-cap3-alluvial` | `rede_textual/cap3/trajectory_alluvial.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 3 | (Co)relações parciais: o fim da "parceria" C4AI-IBM-FAPESP, ecossistem | `fig:trajectory-cap3-semantic` | `rede_textual/cap3/trajectory_semantic.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 4 | As agências do coronavírus | `fig:cadeia_inscricao_Covid_coleta` | `figuras/HIS-77-186-g004.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese diverge da do repositório |
| capítulo 4 | As agências do coronavírus | `fig:cadeia_inscricao_Covid_histologia` | `figuras/HIS-77-186-g001.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese diverge da do repositório |
| capítulo 4 | As agências do coronavírus | `fig:cadeia_inscricao_Covid_ihc` | `figuras/HIS-77-186-g002.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese diverge da do repositório |
| capítulo 4 | As agências do coronavírus | `fig:cadeia_inscricao_Covid_sistemica` | `figuras/HIS-77-186-g003.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese diverge da do repositório |
| capítulo 4 | As agências do coronavírus | `fig:gu2007_isH_ihc` | `figuras/AISelect_20260403_164426_Chrome.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese diverge da do repositório |
| capítulo 4 | Espectogramas mel: a imagem da voz | `fig:espectrograma-sem-legenda` | `figuras/spira_espectrograma_sem_legenda.png` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese diverge da do repositório |
| capítulo 4 | Espectogramas mel: a imagem da voz | `fig:espectrograma-com-eixos` | `figuras/spira_espectrograma_com_eixos.png` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese diverge da do repositório |
| capítulo 4 | O espectrograma na escrita etnográfica | `` | `figuras/juki_1.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese idêntica à do repositório |
| capítulo 4 | O espectrograma na escrita etnográfica | `` | `figuras/novel-coronavirus-sars-cov-2_49531042907_o.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese idêntica à do repositório |
| capítulo 4 | O espectrograma na escrita etnográfica | `` | `figuras/novel-coronavirus-sars-cov-2_49557550706_o.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese idêntica à do repositório |
| capítulo 4 | O espectrograma na escrita etnográfica | `` | `figuras/novel-coronavirus-sars-cov-2_49557550751_o.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese idêntica à do repositório |
| capítulo 4 | O espectrograma na escrita etnográfica | `` | `figuras/novel-coronavirus-sars-cov-2_49597020853_o.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese idêntica à do repositório |
| capítulo 4 | O espectrograma na escrita etnográfica | `` | `figuras/novel-coronavirus-sars-cov-2_49597519106_o.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese idêntica à do repositório |
| capítulo 4 | O espectrograma na escrita etnográfica | `` | `figuras/novel-coronavirus-sars-cov-2_49640655213_o.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese diverge da do repositório |
| capítulo 4 | O espectrograma na escrita etnográfica | `` | `figuras/novel-coronavirus-sars-cov-2_49641177636_o.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese idêntica à do repositório |
| capítulo 4 | O espectrograma na escrita etnográfica | `` | `figuras/novel-coronavirus-sars-cov-2_49641177821_o.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese idêntica à do repositório |
| capítulo 4 | O espectrograma na escrita etnográfica | `fig:sars-cov-2` | `figuras/novel-coronavirus-sars-cov-2_49645120251_o.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese diverge da do repositório |
| capítulo 4 | O espectrograma na escrita etnográfica | `fig:sars-cov-2` | `figuras/novel-coronavirus-sars-cov-2_49534865371_o.jpg` | figura de terceiros ou da literatura (não gerada por script do repositório) | cópia na tese idêntica à do repositório |
| capítulo 4 | Análise de rede textual do capítulo | `fig:infranodus-cap4-network` | `rede_textual/cap4/infranodus_cap4_network.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 4 | Análise de rede textual do capítulo | `fig:infranodus-cap4-focus` | `rede_textual/cap4/infranodus_cap4_focus.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 4 | Análise de rede textual do capítulo | `fig:infranodus-cap4-pmi` | `rede_textual/cap4/infranodus_cap4_focus_pmi.png` | `rede_textual/rede_textual_capitulo.py` | cópia na tese diverge da do repositório |
| capítulo 4 | Análise de rede textual do capítulo | `fig:trajectory-cap4-gantt` | `rede_textual/cap3/trajectory_gantt.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 4 | Análise de rede textual do capítulo | `fig:trajectory-cap4-alluvial` | `rede_textual/cap3/trajectory_alluvial.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 4 | Análise de rede textual do capítulo | `fig:trajectory-cap4-semantic` | `rede_textual/cap3/trajectory_semantic.png` | `rede_textual/narrative_trajectory.py` | cópia na tese diverge da do repositório |
| capítulo 5 |  | `fig:infranodus-tese` | `figuras/rede_tese_inteira.png` | `rede_textual/render_tese_network_figura.py` | cópia na tese idêntica à do repositório |

As imagens de `cap.4/covid/` (arquivos `HIS-77-186-g00*.jpg`, `novel-coronavirus-sars-cov-2_*.jpg`, `juki_1.jpg` e uma captura de tela) não são geradas por script deste repositório e têm autoria de terceiros; verificar autoria e licença de cada uma antes do depósito. As demais figuras do site (galerias) espelham a pasta `figuras/` do repositório da tese, sincronizada por `rede_textual/sync_site_figuras.py`.

