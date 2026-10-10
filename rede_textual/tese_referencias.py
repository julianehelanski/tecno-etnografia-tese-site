#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tese_referencias.py
===================
Compila a bibliografia EFETIVAMENTE CITADA na tese e a reinjeta no HTML
(<script id="refsdata">), para a seção "Referências" ao final da aba
"A tese". Companheiro do `tese_documento.py` (que gera o `docdata`).

O que faz:
  1. Lê o `tese.tex` de `--source-root` e descobre quais arquivos são de
     fato `\\input`/`\\include` (os comentados com % ficam de fora — como
     os apêndices `ex_ape*`, que não entram na compilação do PDF).
  2. Varre esses arquivos coletando as chaves dos comandos `\\textcite` e
     `\\parencite` (inclui variantes com `*`, colchetes opcionais e várias
     chaves separadas por vírgula). Não há `\\nocite` na tese.
  3. Cruza as chaves com o `tese.bib` e formata cada entrada no estilo
     `authoryear`/ABNT usado na compilação do PDF (autor invertido, ano
     entre parênteses, título em itálico, "Trad. por", nota de original,
     local: editora; DOI e URLs quando presentes). Ordena por nty.
  4. Exporta JSON e, com `--inject`, reinjeta o `<script id="refsdata">`.

Uso:
    python3 rede_textual/tese_referencias.py --source-root /tmp/tese --inject index.html

Obs.: aproximação fiel do estilo authoryear feita a partir dos campos do
`.bib` (não há toolchain LaTeX/biber aqui). Pode haver pequenas diferenças
de pontuação/ordem de campos em relação ao que o biber geraria.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# comandos de citação usados na tese
CITE_RE = re.compile(
    r'\\(?:paren|text)cite[a-zA-Z]*\*?(?:\s*\[[^\]]*\])*\s*\{([^}]*)\}'
)

# ---------------------------------------------------------------- fontes .tex

def included_tex_files(tex_root: Path) -> list[Path]:
    """Arquivos .tex de fato \\input/\\include no tese.tex (ignora comentados)."""
    master = tex_root / "tese.tex"
    files: list[Path] = []
    if not master.exists():
        print(f"[ref] ERRO: {master} não encontrado.")
        return files
    for line in master.read_text(encoding="utf-8").splitlines():
        code = line.split("%", 1)[0]  # descarta comentário
        for m in re.finditer(r'\\(?:input|include)\{([^}]+)\}', code):
            name = m.group(1)
            p = tex_root / (name if name.endswith(".tex") else name + ".tex")
            if p.exists():
                files.append(p)
    return files


def collect_cited_keys(files: list[Path]) -> set[str]:
    keys: set[str] = set()
    for p in files:
        txt = p.read_text(encoding="utf-8")
        txt = "\n".join(l.split("%", 1)[0] for l in txt.splitlines())  # sem comentários
        for grp in CITE_RE.findall(txt):
            for k in grp.split(","):
                k = k.strip()
                if k:
                    keys.add(k)
    return keys

# ---------------------------------------------------------------- parser .bib

def parse_bib(bib_path: Path) -> dict[str, tuple[str, dict]]:
    raw = bib_path.read_text(encoding="utf-8")
    out: dict[str, tuple[str, dict]] = {}
    for m in re.finditer(r'@(\w+)\s*\{', raw):
        typ = m.group(1).lower()
        start = m.end()
        depth, j = 1, start
        while j < len(raw) and depth > 0:
            if raw[j] == '{':
                depth += 1
            elif raw[j] == '}':
                depth -= 1
            j += 1
        body = raw[start:j - 1]
        key = body.split(",", 1)[0].strip()
        out[key] = (typ, _fields(body))
    return out


def _fields(body: str) -> dict:
    b = body.split(",", 1)[1] if "," in body else ""
    fs: dict = {}
    for fm in re.finditer(r'(\w+)\s*=\s*', b):
        name = fm.group(1).lower()
        p = fm.end()
        if p >= len(b):
            continue
        if b[p] == '{':
            depth, q = 1, p + 1
            while q < len(b) and depth > 0:
                if b[q] == '{':
                    depth += 1
                elif b[q] == '}':
                    depth -= 1
                q += 1
            val = b[p + 1:q - 1]
        elif b[p] == '"':
            q = b.index('"', p + 1)
            val = b[p + 1:q]
        else:
            q = p
            while q < len(b) and b[q] not in ',\n':
                q += 1
            val = b[p:q].strip()
        fs[name] = val
    return fs

# ---------------------------------------------------- LaTeX -> unicode/HTML

