#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_site_figuras.py
====================
Copia as imagens regeneradas pela análise (rede_textual/<slug>/...) para a
pasta que o SITE exibe (figuras/<slug>/...), já com os nomes que o
index.html usa.

Princípio: só atualiza imagem cujo destino JÁ EXISTE em figuras/. Assim
refrescamos exatamente o que o site mostra hoje (atualmente só o cap1),
sem despejar arquivos não referenciados. Para passar a exibir um novo
capítulo, basta criar os arquivos em figuras/<slug>/ uma vez — depois
eles se atualizam sozinhos.

Uso:
    python rede_textual/sync_site_figuras.py [--dry-run]
"""
import sys
import shutil
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parent
FIGURAS = REPO_ROOT / "figuras"

SLUGS = ["cap1", "cap2", "cap3", "cap4"]

# mapeamento: nome gerado em rede_textual/<slug>/  ->  nome usado em figuras/<slug>/
# {slug} é substituído pelo capítulo. As legendas do site associam o "pmi"
# ao NÚCLEO da rede (focus_pmi), não à rede completa.
NAME_MAP = {
    "infranodus_{slug}_network.png":   "{slug}-infranodus-network.png",
    "infranodus_{slug}_focus.png":     "{slug}-infranodus-focus.png",
    "infranodus_{slug}_focus_pmi.png": "{slug}-infranodus-pmi.png",
    "trajectory_gantt.png":            "{slug}-trajectory-gantt.png",
    "trajectory_alluvial.png":         "{slug}-trajectory-alluvial.png",
    "trajectory_semantic.png":         "{slug}-trajectory-semantic.png",
}


def main() -> int:
    dry = "--dry-run" in sys.argv[1:]
    copied = skipped_no_dest = skipped_no_src = 0

    for slug in SLUGS:
        src_dir = THIS_DIR / slug
        dst_dir = FIGURAS / slug
        for src_tmpl, dst_tmpl in NAME_MAP.items():
            src = src_dir / src_tmpl.format(slug=slug)
            dst = dst_dir / dst_tmpl.format(slug=slug)
            if not dst.exists():
                skipped_no_dest += 1
                continue  # site não exibe esta imagem; não criar do nada
            if not src.exists():
                skipped_no_src += 1
                print(f"AVISO: gerado ausente, mantendo o atual: {src}")
                continue
            print(f"{'(dry) ' if dry else ''}atualiza {dst}  <-  {src}")
            if not dry:
                shutil.copyfile(src, dst)
            copied += 1

    print(f"\n{copied} imagem(ns) {'seriam ' if dry else ''}atualizada(s); "
          f"{skipped_no_dest} fora do site (puladas), "
          f"{skipped_no_src} sem arquivo gerado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
