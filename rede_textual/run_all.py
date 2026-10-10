"""
Driver que lê rede_textual/chapters.yml e dispara a análise textual em cada
capítulo habilitado.

Uso típico:
    python rede_textual/run_all.py --source-root _tex
    python rede_textual/run_all.py --source-root /caminho/local/etnografia
    python rede_textual/run_all.py --only cap1,cap2

Cada capítulo grava seus PNG/GEXF/CSV/relatório em rede_textual/<slug>/.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rede_textual_capitulo import run as run_analysis
from narrative_trajectory import run as run_trajectory

THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parent
DEFAULT_MANIFEST = THIS_DIR / "chapters.yml"


def _load_yaml(path: Path) -> dict:
    """Minimal YAML loader for the chapters.yml schema.

    Avoids a PyYAML dependency. The expected schema is a flat list under
    `chapters:` where each item has scalar key/value pairs (string, bool).
    """
    chapters: list[dict] = []
    current: dict | None = None
    in_list = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("chapters:"):
            in_list = True
            continue
        if not in_list:
            continue
        if line.startswith("  - "):
            if current:
                chapters.append(current)
            current = {}
            rest = line[4:]
            if ":" in rest:
                k, v = rest.split(":", 1)
                current[k.strip()] = _coerce(v.strip())
        elif line.startswith("    ") and current is not None:
            if ":" in line:
                k, v = line.strip().split(":", 1)
                current[k.strip()] = _coerce(v.strip())
    if current:
        chapters.append(current)
    return {"chapters": chapters}


def _coerce(v: str):
    if v.lower() in ("true", "yes"):
        return True
    if v.lower() in ("false", "no"):
        return False
    return v.strip().strip('"').strip("'")


def _resolve_source(spec: dict, source_root: Path) -> Path | None:
    """Resolve the chapter source path inside `source_root`."""
    candidate = source_root / spec["source"]
    return candidate if candidate.exists() else None


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST,
                   help="Path to chapters.yml (default: rede_textual/chapters.yml).")
    p.add_argument("--source-root", type=Path, default=REPO_ROOT / "_tex",
                   help="Directory where the .tex sister repo is checked out "
                        "(default: ./_tex).")
    p.add_argument("--only", default=None,
                   help="Comma-separated list of slugs to restrict the run "
                        "(e.g. 'cap1,cap2'). Defaults to all enabled chapters.")
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    manifest = _load_yaml(args.manifest)
    selected = {s.strip() for s in args.only.split(",")} if args.only else None

    failures: list[str] = []
    skipped: list[str] = []
    for spec in manifest["chapters"]:
        slug = spec["slug"]
        if selected is not None and slug not in selected:
            continue
        if not spec.get("enabled", False) and selected is None:
            skipped.append(f"{slug} (disabled)")
            continue
        src = _resolve_source(spec, args.source_root)
        if src is None:
            failures.append(f"{slug}: source not found ({spec['source']})")
            continue

        out = THIS_DIR / slug
        interp = THIS_DIR / f"interpretation_{slug}.md"
        title = spec.get("title", slug)
        print(f"\n=== {slug} ({title}) ← {src}")
        run_analysis(
            src=src,
            slug=slug,
            title=title,
            out=out,
            interpretation_path=interp if interp.exists() else None,
        )
        try:
            run_trajectory(src=src, slug=slug, title=title, out=out)
        except Exception as exc:  # noqa: BLE001 — trajectory is non-fatal
            failures.append(f"{slug} (trajectory): {type(exc).__name__}: {exc}")

    if skipped:
        print("\nSkipped (disabled):", ", ".join(skipped))
    if failures:
        print("\nFailures:", *failures, sep="\n  - ")
        sys.exit(1)


if __name__ == "__main__":
    main()