_ACC = {
    "'": {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú', 'c': 'ć', 'n': 'ń',
          'y': 'ý', 's': 'ś', 'z': 'ź', 'A': 'Á', 'E': 'É', 'I': 'Í', 'O': 'Ó', 'U': 'Ú'},
    "`": {'a': 'à', 'e': 'è', 'i': 'ì', 'o': 'ò', 'u': 'ù', 'A': 'À', 'E': 'È', 'O': 'Ò'},
    "^": {'a': 'â', 'e': 'ê', 'i': 'î', 'o': 'ô', 'u': 'û', 'A': 'Â', 'E': 'Ê', 'O': 'Ô'},
    "~": {'a': 'ã', 'o': 'õ', 'n': 'ñ', 'A': 'Ã', 'O': 'Õ', 'N': 'Ñ'},
    '"': {'a': 'ä', 'e': 'ë', 'i': 'ï', 'o': 'ö', 'u': 'ü', 'A': 'Ä', 'O': 'Ö', 'U': 'Ü'},
}


def latex_to_text(s: str, italic: bool = True) -> str:
    if not s:
        return ''
    s = re.sub(r'\s+', ' ', s.replace('\n', ' ').replace('\r', ' ')).strip()
    if italic:
        s = re.sub(r'\\(?:emph|textit|textsl)\s*\{([^{}]*)\}', r'<em>\1</em>', s)
    else:
        s = re.sub(r'\\(?:emph|textit|textsl)\s*\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\(?:textbf|textsc|textrm|texttt|mkbibquote)\s*\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\url\s*\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\c\s*\{?\s*c\s*\}?', 'ç', s)
    s = re.sub(r'\\c\s*\{?\s*C\s*\}?', 'Ç', s)

    def _accrepl(m):
        return _ACC.get(m.group(1), {}).get(m.group(2), m.group(2))
    s = re.sub(r"\\(['`^~\"])\{([A-Za-z])\}", _accrepl, s)   # forma \'{e}
    s = re.sub(r"\\(['`^~\"])\s*([A-Za-z])", _accrepl, s)    # forma \'e
    s = (s.replace('\\&', '&').replace('\\#', '#').replace('\\_', '_')
          .replace('\\%', '%').replace('\\$', '$'))
    s = s.replace('---', '—').replace('--', '–')
    s = s.replace('``', '“').replace("''", '”').replace('~', ' ').replace('\\ ', ' ')
    s = re.sub(r'\\[,;:!]', ' ', s)     # espaçamentos finos
    s = re.sub(r'\\[a-zA-Z]+', '', s)   # comandos remanescentes
    s = s.replace('{', '').replace('}', '')
    s = re.sub(r'\s+', ' ', s).strip().replace(' ,', ',').replace(' .', '.')
    return s

# ---------------------------------------------------------------- nomes

def _split_names(field: str) -> list[str]:
    return [n.strip() for n in re.split(r'\s+and\s+', field) if n.strip()]


def _name_inverted(n: str) -> str:   # "Sobrenome, Nome"
    n = n.strip()
    if n.startswith('{') and n.endswith('}'):
        return latex_to_text(n[1:-1], italic=False)
    if ',' in n:
        fam, giv = n.split(',', 1)
        return latex_to_text(fam.strip() + ', ' + giv.strip(), italic=False)
    parts = n.split()
    if len(parts) == 1:
        return latex_to_text(n, italic=False)
    return latex_to_text(parts[-1] + ', ' + ' '.join(parts[:-1]), italic=False)


def _name_natural(n: str) -> str:    # "Nome Sobrenome"
    n = n.strip()
    if n.startswith('{') and n.endswith('}'):
        return latex_to_text(n[1:-1], italic=False)
    if ',' in n:
        fam, giv = n.split(',', 1)
        return latex_to_text(giv.strip() + ' ' + fam.strip(), italic=False)
    return latex_to_text(n, italic=False)


def _join_names(names: list[str], inverted: bool = True) -> str:
    fmt = [(_name_inverted(n) if inverted else _name_natural(n)) for n in names]
    if len(fmt) == 1:
        return fmt[0]
    return ', '.join(fmt[:-1]) + ' e ' + fmt[-1]

# ---------------------------------------------------------------- datas/campos

_MES = {'1': 'jan.', '2': 'fev.', '3': 'mar.', '4': 'abr.', '5': 'mai.', '6': 'jun.',
        '7': 'jul.', '8': 'ago.', '9': 'set.', '10': 'out.', '11': 'nov.', '12': 'dez.',
        '01': 'jan.', '02': 'fev.', '03': 'mar.', '04': 'abr.', '05': 'mai.',
        '06': 'jun.', '07': 'jul.', '08': 'ago.', '09': 'set.'}


