#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_tese_figuras.py
====================
Sincroniza figuras de CONTEÚDO da tese para o site, conforme o mapa
``rede_textual/figuras_tese_map.tsv``.

Cada linha do mapa liga um destino no site a uma origem na tese (um glob,
para tolerar nomes com timestamp que mudam a cada re-exportação). Para cada
entrada, usa-se a origem MAIS RECENTE que casa com o glob.

Duas preocupações tratadas aqui:

1. **Peso da página.** Os originais da tese costumam ser grandes (vários MB).
   Ao copiar, a imagem é *otimizada para web*: redimensionada para no máximo
   ``--max-side`` px no maior lado e recomprimida. (PDF é copiado como está;
   se Pillow não estiver instalado, faz cópia crua.)

2. **Sem churn.** Um arquivo de estado (``figuras_tese_sync_state.json``)
   guarda o hash do CONTEÚDO de origem já sincronizado. A figura do site só é
   reescrita quando a origem na tese realmente muda — então rodar de novo sem
   mudanças na tese não reescreve nada.

Diferente de ``sync_site_figuras.py`` (figuras de análise geradas aqui), este
trata as figuras autorais da tese (diagramas, imagens, gráficos) exibidas no
site.

Uso:
    python3 scripts/sync_tese_figuras.py --source-root _tex
    python3 scripts/sync_tese_figuras.py --source-root /caminho/da/tese --dry-run
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import io
import json
import os
import shutil
from pathlib import Path

try:
    from PIL import Image
    _HAVE_PIL = True
except Exception:  # pragma: no cover
    _HAVE_PIL = False

THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parent
DEFAULT_MANIFEST = REPO_ROOT / "rede_textual" / "figuras_tese_map.tsv"
STATE_FILE = REPO_ROOT / "rede_textual" / "figuras_tese_sync_state.json"
RASTER = (".png", ".jpg", ".jpeg", ".gif", ".webp")


def _sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _newest(paths: list[str]) -> str | None:
    paths = [p for p in paths if os.path.isfile(p)]
    return max(paths, key=os.path.getmtime) if paths else None


def _web_bytes(src: str, dest_ext: str, max_side: int) -> bytes:
    """Versão otimizada para web da imagem de origem (ou bytes crus se não der)."""
    if not _HAVE_PIL or dest_ext.lower() not in RASTER:
        with open(src, "rb") as f:
            return f.read()
    try:
        img = Image.open(src)
        img.load()
        w, h = img.size
        if max(w, h) > max_side:
            scale = max_side / max(w, h)
            img = img.resize((max(1, round(w * scale)), max(1, round(h * scale))),
                             Image.LANCZOS)
        buf = io.BytesIO()
        ext = dest_ext.lower()
        if ext in (".jpg", ".jpeg"):
            img.convert("RGB").save(buf, "JPEG", quality=85, optimize=True,
                                    progressive=True)
        elif ext == ".png":
            img.save(buf, "PNG", optimize=True)
        elif ext == ".webp":
            img.save(buf, "WEBP", quality=88, method=6)
        else:  # gif e outros: salva no formato original
            img.save(buf, img.format or "PNG")
        out = buf.getvalue()
        with open(src, "rb") as f:
            rawb = f.read()
        # se a "otimização" ficou maior que o original (PNG já bem comprimido),
        # fica com o menor.
        return out if len(out) <= len(rawb) else rawb
    except Exception:
        with open(src, "rb") as f:
            return f.read()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source-root", type=Path, default=REPO_ROOT / "_tex")
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--max-side", type=int, default=1600,
                    help="Maior lado em px após otimização (padrão: 1600).")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.manifest.exists():
        print(f"manifesto não encontrado: {args.manifest}")
        return 2
    if not _HAVE_PIL:
        print("AVISO: Pillow não instalado — cópia crua (sem otimização web).")

    state = {}
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            state = {}

    copied = unchanged = missing = 0
    no_source: list[str] = []
    for raw in args.manifest.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "\t" not in line:
            continue
        dest_rel, src_glob = (x.strip() for x in line.split("\t", 1))
        src = _newest(glob.glob(str(args.source_root / src_glob)))
        if src is None:
            missing += 1
            no_source.append(src_glob)
            continue
        src_sha = _sha(src)
        dest = REPO_ROOT / dest_rel
        if state.get(dest_rel) == src_sha and dest.exists():
            unchanged += 1
            continue
        print(f"{'(dry) ' if args.dry_run else ''}atualiza {dest_rel}  <-  "
              f"{os.path.relpath(src, args.source_root)}")
        if not args.dry_run:
            data = _web_bytes(src, os.path.splitext(dest_rel)[1], args.max_side)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            state[dest_rel] = src_sha
        copied += 1

    if not args.dry_run:
        STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False,
                                         sort_keys=True), encoding="utf-8")
    print(f"\n{copied} figura(s) {'seriam ' if args.dry_run else ''}atualizada(s); "
          f"{unchanged} já em dia; {missing} sem origem na tese.")
    if no_source:
        print("  sem origem (glob não casou — figura ainda não está na tese?):")
        for g in no_source:
            print("   -", g)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
