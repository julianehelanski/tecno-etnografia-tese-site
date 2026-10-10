# Sincronização automática das figuras da tese → site

Quando você adiciona ou atualiza uma figura no repositório da tese
(`tecno-etnografia-centro-ia`), o site ressincroniza a imagem correspondente
automaticamente. Fluxo:

1. **Gatilho** — o workflow `notify-c4ai.yml` na tese avisa o site a cada push
   que toque `figuras/**` ou `ex_cap*.tex` (veja `docs/dispatch-from-tex.yml.example`).
2. **Sync** — o site roda `scripts/sync_tese_figuras.py`, que lê o mapa
   `rede_textual/figuras_tese_map.tsv` e, para cada destino, pega a versão **mais
   recente** da origem na tese, **otimiza para web** (máx. 1600 px no maior
   lado + recompressão) e grava no site.
3. **Sem churn** — `rede_textual/figuras_tese_sync_state.json` guarda o hash da
   origem já sincronizada; uma figura só é reescrita quando a origem **muda de
   fato** na tese.
4. **Cache-busting** — `scripts/cache_busting_figuras.py` atualiza o `?v=` para
   o navegador baixar a nova versão.
5. O GitHub Pages republica.

## O mapa (`rede_textual/figuras_tese_map.tsv`)

Cada linha liga `destino-no-site` ⟶ `origem-na-tese` (um *glob*; `*` cobre os
timestamps de data que mudam a cada re-exportação). **56 figuras mapeadas e
confirmadas**:

- **24** por hash de conteúdo (bytes idênticos entre site e tese);
- **32** por *hash perceptual* de imagem (mesma figura, mesmo redimensionada/
  recomprimida) — conferidas uma a uma.

> O estado inicial foi registrado sem reescrever nada (as figuras do site já
> correspondem às da tese). A primeira atualização real de cada figura na tese
> dispara a cópia otimizada.

## Como adicionar uma figura nova

1. Coloque/atualize o arquivo na tese (em `figuras/...`).
2. Adicione uma linha no mapa: `caminho/no/site.png` ⟨TAB⟩ `figuras/.../arquivo*.png`.
3. Referencie a figura no `index.html` — seja como `<img src="figuras/no/site.png">`,
   seja como entrada no array `ANALISES` da **galeria de análises** (objetos
   `{g, s, c}`: grupo, caminho e legenda).
4. Pronto — a partir daí ela se atualiza sozinha.

> O `cache_busting_figuras.py` versiona qualquer caminho `figuras/...` entre
> aspas (atributo `src=`/`href=` **ou** string em JS, como no array `ANALISES`),
> então o `?v=` vale também para as imagens da galeria.

## Figuras exibidas no site SEM origem na tese (não sincronizam)

Estas são referenciadas no site mas **não existem como arquivo no repositório
da tese** (são diagramas exportados à parte, ou ainda não versionados). Não há
de onde sincronizar. Se quiser que entrem no fluxo, comite o arquivo
correspondente na tese e adicione a linha no mapa.

- `figuras/cap2/cap2-urdidura.png`
- `figuras/cap3/cap3-arranjo-publico-privado.png`
- `figuras/cap3/cap3-cadeia-translacao-ibm.png`
- `figuras/cap3/cap3-dobra-etnografica.png`
- `figuras/cap3/cap3-hollerith-rede-sociotecnica.png`
- `figuras/cap3/cap3-panorama-c4ai.png`
- `figuras/cap3/cap3-quadro-analitico.png`
- `figuras/cap3/cap3-roadmap-ciclo.png`
- `figuras/cap3/cap3-seguindo-atores.png`
- `figuras/cronologia-spira-2026-03-11-130835.png`
- `figuras/translacao-spira-antes-depois-2026-03-11-233343.png`

> Observação: os diagramas Mermaid do capítulo 3 estão nesta lista porque seus
> PNGs não estão no repositório da tese (o `.tex` os referencia, mas o arquivo
> não foi versionado). Assim que existirem lá, mapeamos.

## As figuras de análise (rede textual / trajetórias)

Não passam por este mapa: são **geradas** aqui pelo `rede_textual/run_all.py` e
sincronizadas por `rede_textual/sync_site_figuras.py`. Continuam atualizando como
antes, a cada mudança de capítulo.