def _fmt_urldate(d: str) -> str:
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', d or '')
    if m:
        y, mo, da = m.groups()
        return f'{int(da)} {_MES.get(mo, mo)} {y}'
    return latex_to_text(d, italic=False)


def _pages(p: str) -> str:
    return latex_to_text(p, italic=False).replace('--', '–')


def _url_html(u: str) -> str:
    u = u.strip()
    return f'<a href="{u}" target="_blank" rel="noopener">{u}</a>'


def _year(f: dict) -> str:
    y = f.get('year') or ''
    if not y and f.get('date'):
        m = re.match(r'(\d{4})', f['date'])
        y = m.group(1) if m else f['date']
    return latex_to_text(y, italic=False)


def _T(f: dict, k: str, italic: bool = False) -> str:
    return latex_to_text(f.get(k, ''), italic=italic) if f.get(k) else ''


def _title_full(f: dict) -> str:
    t = latex_to_text(f.get('title', ''), italic=False)
    if f.get('subtitle'):
        t += ': ' + latex_to_text(f['subtitle'], italic=False)
    return t


def _main_names(f: dict) -> tuple[str, bool]:
    if f.get('author'):
        return _join_names(_split_names(f['author']), inverted=True), False
    if f.get('editor'):
        return _join_names(_split_names(f['editor']), inverted=True), True
    return '', False

# ---------------------------------------------------------------- formatação

def format_entry(typ: str, f: dict) -> str:
    names, is_ed = _main_names(f)
    yr = _year(f)
    head = names + (' (org.)' if (is_ed and names) else '')
    head = f'{head} ({yr})' if yr else head

    ttl = _title_full(f)

    def addr_pub() -> str:
        loc = _T(f, 'address') or _T(f, 'location')
        pub = _T(f, 'publisher')
        return f'{loc}: {pub}' if (loc and pub) else (pub or loc)

    if typ == 'book':
        s = f'<em>{ttl}</em>'
        if f.get('translator'):
            s += '. Trad. por ' + _join_names(_split_names(f['translator']), inverted=False)
        if f.get('edition'):
            ed = _T(f, 'edition')
            s += '. ' + (ed + '. ed.' if ed.isdigit() else ed)
        if f.get('note'):
            s += '. ' + latex_to_text(f['note'], italic=True)
        ap = addr_pub()
        if ap:
            s += '. ' + ap
    elif typ in ('collection', 'edited'):
        s = f'<em>{ttl}</em>'
        ap = addr_pub()
        if ap:
            s += '. ' + ap
        if f.get('note'):
            s += '. ' + latex_to_text(f['note'], italic=True)
    elif typ == 'incollection':
        s = ttl + '. In: '
        if f.get('editor'):
            s += _join_names(_split_names(f['editor']), inverted=False) + ' (org.), '
        s += f'<em>{latex_to_text(f.get("booktitle", ""), italic=False)}</em>'
        ap = addr_pub()
        if ap:
            s += '. ' + ap
        if f.get('pages'):
            s += ', pp. ' + _pages(f['pages'])
    elif typ == 'inproceedings':
        s = ttl + f'. In: <em>{latex_to_text(f.get("booktitle", ""), italic=False)}</em>'
        ap = addr_pub()
        if ap:
            s += '. ' + ap
        if f.get('pages'):
            s += ', pp. ' + _pages(f['pages'])
        if f.get('doi'):
            s += '. DOI: ' + _T(f, 'doi')
    elif typ == 'article':
        s = ttl
        jt = _T(f, 'journal') or _T(f, 'journaltitle')
        if jt:
            s += f'. <em>{jt}</em>'
        vn = []
        if f.get('volume'):
            vn.append('vol. ' + _T(f, 'volume'))
        if f.get('number'):
            vn.append('n. ' + _T(f, 'number'))
        if vn:
            s += ', ' + ', '.join(vn)
        if f.get('pages'):
            s += ', pp. ' + _pages(f['pages'])
        if f.get('doi'):
            s += '. DOI: ' + _T(f, 'doi')
    elif typ == 'phdthesis':
        s = f'<em>{ttl}</em>. Tese (Doutorado)'
        if f.get('school'):
            s += ' — ' + _T(f, 'school')
        if f.get('address'):
            s += ', ' + _T(f, 'address')
    elif typ in ('report', 'techreport'):
        s = f'<em>{ttl}</em>'
        if f.get('type'):
            s += '. ' + _T(f, 'type')
        if f.get('institution'):
            s += '. ' + _T(f, 'institution')
        if f.get('address'):
            s += ', ' + _T(f, 'address')
        if f.get('note'):
            s += '. ' + latex_to_text(f['note'], italic=True)
        if f.get('url'):
            s += '. Disponível em: ' + _url_html(f['url'])
            if f.get('urldate'):
                s += f'. Acesso em: {_fmt_urldate(f["urldate"])}'
    elif typ in ('online', 'misc', 'booklet'):
        s = f'<em>{ttl}</em>'
        extras = []
        if f.get('howpublished'):
            extras.append(_T(f, 'howpublished'))
        if f.get('series'):
            se = _T(f, 'series')
            if f.get('number'):
                se += ', n. ' + _T(f, 'number')
            extras.append(se)
        if f.get('organization') and typ == 'online':
            extras.append(_T(f, 'organization'))
        if f.get('institution'):
            ins = _T(f, 'institution')
            if f.get('address'):
                ins += ', ' + _T(f, 'address')
            extras.append(ins)
        elif f.get('address') and typ == 'booklet':
            extras.append(_T(f, 'address'))
        for e in extras:
            s += '. ' + e
        if f.get('note'):
            s += '. ' + latex_to_text(f['note'], italic=True)
        if f.get('url'):
            s += '. Disponível em: ' + _url_html(f['url'])
            if f.get('urldate'):
                s += f'. Acesso em: {_fmt_urldate(f["urldate"])}'
    else:
        s = f'<em>{ttl}</em>'
        ap = addr_pub()
        if ap:
            s += '. ' + ap

    out = (head + '. ' + s).strip() if head else s.strip()
    if not out.endswith('.'):
        out += '.'
    # colapsa ponto duplo nas junções (ex.: "2. ed." + ". ") sem tocar em reticências
    out = re.sub(r'\.\.(?=\s|<|$)', '.', out)
    return out


