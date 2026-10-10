# Como conectar este repo ao `julianehelanski/tecno-etnografia-centro-ia` (.tex)

Este repositório roda a análise de rede textual sobre os
capítulos da tese, que vivem no repo irmão
`julianehelanski/tecno-etnografia-centro-ia`. A cada atualização lá, este repo
regenera automaticamente PNG/GEXF/relatório.

## Passos manuais (uma vez só)

### 1. No repo `tecno-etnografia-tese-site` (este)

- Vá em **Settings → Secrets and variables → Actions** e crie:
  - `ETNOGRAFIA_PAT` *(opcional, só se o repo .tex for privado)*:
    Personal Access Token fine-grained com `Contents: read` no repo
    `julianehelanski/tecno-etnografia-centro-ia`. Como o repo é público,
    pode pular — o workflow usa `GITHUB_TOKEN` como fallback.

### 2. No repo `tecno-etnografia-centro-ia` (.tex)

- Crie o secret **Settings → Secrets and variables → Actions**:
  - `C4AI_DISPATCH_PAT`: PAT fine-grained com `Contents: read & write` no
    repo `julianehelanski/tecno-etnografia-tese-site`.
- Copie o conteúdo de `docs/dispatch-from-tex.yml.example` (deste repo)
  para `.github/workflows/notify-c4ai.yml` no repo tecno-etnografia-centro-ia
  e commite.

### 3. No `rede_textual/chapters.yml` (deste repo)

- Mude `enabled: false` para `enabled: true` em cada capítulo cujo `.tex`
  já exista no repo .tex. O nome em `source:` precisa bater com o caminho
  relativo no repo tecno-etnografia-centro-ia (ex.: `ex_cap2.tex`).
- *(Opcional)* Crie `rede_textual/interpretation_capN.md` com sua leitura
  interpretativa — o conteúdo é embutido na seção 9 do relatório.

## Fluxo automático que isso habilita

1. Você commita uma mudança em `ex_cap3.tex` no repo
   `tecno-etnografia-centro-ia`.
2. O workflow `notify-c4ai.yml` nesse repo dispara um
   `repository_dispatch` (tipo `thesis-updated`) para este repo.
3. O workflow `analyze.yml` aqui:
   - faz checkout deste repo + checkout do repo .tex em `_tex/`;
   - roda `python rede_textual/run_all.py --source-root _tex`;
   - commita os PNG/GEXF/CSV/JSON/`.md` atualizados em `main`.

## Rodar localmente

```bash
# clonar o repo .tex ao lado para que _tex/ aponte para ele
git clone https://github.com/julianehelanski/tecno-etnografia-centro-ia.git _tex
pip install -r requirements.txt

# todos os capítulos habilitados
python rede_textual/run_all.py --source-root _tex

# só alguns
python rede_textual/run_all.py --source-root _tex --only cap1,cap2

# ou um único, manualmente, sem o manifesto
python rede_textual/rede_textual_capitulo.py \
  --chapter _tex/ex_cap2.tex --slug cap2 --title "Capítulo 2"
```

Outputs: cada capítulo grava em `rede_textual/<slug>/` — `cap1`, `cap2`,
`cap3`, `cap4` ficam cada um na sua subpasta com PNG/GEXF/CSV/`.md` próprios.

## Trigger manual

Em **Actions → "Analisa capítulos da tese" → Run workflow** você pode
forçar uma rerun (e opcionalmente passar `only=cap2` para limitar).
