# Diagramas da tese: código-fonte Mermaid

Esta pasta guarda o código-fonte (`.mmd`) dos diagramas que fiz no [MermaidChart](https://www.mermaidchart.com/) para a tese *Tecnografias de um centro de inteligência artificial*. Exportei os arquivos da minha conta no MermaidChart em 26 de outubro de 2026. Cada `.mmd` abre no MermaidChart, no [Mermaid Live Editor](https://mermaid.live/) ou em qualquer renderizador Mermaid (os mapas de capítulo usam o *layout* `elk`).

## Organização

- `capN/`: um `.mmd` por diagrama, separados pelo capítulo da tese em que aparecem (`cap5/` reúne as Considerações finais, `ex_cap5.tex`).
- Quando o site já exibe o PNG renderizado a partir do mesmo código, o `.mmd` tem o nome desse PNG em [`figuras/`](../figuras). Nos outros casos, o `.mmd` tem o nome do PNG no repositório da tese (`tecno-etnografia-centro-ia`), sem o carimbo de data da exportação.
- Em cinco casos o site ainda exibe uma *versão anterior* do diagrama: a estrutura é a mesma, mas o estilo e o conteúdo são mais antigos. Para não sugerir que o código atual gera aquela imagem, o `.mmd` não recebe o nome do PNG antigo; a tabela indica o PNG como "versão anterior no site".

## Correspondência com as figuras da tese

Os números de figura saem da contagem das legendas (`\caption`) em `ex_cap1.tex` a `ex_cap5.tex`, conforme a numeração por capítulo da classe `book`. Confiro cada correspondência pelo *link* `mermaid.ai/d/…` que a legenda traz e pelo nome do PNG em `\includegraphics`. A última coluna abre a versão interativa citada na legenda.

| Figura nº | Capítulo | Título | `.mmd` | PNG | Versão interativa |
|---|---|---|---|---|---|
| 1.1 | Cap. 1 | Linha do tempo do capítulo 1 | [`linha-tempo-capitulo1.mmd`](cap1/linha-tempo-capitulo1.mmd) | tese: `figuras/cap.1/linha-tempo-capitulo1.png` | [abrir](https://mermaid.ai/d/b27ca78c-b037-42fe-a3eb-939a092e1455) |
| 1.2 | Cap. 1 | Mapa do capítulo 1 | [`cap1-urdidura.mmd`](cap1/cap1-urdidura.mmd) | [`figuras/cap1/cap1-urdidura.png`](../figuras/cap1/cap1-urdidura.png) | [abrir](https://mermaid.ai/d/6dbd9e0b-a652-428d-99b1-a76d0c068b5b) |
| 1.3 | Cap. 1 | Grade dos três planos | [`cap1-grade-tres-planos.mmd`](cap1/cap1-grade-tres-planos.mmd) | [`figuras/cap1/cap1-grade-tres-planos.png`](../figuras/cap1/cap1-grade-tres-planos.png) | [abrir](https://mermaid.ai/d/23442efa-7a2f-4a5e-9dae-0e2faeedc3ae) |
| 2.3 | Cap. 2 | Mapa do capítulo 2 | [`mapa-capitulo2.mmd`](cap2/mapa-capitulo2.mmd) | tese: `figuras/cap.2/diagramas/mapa-capitulo2.png`<br>versão anterior no site: [`cap2-urdidura.png`](../figuras/cap2/cap2-urdidura.png) | [abrir](https://mermaid.ai/d/b4a7d089-3a37-4ab6-8e45-fc4ecca9e22f) |
| 2.4 | Cap. 2 | Linha do tempo do capítulo 2 | [`linha-tempo-capitulo2.mmd`](cap2/linha-tempo-capitulo2.mmd) | tese: `figuras/cap.2/diagramas/linha-tempo-capitulo2.png` | [abrir](https://mermaid.ai/d/a7b611c1-a522-41da-9603-0a8be61de483) |
| 2.12 | Cap. 2 | Primeiro significado da mediação técnica: tradução de objetivos | [`mediacaosignificado_1_traducao.mmd`](cap2/mediacaosignificado_1_traducao.mmd) | tese: `figuras/cap.2/diagramas/mediacaosignificado_1_traducao.png` | [abrir](https://mermaid.ai/d/f1c51456-43c3-424c-8edf-50566fbe40c2) |
| 2.13 | Cap. 2 | Segundo significado da mediação técnica: composição | [`mediacaosignificado_2_composicao.mmd`](cap2/mediacaosignificado_2_composicao.mmd) | tese: `figuras/cap.2/diagramas/mediacaosignificado_2_composicao.png` | [abrir](https://mermaid.ai/d/050e4650-4240-4681-b65d-825c33579f58) |
| 2.14 | Cap. 2 | Terceiro significado da mediação técnica: entrelaçamento de tempo e espaço | [`mediacaosignificado_3_obscurecimento.mmd`](cap2/mediacaosignificado_3_obscurecimento.mmd) | tese: `figuras/cap.2/diagramas/mediacaosignificado_3_obscurecimento.png` | [abrir](https://mermaid.ai/d/4b90c964-c828-4b60-ba05-d9b4ee409c69) |
| 2.15 | Cap. 2 | Quarto significado da mediação técnica: delegação | [`mediacaosignificado_4_delegacao.mmd`](cap2/mediacaosignificado_4_delegacao.mmd) | tese: `figuras/cap.2/diagramas/mediacaosignificado_4_delegacao.png` | [abrir](https://mermaid.ai/d/fb8411e2-65f0-4a16-a767-fad97bf15f8f) |
| 2.16 | Cap. 2 | O diferencial da IA generativa na mediação técnica | [`cap2-mediacao-diferencial.mmd`](cap2/cap2-mediacao-diferencial.mmd) | [`figuras/cap2/cap2-mediacao-diferencial.png`](../figuras/cap2/cap2-mediacao-diferencial.png) | [abrir](https://mermaid.ai/d/9b29f69e-2c76-465a-b25f-033401bf57c5) |
| 3.1 | Cap. 3 | Mapa do capítulo 3 | [`mapa-capitulo3.mmd`](cap3/mapa-capitulo3.mmd) | tese: `figuras/cap.3/diagrama/mapa-capitulo3.png` | [abrir](https://mermaid.ai/d/0c8eb50f-d995-4bba-b60a-c768ebe5dd51) |
| 3.5 | Cap. 3 | Mapa analítico do capítulo 3: do campo à implicação | [`mapa-analitico-capitulo3.mmd`](cap3/mapa-analitico-capitulo3.mmd) | tese: `figuras/cap.3/diagrama/mapa-analitico-capitulo3-2026-07-18-220352.png`<br>versão anterior no site: [`cap3-quadro-analitico.png`](../figuras/cap3/cap3-quadro-analitico.png) | [abrir](https://mermaid.ai/d/524aeaa7-bdc0-4a59-86f8-1babbb51b23c) |
| 3.6 | Cap. 3 | Mapa metodológico do capítulo 3 | [`mapa-metodologico-capitulo3.mmd`](cap3/mapa-metodologico-capitulo3.mmd) | tese: `figuras/cap.3/diagrama/mapa-metodologico-capitulo3.png`<br>versão anterior no site: [`cap3-seguindo-atores.png`](../figuras/cap3/cap3-seguindo-atores.png) | [abrir](https://mermaid.ai/d/1e91bd86-5adf-4ac9-8267-5e2c0ef106a2) |
| 3.7 | Cap. 3 | Mapa das associações do capítulo 3 | [`mapa-associacoes-capitulo3.mmd`](cap3/mapa-associacoes-capitulo3.mmd) | tese: `figuras/cap.3/diagrama/mapa-associacoes-capitulo3.png` | [abrir](https://mermaid.ai/d/5489d21c-59fe-4af5-88e2-266248114a98) |
| 3.8 | Cap. 3 | Linha do tempo do capítulo 3 (1890–2025) | [`linha-tempo-capitulo3.mmd`](cap3/linha-tempo-capitulo3.mmd) | tese: `figuras/cap.3/diagrama/linha-tempo-capitulo3.png` | [abrir](https://mermaid.ai/d/0ef94ec0-258e-470f-83b5-cd07c511f760) |
| 3.9 | Cap. 3 | Mapa da rede sociotécnica do sistema de Hollerith | [`mapa-rede-hollerith-capitulo3.mmd`](cap3/mapa-rede-hollerith-capitulo3.mmd) | tese: `figuras/cap.3/diagrama/mapa-rede-hollerith-capitulo3.png`<br>versão anterior no site: [`cap3-hollerith-rede-sociotecnica.png`](../figuras/cap3/cap3-hollerith-rede-sociotecnica.png) | [abrir](https://mermaid.ai/d/58220d39-fbdc-41b0-87a6-c23c1e18e36f) |
| 3.10 | Cap. 3 | Mapa das cadeias de translação de Hollerith e sua expansão global: o caso brasileiro | [`cadeia-translacao-ibm-capitulo3.mmd`](cap3/cadeia-translacao-ibm-capitulo3.mmd) | tese: `figuras/cap.3/diagrama/cadeia-translacao-ibm-capitulo3.png`<br>versão anterior no site: [`cap3-cadeia-translacao-ibm.png`](../figuras/cap3/cap3-cadeia-translacao-ibm.png) | [abrir](https://mermaid.ai/d/0c180893-5d01-4821-96e8-155a4e627aa5) |
| 4.3 | Cap. 4 | Mapa do capítulo 4: a rede que Marcelo construiu | [`mapa-capitulo4.mmd`](cap4/mapa-capitulo4.mmd) | tese: `figuras/cap.4/diagramas-mermaid/mapa-capitulo4.png` | [abrir](https://mermaid.ai/d/cde0a17c-8b5b-4e55-a287-2f2a51f8738d) |
| 4.4 | Cap. 4 | Mapa da cadeia de translação do projeto Spira: do covideiro ao objeto fracional (2020–2026) | [`cadeia-translacao-condensada-capitulo4-2026-04-15-202330.mmd`](cap4/cadeia-translacao-condensada-capitulo4-2026-04-15-202330.mmd) | [`figuras/cadeia-translacao-condensada-capitulo4-2026-04-15-202330.png`](../figuras/cadeia-translacao-condensada-capitulo4-2026-04-15-202330.png) | [abrir](https://mermaid.ai/d/f2bf88be-28fc-4669-8b14-b9ddda943184) |
| 4.5 | Cap. 4 | Mapa da linha do tempo do capítulo 4 (2020–2026) | [`mapa-linha-tempo-capitulo4.mmd`](cap4/mapa-linha-tempo-capitulo4.mmd) | tese: `figuras/cap.4/diagramas-mermaid/mapa-linha-tempo-capitulo4.png` | [abrir](https://mermaid.ai/d/49007d9e-941f-4172-889a-a3257c8a14ac) |
| 4.6 | Cap. 4 | Mapa analítico do capítulo (posicionamento analítico) | [`quadro-analitico-capitulo4-2026-04-15-202321.mmd`](cap4/quadro-analitico-capitulo4-2026-04-15-202321.mmd) | [`figuras/quadro-analitico-capitulo4-2026-04-15-202321.png`](../figuras/quadro-analitico-capitulo4-2026-04-15-202321.png) | [abrir](https://mermaid.ai/d/7aec6c39-38e8-4dce-904f-06b74374d4bf) |
| 4.7 | Cap. 4 | Mapa do argumento (procedimento analítico) | [`cap4-argumento.mmd`](cap4/cap4-argumento.mmd) | [`figuras/cap4-argumento.png`](../figuras/cap4-argumento.png) | [abrir](https://mermaid.ai/d/dbdaf709-a83d-4c21-bde0-fed7b4f04c12) |
| 4.26 | Considerações finais | Síntese das reflexões da tese | [`diagrama_sintese_tese.mmd`](cap5/diagrama_sintese_tese.mmd) | tese: `figuras/cap.4/diagramas-mermaid/diagrama_sintese_tese.png` | [abrir](https://mermaid.ai/d/47234d6a-8a7b-468f-9559-28ded7c400cf) |

As Considerações finais são um `\chapter*`, que não reinicia o contador de figuras; por isso a Figura 4.26 continua a numeração do capítulo 4.

## Relação com `figuras/mapas/` e `figuras/linha-do-tempo/`

Os `.mmd` de [`figuras/mapas/`](../figuras/mapas) e [`figuras/linha-do-tempo/`](../figuras/linha-do-tempo) são cópias anteriores. Os mapas dos capítulos 1 e 2 são idênticos aos desta pasta (só falta a quebra de linha final). Já `mapa-capitulo3.mmd`, `mapa-capitulo4.mmd` e `linha-do-tempo-capitulo3.mmd` diferem das versões que a tese usa hoje. A fonte atual é esta pasta.

## Licença

Os diagramas são de minha autoria e estão sob [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.pt-br), conforme [`LICENSE-DADOS.md`](../LICENSE-DADOS.md). Ao reutilizar, cite a autoria (Juliane Cristina Helanski Cardoso) e a fonte, conforme o [`CITATION.cff`](../CITATION.cff).