def _strip_acc(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn').lower()


def _sortkey(f: dict) -> tuple:
    names, _ = _main_names(f)
    fam = _strip_acc(names.split(',')[0]) if names else _strip_acc(_title_full(f))
    return (fam, _strip_acc(_title_full(f)), _year(f))

# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", type=Path, default=Path("/tmp/tese"),
                    help="Raiz do repositório da tese (contém tese.tex e tese.bib).")
    ap.add_argument("--out", type=Path, default=THIS_DIR / "tese_referencias.json")
    ap.add_argument("--inject", type=Path, default=None)
    args = ap.parse_args()

    bib_path = args.source_root / "tese.bib"
    if not bib_path.exists():
        print(f"[ref] ERRO: {bib_path} não encontrado.")
        return 1

    files = included_tex_files(args.source_root)
    if not files:
        print("[ref] ERRO: nenhum arquivo .tex incluído encontrado.")
        return 1
    cited = collect_cited_keys(files)
    bib = parse_bib(bib_path)

    missing = sorted(k for k in cited if k not in bib)
    if missing:
        print(f"[ref] aviso: {len(missing)} chave(s) citada(s) sem entrada no .bib: "
              + ", ".join(missing[:20]) + (" …" if len(missing) > 20 else ""))

    # ordem determinística: chaves ordenadas por bibkey e depois ordenação
    # estável por nty (nome, título, ano) — empates preservam a ordem por chave.
    used = [(k, *bib[k]) for k in sorted(cited) if k in bib]  # (key, typ, fields)
    used.sort(key=lambda x: _sortkey(x[2]))
    refs = [format_entry(typ, f) for _k, typ, f in used]

    data_str = json.dumps(refs, ensure_ascii=False, separators=(",", ":"))
    args.out.write_text(data_str, encoding="utf-8")
    print(f"[ref] JSON: {args.out} ({args.out.stat().st_size/1024:.0f} KB) | "
          f"{len(refs)} referências citadas (de {len(bib)} entradas no .bib) · "
          f"{len(files)} arquivos .tex varridos")

    if args.inject is not None:
        assert "</script" not in data_str.lower()
        html = args.inject.read_text(encoding="utf-8")
        pat = re.compile(r'(<script type="application/json" id="refsdata">).*?(</script>)',
                         re.DOTALL)
        new, n = pat.subn(lambda m: m.group(1) + data_str + m.group(2), html, count=1)
        if n != 1:
            print(f"[ref] ERRO: <script id=refsdata> não encontrado em {args.inject}")
            return 1
        args.inject.write_text(new, encoding="utf-8")
        print(f"[ref] reinjetado em {args.inject}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
