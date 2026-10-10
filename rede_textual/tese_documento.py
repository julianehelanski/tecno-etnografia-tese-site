#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tese_documento.py
=================
Extrai do `.tex` da tese os "paratextos" para apresentar na defesa:
resumo (PT), palavras-chave, sumário (capítulos · seções · subseções,
com um breve resumo por capítulo e uma nota por seção), lista de
ilustrações e lista de tabelas. Exporta JSON e, opcionalmente, reinjeta
num HTML (<script id="docdata">).

Uso:
    python3 rede_textual/tese_documento.py --source-root /tmp/tese --inject index.html
"""
import argparse
import json
import re
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR.parent / "scripts"))
from relatorio_divergencia_tese import clean_title, _match_brace_arg  # noqa: E402

# Síntese para a banca, ancorada no Resumo e nas Considerações Finais (cap.5).
# Curada (não gerada): revise/ajuste se quiser outra ênfase.
TESE = {
    "tema": "Faço da pesquisa em inteligência artificial meu objeto "
            "etnográfico: uma prática tecnocientífica situada, que descrevo "
            "pela tecnografia do C4AI, o Centro de Inteligência Artificial "
            "da USP, seguindo cientistas e engenheiros universidade afora.",
    "objeto": "Cada capítulo corta um objeto etnográfico próprio: a própria "
              "pesquisa como prática composta, humana e além de humana "
              "(cap. 1); a obra de Latour e o campo brasileiro de estudos de IA "
              "nas ciências humanas (cap. 2); o arranjo "
              "USP · FAPESP · IBM que sustentou o C4AI, da fundação (2020) à "
              "dissolução da parceria (2025) (cap. 3); e a rede que se "
              "ata em torno do SPIRA, da voz de pacientes hospitalizados com "
              "Covid-19 à detecção de insuficiência respiratória pela rede "
              "neural (cap. 4).",
    "pergunta": "Onde está o laboratório de IA e onde estão os seus cientistas? "
                "O que cientistas e engenheiros fazem quando desenvolvem "
                "inteligência artificial?",
    "objetivo": "Descrevo o arranjo das práticas tecnocientíficas da rede "
                "sociotécnica do C4AI e analiso como o plano "
                "institucional-corporativo e o plano técnico-situado se "
                "articulam na produção de conhecimento em IA e na produção de "
                "conhecimento sobre IA pelas ciências sociais.",
    "questoes": [
        "Como se faz IA, na prática, num centro de pesquisa?",
        "Como um arranjo público-privado nasce, funciona e se dissolve?",
        "Como a voz de um paciente se converte em dado e em classificação pela "
        "rede neural, e o que se perde nessa cadeia de inscrições?",
        "Que vocabulário (figurações) descreve a tecnociência sem denunciá-la "
        "nem celebrá-la?",
    ],
    "conclusao": "Fazer IA é fazer tecnociência: construir fatos e, ao mesmo "
                 "tempo, sustentar as redes que os tornam possíveis. O "
                 "computador é o próprio laboratório, e a tecnociência da IA se "
                 "faz distribuída, sobre infraestrutura computacional que poucos "
                 "atores no mundo detêm. As redes que pareciam estáveis "
                 "mostraram-se composições precárias: a falha de generalização "
                 "do SPIRA e a dissolução da parceria IBM-C4AI (dez. 2025) "
                 "tornaram visível essa fragilidade.",
    "contribuicoes": [
        "Empírica — o registro etnográfico do ciclo completo de uma parceria "
        "público-privada em IA no Brasil, do nascimento à dissolução, com "
        "relatórios não-públicos e entrevistas que preservam a ciência em "
        "construção.",
        "Metodológica — as quatro lições que retiro do Capítulo 1, a proposta "
        "da tecnografia (conceito que nasceu como tecnoetnografia e que "
        "renomeei no encontro com a antropologia da técnica) e o uso das notas "
        "de rodapé como dispositivo teórico-metodológico.",
        "Analítica — o conceito de inscrição tecnográfica, a leitura do SPIRA "
        "como objeto fracional (Mol/Law), a descrição da IA generativa como "
        "mediador não determinista, cuja resposta se enacta a cada uso situado, "
        "e o tecnopoder (termo que tomo de Brennan e desloco para o material do "
        "Capítulo 3).",
    ],
    "desdobramentos": [
        "A reconfiguração da rede após o encerramento da parceria C4AI-IBM "
        "(dez. 2025): como se redistribuem recursos, competências e vínculos "
        "quando um arranjo desse porte se desfaz.",
        "O lugar da universidade pública na pesquisa em IA quando o "
        "conhecimento de ponta migra para as corporações: sob quais arranjos, "
        "com quais salvaguardas e em direção a quais finalidades se firmam os "
        "vínculos com quem detém a infraestrutura computacional (do Arandu ao "
        "JAIRU, inaugurado em fev. 2026), pergunta que um retorno ao campo, "
        "com a continuação do SPIRA-BM, talvez me deixe seguir.",
        "O vocabulário crítico que as ciências humanas e sociais brasileiras "
        "ainda constroem para descrever a IA, o campo em formação que meu "
        "mapeamento bibliométrico registrou.",
        "O que o não determinismo da IA generativa significa para a pesquisa e "
        "o ensino: regimes de declaração e auditabilidade, letramento técnico "
        "nas ciências sociais e a desigualdade epistêmica entre acessos.",
    ],
}

# Curadoria de títulos e notas de seção. A extração vem do .tex; estes itens
# foram revisados para o site e ainda divergem do texto da tese. Cada entrada
# mapeia o texto extraído → o texto que vai ao ar. Quando o .tex for
# atualizado, a chave deixa de casar e a entrada pode sair daqui (o
# --relatorio-curadoria lista as que já não casam com nada).
CURADORIA = {
    "ex_cap1.tex": {
        # notas de seção (1ª frase extraída)
        "Antes de entrar em campo, situo o leitor sobre o que vai encontrar "
        "neste capítulo 1.":
            "Antes de entrar em campo, situo quem me lê sobre o que vai "
            "encontrar neste capítulo 1.",
        "Direct access to anything is not in the power of “humans” souls and "
        "machinery.":
            "Direct access to anything is not in the power of human souls and "
            "machinery.",
        "Este capítulo funcionou como laboratório de suas próprias decisões.":
            "Fiz deste capítulo o laboratório de suas próprias decisões, e o "
            "que o sustenta é, antes de teórico, etnográfico.",
        # títulos de subseção
        "Compostando o método: acompanhar a pesquisa em IA enquanto ciência "
        "em construção":
            "Compostando o método: acompanhar a pesquisa em IA como ciência "
            "em construção",
        "Do princípio de simetria às existências parciais":
            "Simetria e existências parciais",
        "Multiplicidades ontológicas e a especificidade de claude":
            "Multiplicidades ontológicas e a especificidade da inteligência "
            "artificial generativa",
        "Por que fazer parentesco com este problema?":
            "Por que ficar com este problema?",
        "Tecnografia": "Tecnografias",
    },
    "ex_cap2.tex": {
        # notas que a extração cortava em 180 caracteres: as versões curadas
        # fecham a frase em vez de reticências.
        "A figuração militar-industrial é um ponto sensível na escrita de "
        "Latour, e isso se torna mais explícito quando deixo de apoiá-la "
        "apenas na leitura de passagens que escolhi citar d…":
            "A figuração militar-industrial é um ponto sensível na escrita de "
            "Latour, e isso se torna mais explícito quando deixo de apoiá-la "
            "apenas na leitura de passagens que escolhi citar dele.",
        "Isso se torna uma estrutura complexa de cadeias de fornecimento "
        "dentro de cadeias de fornecimento, um zoom fractal de dezenas de "
        "milhares de fornecedores, milhões de quilômetros d…":
            "Isso se torna uma estrutura complexa de cadeias de fornecimento "
            "dentro de cadeias de fornecimento, um zoom fractal de dezenas de "
            "milhares de fornecedores, milhões de quilômetros de estradas.",
        "Abri o capítulo 2 com duas epígrafes e duas figuras postas lado a "
        "lado, a do exército de aliados de Latour e a do berço de gato de "
        "Haraway, porque em Haraway a figuração propõe e…":
            "Abri o capítulo 2 com duas epígrafes e duas figuras postas lado a "
            "lado, a do exército de aliados de Latour e a do berço de gato de "
            "Haraway, porque em Haraway a figuração propõe mundos.",
    },
    "ex_cap3.tex": {
        # epígrafe: fecho pelo texto exato do .tex (é citação).
        "Terceiro princípio: Nunca somos postos diante da ciência, da "
        "tecnologia e da sociedade, mas sim diante de uma gama de associações "
        "mais fracas e mais fortes, portanto, entender o q…":
            "Terceiro princípio: Nunca somos postos diante da ciência, da "
            "tecnologia e da sociedade, mas sim diante de uma gama de "
            "associações mais fracas e mais fortes, portanto, entender o que "
            "são fatos e máquinas é o mesmo que entender o que as pessoas são.",
        "Seguir os atores do modo que descrevi me levou a uma pergunta que "
        "organiza a reconstrução histórica deste capítulo, a de como a IBM "
        "compôs, ao longo do tempo, o ecossistema de ino…":
            "Seguir os atores do modo que descrevi me levou a uma pergunta que "
            "organiza a reconstrução histórica deste capítulo, a de como a IBM "
            "compôs, ao longo do tempo, o ecossistema de inovação que tornou "
            "possível o C4AI.",
    },
    "ex_cap4.tex": {
        # duas epígrafes: fecho pelo texto exato do .tex (são citações).
        "Cada elemento pertence à matéria por sua origem e à forma por sua "
        "destinação; é abstraído de um domínio excessivamente concreto antes "
        "de tornar-se, na etapa seguinte, excessivamen…":
            "Cada elemento pertence à matéria por sua origem e à forma por sua "
            "destinação; é abstraído de um domínio excessivamente concreto "
            "antes de tornar-se, na etapa seguinte, excessivamente concreto "
            "outra vez.",
        "Os fenômenos não se acham no ponto de encontro entre as coisas e as "
        "formas da mente humana; os fenômenos são aquilo que circula ao longo "
        "da cadeia reversível de transformação, per…":
            "Os fenômenos não se acham no ponto de encontro entre as coisas e "
            "as formas da mente humana; os fenômenos são aquilo que circula ao "
            "longo da cadeia reversível de transformação, perdendo a cada etapa "
            "algumas propriedades a fim de ganhar outras que as tornem "
            "compatíveis com os centros de cálculo já instalados.",
        "A heterogeneidade constitutiva do Spira, pausas na fala, ruídos de "
        "enfermaria, celulares, máscaras de proteção, fonoaudiólogos, médicos, "
        "linguistas, pacientes, equações matemática…":
            "A heterogeneidade constitutiva do Spira: pausas na fala, ruídos de "
            "enfermaria, celulares, máscaras de proteção, fonoaudiólogos, "
            "médicos, linguistas, pacientes, equações matemáticas.",
    },
}


# Apresentação e Considerações finais não têm \section no .tex, e a extração
# vem vazia. As seções abaixo são curadas e entram no lugar dela.
SECOES_CURADAS = {
    "ex_cap0.tex": [
        {"t": "Como cheguei aqui", "subs": [], "nota":
         "Em março de 2022 fiz minha primeira visita ao C4AI, o Centro de "
         "Inteligência Artificial da USP, no InovaUSP. Cheguei por acaso: a IA "
         "não estava no meu projeto inicial de doutorado, e foi a notícia da "
         "inauguração do Centro, enviada por um amigo, que me levou a escrever "
         "para João, coordenador do OBIA, e a entrar em campo."},
        {"t": "A pergunta que abre a tese", "subs": [], "nota":
         "Naquela visita, procurei o laboratório e encontrei uma sala de "
         "máquinas: uma parede de vidro expondo estações vazias, e, atrás de "
         "outra porta, as GPUs enfileiradas, sem cientistas entre elas. João me "
         "disse que não era ali o laboratório. Desse desencontro entre o que eu "
         "esperava ver e o que o campo me dava a ver nasceu a pergunta que "
         "carrego pela tese inteira: onde está o laboratório de IA e onde estão "
         "os seus cientistas? Oito meses depois, o lançamento do ChatGPT "
         "tornava a IA um fenômeno de massa sem alterar a rotina silenciosa do "
         "Centro, e isso só intensificou o estranhamento da pergunta."},
        {"t": "O que proponho", "subs": [], "nota":
         "Chamo esta tese de uma tecnografia: um conceito que se constitui no "
         "próprio gesto de pôr em relação o campo, a teoria, minhas memórias de "
         "pesquisa e os modelos de linguagem junto aos quais faço esta tese, e "
         "não um "
         "método trazido pronto para aplicar. O nome teve uma primeira forma, "
         "tecno-etnografia, e a contração para tecnografia pertence ao mesmo "
         "percurso em que o conceito se fez. Desse gesto de pôr em relação "
         "decorre a coexistência de duas figurações que atravessa a tese: penso "
         "o argumento por uma figuração têxtil (fios, tramas, costuras, nós e "
         "cortes) e ao mesmo tempo inscrevo o percurso em diagramas e mapas, "
         "que relacionam numa superfície plana. Habito essa tensão sem reduzir "
         "uma à outra."},
        {"t": "O percurso dos capítulos", "subs": [], "nota":
         "Sigo cientistas e engenheiros em ação, universidade afora, variação "
         "que faço do subtítulo de Ciência em Ação. Meu campo vai de março de "
         "2022 a dezembro de 2025; o período anterior à minha entrada "
         "reconstruo por relatórios e entrevistas, e é como reconstrução que "
         "ele entra na tese. A ordem dos quatro capítulos é proposta "
         "argumentativa: os capítulos 1 e 2 fazem o trabalho reflexivo sobre o "
         "vocabulário com que se descreve a tecnociência, antes que os "
         "capítulos 3 e 4 descrevam etnograficamente o C4AI e o SPIRA, para não "
         "naturalizar de antemão a figuração da tecnociência como combate. A "
         "parceria C4AI-IBM chegou ao fim enquanto eu concluía a escrita, o que "
         "tornou esta tese o registro de uma trajetória completa, da fundação "
         "(out. 2020) à dissolução (dez. 2025)."},
    ],
    "ex_cap5.tex": [
        {"t": "O que sustento no fechamento", "nota": "", "subs": []},
        {"t": "A coexistência de duas figurações", "subs": [], "nota":
         "Penso o argumento pela figuração têxtil, feita de fios, tramas, "
         "costuras e cortes, que trabalha no tempo e na espessura do "
         "pensamento; e inscrevo o percurso em diagramas e mapas, que põem em "
         "relação numa superfície plana, na simultaneidade do que se apreende "
         "de um só golpe de vista. Pratica-se a urdidura, mostra-se a trama. "
         "Habito essa tensão e a deixo aberta."},
        {"t": "A IA generativa como mediador não determinista", "subs": [],
         "nota":
         "Descrevo o claude e o claude code como mediadores, não como "
         "instrumentos neutros, e preciso o que os distingue dos sistemas que a "
         "teoria ator-rede descreveu: a mesma entrada pode devolver saídas "
         "diferentes, e a resposta não preexiste à pergunta, mas se enacta a "
         "cada uso situado (Mol). O que permanece meu, e não cedo, é o gesto de "
         "ler o que voltou, decidir o que significa e responder por isso."},
        {"t": "A recursividade da tese", "subs": [], "nota":
         "Ao seguir uma tecnociência que se faz no computador e com "
         "infraestrutura compartilhada, fiz eu mesma a pesquisa no computador, "
         "junto aos modelos de linguagem: revisei o texto junto ao claude, "
         "produzi as análises lexicométrica e bibliométrica junto ao claude "
         "code, montei os diagramas e o site. A tese tornou-se uma inscrição "
         "tecnocientífica entre as que descrevo, e é isso que a faz "
         "tecnografia: uma pesquisa sobre a produção de conhecimento em IA que "
         "se fez ela própria com IA."},
        {"t": "A trajetória do nome", "subs": [], "nota":
         "O conceito nasceu filiado à etnografia digital como tecno-etnografia, "
         "encontrou nas leituras a linhagem da cadeia operatória que guardava a "
         "palavra tecnografia, e contraiu-se sobre a grafia que as duas "
         "filiações partilham. A própria decisão de renomear foi tomada junto "
         "ao claude, e por isso a assumo como decisão tecnográfica."},
        {"t": "Curadoria e automatização graduada", "subs": [], "nota":
         "Deleguei tarefas delimitadas e retive comigo a curadoria das fontes, "
         "as relações entre teoria e campo e a decisão sobre o que importa. "
         "Montei também um caminho para refazer todas as análises na minha "
         "máquina, sem IA, porque a automação executa os scripts que escrevi, e "
         "não acrescenta nada de novo."},
        {"t": "As questões que carrego para fora", "nota": "", "subs": []},
        {"t": "A reconfiguração do arranjo após dezembro de 2025", "subs": [],
         "nota":
         "Como se redistribuem recursos, competências e vínculos quando uma "
         "parceria desse porte se desfaz, por vias que o corte nos porta-vozes "
         "do C4AI não alcança."},
        {"t": "O vocabulário crítico do campo brasileiro", "subs": [], "nota":
         "O vocabulário crítico que as ciências humanas e sociais brasileiras "
         "ainda constroem para descrever a IA, o campo em formação que meu "
         "mapeamento bibliométrico registrou."},
        {"t": "O lugar da universidade pública", "subs": [], "nota":
         "Quando o conhecimento de ponta migra para as corporações: sob quais "
         "arranjos, com quais salvaguardas e em direção a quais finalidades se "
         "firmam os vínculos com quem detém a infraestrutura computacional, do "
         "Arandu (8 GPUs, 2022) ao JAIRU (96 GPUs, fev. 2026), pergunta que a "
         "continuação do SPIRA-BM talvez me deixe seguir."},
        {"t": "O que o não determinismo significa para a pesquisa e o ensino",
         "subs": [], "nota":
         "Se a saída se enacta a cada uso, quem está diante da mesma plataforma "
         "não está diante do mesmo objeto, e é a prática, não a plataforma, o "
         "que resta avaliável. Daí as perguntas que deixo em suspenso, sobre "
         "regimes de declaração e de auditabilidade, sobre o letramento técnico "
         "que as ciências sociais podem construir sem ceder a régua crítica que "
         "as constitui, e sobre a desigualdade epistêmica entre quem acessa a "
         "IA paga e quem acessa a gratuita."},
        {"t": "O que a aceleração faz ao pensar", "subs": [], "nota":
         "A facilidade que a IA oferece repousa na mesma cadeia extrativa que "
         "descrevo, e a produtividade que promete pode embotar as fricções de "
         "que o pensamento se alimenta. Fico com esse problema no registro do "
         "lento, pero avanzo, o lema do caracol zapatista da dedicatória."},
        {"t": "Arremate", "subs": [], "nota":
         "No centro do grafo de co-ocorrência de toda a tese está rede, o termo "
         "de maior grau (degree) e a maior ponte, e nele se encontram os dois "
         "sentidos "
         "que mantive lado a lado: a rede sociotécnica que descrevi e a análise "
         "de rede que pratiquei. O vocabulário de método é o mais enxuto e o "
         "mais central; os objetos empíricos ocupam as comunidades maiores. "
         "Esta tese é a rede distribuída e dependente de infraestrutura que "
         "descrevi no C4AI, e partilha a sua condição: uma rede não é forte por "
         "ser extensa, porque cada elo a mais é mais um a manter. Existe "
         "enquanto as suas conexões forem mantidas, e segue também em outra "
         "superfície, a da rede textual navegável no site que a apresenta."},
    ],
}

_CURADORIA_USADA: set[tuple[str, str]] = set()


def curar(fname: str, texto: str) -> str:
    """Aplica a curadoria de título/nota, quando houver, ao texto extraído."""
    novo = CURADORIA.get(fname, {}).get(texto)
    if novo is None:
        return texto
    _CURADORIA_USADA.add((fname, texto))
    return novo


def avisar_curadoria_obsoleta() -> None:
    """Avisa sobre entradas que já não casam com o .tex (tese atualizada)."""
    for fname, mapa in CURADORIA.items():
        for chave in mapa:
            if (fname, chave) not in _CURADORIA_USADA:
                print(f"[doc] curadoria sem correspondência em {fname}: "
                      f"{chave[:70]!r} — o .tex mudou? revise CURADORIA.")


# capítulo: (arquivo, número, título, resumo [o que faz], conclusão [a que chega])
CHAPTERS = [
    ("ex_cap0.tex", "", "Apresentação",
     "Como cheguei ao campo, a pergunta que nasce do desencontro entre o "
     "laboratório que procurei e a sala de máquinas que encontrei, a "
     "tecnografia que proponho e o percurso dos quatro capítulos.",
     ""),
    ("ex_cap1.tex", "1", "Onde está o laboratório e os seus cientistas?",
     "Documento meu percurso pelo campo e construo o método a partir da "
     "experiência: o patchwork como figuração, as existências parciais "
     "(incluindo o fazer-com IA generativa) e a compostagem.",
     "Chego às quatro compostagens (método, teoria, letramento e política) e à "
     "proposta da tecnografia. O capítulo funciona como laboratório de suas "
     "próprias decisões: aplica à própria escrita da tese o tratamento que dou "
     "aos pesquisadores que descrevo, e entrega às tramas seguintes a "
     "consciência de que a figuração com que se descreve a tecnociência é parte "
     "do que se descreve. Fica em aberto a questão que carrego pela tese "
     "inteira: a coexistência de duas figurações, a têxtil, com que penso o "
     "argumento, e a topológica dos diagramas, com que o inscrevo, e a pergunta "
     "sobre como se mostra, numa superfície plana, um pensar que se faz por "
     "tramas."),
    ("ex_cap2.tex", "2", "Metáforas, figurações e alianças: revisão da literatura",
     "Reconstruo as alianças teóricas da tese em duas tramas: a análise "
     "lexicométrica das figurações em seis obras de Latour e o mapeamento "
     "bibliométrico do campo brasileiro de IA nas ciências humanas.",
     "Mostro que a figuração militar-industrial é situada e que o vocabulário "
     "têxtil-topológico organiza os textos metateóricos de Latour; documento um "
     "campo brasileiro em formação, onde insiro minha pesquisa."),
    ("ex_cap3.tex", "3", "A rede que Fábio e Cláudio construíram",
     "Sigo Fábio e Cláudio pela rede que sustentou o C4AI por cinco anos, dos "
     "cartões de Hollerith (1890) à genealogia da IBM e à racionalidade do "
     "ecossistema de inovação.",
     "Documento o ciclo completo da parceria (2020–2025) e descrevo o padrão de "
     "reprodução de dependências técnica e comercial que a IBM sedimentou ao "
     "longo de 135 anos, que leio na figura do tecnopoder (termo que tomo de "
     "Brennan); encerro com a dissolução IBM-C4AI (dez. 2025)."),
    ("ex_cap4.tex", "4", "A rede que Marcelo construiu",
     "Sigo Marcelo Finger pela rede do SPIRA: a cadeia de translações que "
     "converte a voz de pacientes com Covid-19 em espectrogramas processados "
     "por redes neurais, da fala ao dado à detecção de insuficiência "
     "respiratória.",
     "Mostro que o modelo (96,5% de precisão) aprendeu uma insuficiência "
     "respiratória específica ao covideiro pandêmico, e sua falha de "
     "generalização é evidência empírica da tensão ontológica (Mol). Proponho a "
     "inscrição tecnográfica."),
    ("ex_cap5.tex", "", "Considerações finais",
     "Retomo os três movimentos do método (o corte, os atores e actantes, a "
     "compostagem) e releio o C4AI e o SPIRA como a mesma rede sob cortes "
     "distintos: um a partir do arranjo institucional que torna a pesquisa "
     "possível, outro a partir das práticas situadas em que ela se faz. Reúno "
     "as contribuições e deixo abertas as questões que carrego para fora da "
     "tese.",
     "Comecei procurando um laboratório e encontrei uma sala de máquinas. O "
     "computador é o próprio laboratório de uma tecnociência distribuída, que "
     "se faz numa infraestrutura computacional que poucos atores no mundo "
     "fabricam e mantêm. As redes que pareciam estáveis mostraram-se "
     "composições precárias, e a dissolução da parceria IBM-C4AI (dez. 2025) "
     "tornou visível essa fragilidade. A própria tese, repartida entre "
     "Overleaf, GitHub e o site, partilha essa condição: existe enquanto as "
     "suas conexões forem mantidas."),
]

# título real do capítulo: primeiro \chapter{...} ou \chapter*{...} do .tex
CHAP_RE = re.compile(r'\\chapter\*?\s*(?:\[[^\]]*\])?\s*\{')


def parse_chapter_title(tex: str, fallback: str) -> str:
    """Extrai o título real do \\chapter{...} (ou \\chapter*{...}) do .tex,
    para casar com o nome oficial no documento. Cai no fallback curado se
    o comando não for encontrado."""
    m = CHAP_RE.search(tex)
    if not m:
        return fallback
    arg, _ = _match_brace_arg(tex, m.end() - 1)
    return clean_title(arg) or fallback

ENV_RE = re.compile(
    r'\\begin\{(figure|table|longtable)\*?\}'
    r'|\\end\{(figure|table|longtable)\*?\}'
    r'|\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}'
    r'|\\caption(?:\[([^\]]*)\])?\{')

SEC_RE = re.compile(r'\\(section|subsection)\*?\s*\{')

# Diagrama interativo (MermaidChart) embutido na legenda via \href{...}.
MERMAID_RE = re.compile(r'https://mermaid\.ai/d/[0-9a-fA-F-]+')

# Pasta de figuras que o SITE de fato exibe (figuras/<slug>/...).
SITE_FIGURAS = THIS_DIR.parent / "figuras"


def _site_image(texpath: str | None) -> str | None:
    r"""Mapeia o \includegraphics da tese para a figura que o site exibe.

    Hoje só as inscrições da análise de rede textual e as trajetórias
    narrativas têm cópia em figuras/<slug>/ com o nome do site. Retorna o
    caminho relativo ao repositório do site se o arquivo existir; senão None
    — mesmo princípio de sync_site_figuras.py: só mostra o que o site tem.
    """
    if not texpath:
        return None
    base = texpath.strip().replace("\\", "/").rsplit("/", 1)[-1].lower()
    # Rede textual da tese inteira (Considerações finais): cópia na raiz de figuras/.
    if base == "rede_tese_inteira.png":
        return "figuras/rede_tese_inteira.png" if (SITE_FIGURAS / base).exists() else None
    mname = re.search(r"infranodus_cap(\d+)_", base)
    mdir = re.search(r"cap\.?(\d+)", texpath)
    m = mname or mdir
    if not m:
        return None
    slug = f"cap{m.group(1)}"
    name_map = {
        f"infranodus_cap{m.group(1)}_network.png":   f"{slug}-infranodus-network.png",
        f"infranodus_cap{m.group(1)}_focus.png":     f"{slug}-infranodus-focus.png",
        f"infranodus_cap{m.group(1)}_pmi.png":       f"{slug}-infranodus-pmi.png",
        f"infranodus_cap{m.group(1)}_focus_pmi.png": f"{slug}-infranodus-pmi.png",
        "trajectory_gantt.png":                      f"{slug}-trajectory-gantt.png",
        "trajectory_alluvial.png":                   f"{slug}-trajectory-alluvial.png",
        "trajectory_semantic.png":                   f"{slug}-trajectory-semantic.png",
    }
    mapped = name_map.get(base)
    if not mapped:
        return None
    rel = f"figuras/{slug}/{mapped}"
    return rel if (SITE_FIGURAS / slug / mapped).exists() else None


def _is_continuation(s: str) -> bool:
    """Rótulo de continuação (parte seguinte de uma figura/longtable),
    que compartilha o número e não entra na lista de ilustrações."""
    return re.sub(r"[()\.\s]", "", s).lower() in (
        "continua", "continuacao", "continuação")


def _trunc(s: str, n: int = 170) -> str:
    s = s.strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def _refs_cap(s: str) -> str:
    """\\ref{capituloN} → N, como no PDF compilado (para exibição)."""
    return re.sub(r"~?\\(?:ref|cref|Cref|autoref|nameref)\{capitulo(\d+)\}", r" \1", s)


def _enquote(s: str) -> str:
    """\\enquote{x} → “x”: preserva as aspas que o PDF mostra."""
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\\enquote\*?\s*\{([^{}]*)\}", r"“\1”", s)
    return s


def _polish(s: str) -> str:
    """Acabamento tipográfico do texto extraído: travessões TeX, \\_ e espaços."""
    s = s.replace("---", "—").replace("--", "–").replace(r"\_", "_")
    s = re.sub(r"\s+([.,;:!?])", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def _pre(s: str) -> str:
    """Remove ruído de LaTeX preservando caixa, acentos e hífens (para exibição)."""
    s = _enquote(_refs_cap(s))
    s = re.sub(r"(?<!\\)%.*", "", s)                                   # comentários
    s = re.sub(r"\\(begin|end)\{[^}]*\}", " ", s)                      # ambientes
    s = re.sub(r"\\label\{[^}]*\}", " ", s)
    s = re.sub(r"\\(ref|cref|Cref|autoref|eqref|pageref|nameref)\{[^}]*\}", " ", s)
    s = re.sub(r"\\(parencite|textcite|cite[a-zA-Z]*)\*?(?:\[[^\]]*\])*\{[^}]*\}", " ", s)
    s = re.sub(r"\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}", " ", s)
    s = re.sub(r"\\footnote\{[^{}]*\}", " ", s)
    s = re.sub(r"\\(selectlanguage|setstretch|setlength)\{[^}]*\}", " ", s)
    s = re.sub(r"\\(begingroup|endgroup|noindent|large|Large|centering|small|par)\b", " ", s)
    return s


def first_sentence(tex_segment: str) -> str:
    """Primeira frase de prosa de um trecho .tex (para nota de seção)."""
    txt = _polish(clean_title(_pre(tex_segment)))
    m = re.search(r"(.+?[.!?])(\s|$)", txt)
    sent = (m.group(1) if m else txt)
    return _trunc(sent, 180)


def parse_outline(tex: str, fname: str = "") -> list[dict]:
    """Seções (com subseções e nota de 1ª frase), na ordem do documento."""
    secs: list[dict] = []
    seen = False
    matches = list(SEC_RE.finditer(tex))
    for idx, m in enumerate(matches):
        kind = m.group(1)
        arg, nxt = _match_brace_arg(tex, m.end() - 1)
        title = curar(fname, clean_title(_enquote(arg)))
        if not title:
            continue
        # trecho até o próximo section/subsection → nota (1ª frase)
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(tex)
        body = tex[nxt:end]
        # corta no primeiro ambiente para evitar legendas como "nota"
        cut = re.search(r"\\begin\{(figure|table|longtable|itemize|enumerate)", body)
        if cut:
            body = body[:cut.start()]
        nota = curar(fname, first_sentence(body))
        if kind == "section" or not seen:
            seen = seen or kind == "section"
            secs.append({"t": title, "nota": nota, "subs": []})
        else:
            if secs:
                secs[-1]["subs"].append(title)
    return secs


def parse_captions(tex: str):
    """(figuras, tabelas): legendas na ordem do documento, por ambiente."""
    figs, tabs = [], []
    stack = []
    last_img = None   # último \includegraphics do ambiente figure corrente
    for m in ENV_RE.finditer(tex):
        g = m.group(0)
        if g.startswith(r"\begin"):
            stack.append(m.group(1))
            last_img = None
        elif g.startswith(r"\end"):
            if stack:
                stack.pop()
            last_img = None
        elif g.startswith(r"\includegraphics"):
            last_img = m.group(3)
        else:  # \caption
            short = m.group(4)
            if short is not None and short.strip() == "":
                # \caption[]{...}: entrada vazia na lista de ilustrações
                # (típico de continuação de longtable) — não listar.
                continue
            arg, _ = _match_brace_arg(tex, m.end() - 1)
            cap = (_polish(clean_title(_refs_cap(short))) if short
                   else _trunc(_polish(clean_title(_refs_cap(arg)))))
            if not cap or _is_continuation(cap):
                continue
            link_m = MERMAID_RE.search(arg)
            link = link_m.group(0) if link_m else None
            env = stack[-1] if stack else "figure"
            img = None if env in ("table", "longtable") else _site_image(last_img)
            (tabs if env in ("table", "longtable") else figs).append((cap, link, img))
    return figs, tabs


def parse_resumo(src: Path):
    raw = src.read_text(encoding="utf-8")
    clean = _polish(clean_title(_pre(raw)))
    parts = re.split(r"Palavras[\s-]*chave\s*:?\s*", clean, maxsplit=1)
    resumo = re.sub(r"^Resumo\s+", "", parts[0].strip())
    palavras = []
    if len(parts) > 1:
        kw = parts[1].split(".")[0]   # só a frase das palavras-chave
        palavras = [k.strip() for k in re.split(r"[,;]", kw) if k.strip()]
    return resumo, palavras


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", type=Path, default=Path("/tmp/tese"))
    ap.add_argument("--out", type=Path, default=THIS_DIR / "tese_documento.json")
    ap.add_argument("--inject", type=Path, default=None)
    args = ap.parse_args()

    resumo, palavras = parse_resumo(args.source_root / "resumo.tex")

    sumario, figuras, tabelas = [], [], []
    fign = tabn = 0
    for fname, num, title, resumo_cap, conclusao_cap in CHAPTERS:
        src = args.source_root / fname
        if not src.exists():
            print(f"[doc] aviso: {fname} ausente, pulando.")
            continue
        tex = src.read_text(encoding="utf-8")
        sumario.append({
            "id": fname.replace("ex_", "").replace(".tex", ""),
            "num": num, "title": parse_chapter_title(tex, title),
            "resumo": resumo_cap,
            "conclusao": conclusao_cap,
            "sections": SECOES_CURADAS.get(fname) or parse_outline(tex, fname),
        })
        f, t = parse_captions(tex)
        for c, link, img in f:
            fign += 1
            entry = {"n": fign, "cap": num or title, "t": c}
            if link:
                entry["link"] = link
            if img:
                entry["img"] = img
            figuras.append(entry)
        for c, _link, _img in t:
            tabn += 1
            tabelas.append({"n": tabn, "cap": num or title, "t": c})

    avisar_curadoria_obsoleta()

    payload = {
        "tese": TESE,
        "resumo": resumo,
        "palavras_chave": palavras,
        "sumario": sumario,
        "figuras": figuras,
        "tabelas": tabelas,
    }
    data_str = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    args.out.write_text(data_str, encoding="utf-8")
    print(f"[doc] JSON: {args.out} ({args.out.stat().st_size/1024:.0f} KB) | "
          f"resumo={len(resumo)}c · {len(palavras)} palavras-chave · "
          f"{len(sumario)} capítulos · {len(figuras)} figuras · {len(tabelas)} tabelas")

    if args.inject is not None:
        assert "</script" not in data_str.lower()
        html = args.inject.read_text(encoding="utf-8")
        pat = re.compile(r'(<script type="application/json" id="docdata">).*?(</script>)', re.DOTALL)
        new, n = pat.subn(lambda m: m.group(1) + data_str + m.group(2), html, count=1)
        if n != 1:
            print(f"[doc] ERRO: <script id=docdata> não encontrado em {args.inject}")
            return 1
        args.inject.write_text(new, encoding="utf-8")
        print(f"[doc] reinjetado em {args.inject}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
