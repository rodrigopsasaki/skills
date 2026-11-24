#!/usr/bin/env python3
"""Render a markdown report to a self-contained HTML document and print it to PDF.

Usage: python3 render_pdf.py REPORT.md -o OUT.pdf [--title "Text"] [--lang pt-BR]

Standard library only. PDF engines are detected at run time: a Chromium-family
browser, then WeasyPrint, then wkhtmltopdf. With none available the HTML is
written next to the requested output and the exit status is 3.
"""
from __future__ import annotations

import argparse
import datetime
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

EXIT_NO_ENGINE = 3
ENGINE_TIMEOUT_SECONDS = 90

CSS = """
@page { size: A4; margin: 24mm 22mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  margin: 0;
  color: #2d2f33;
  background: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Helvetica, Arial,
    "Noto Sans", "Liberation Sans", "DejaVu Sans",
    "Hiragino Sans", "Hiragino Kaku Gothic ProN", "PingFang SC", "Yu Gothic", "Microsoft YaHei",
    "Malgun Gothic", "Noto Sans CJK JP", "Noto Sans CJK SC", "Noto Sans CJK KR",
    "Geeza Pro", "Noto Sans Arabic", "Noto Naskh Arabic", "Arial Hebrew", "Noto Sans Hebrew",
    "Kohinoor Devanagari", "Devanagari Sangam MN", "Nirmala UI", "Noto Sans Devanagari",
    sans-serif;
  font-size: 10.5pt;
  line-height: 1.6;
  overflow-wrap: break-word;
}
header.title-block { margin: 0 0 14mm 0; padding-bottom: 5mm; border-bottom: 2px solid #1f5468; }
header.title-block h1 { margin: 0 0 2mm 0; font-size: 22pt; line-height: 1.2; color: #1f5468; }
header.title-block p { margin: 0; font-size: 9.5pt; color: #6b7076; }
h1, h2, h3, h4 {
  color: #1f5468;
  line-height: 1.3;
  page-break-after: avoid;
  break-after: avoid;
}
h1 { font-size: 18pt; margin: 9mm 0 3mm 0; }
h2 {
  font-size: 15pt;
  margin: 11mm 0 3.5mm 0;
  padding-bottom: 1.5mm;
  border-bottom: 1px solid #c9d6dc;
}
h3 { font-size: 12pt; margin: 7mm 0 2mm 0; }
h4 { font-size: 10.5pt; margin: 5mm 0 1.5mm 0; }
p { margin: 0 0 3mm 0; orphans: 3; widows: 3; }
strong { color: #1d1f22; }
a { color: #1f5468; text-decoration: underline; }
ul, ol { margin: 0 0 3.5mm 0; padding-inline-start: 6mm; }
li { margin: 0 0 1.5mm 0; page-break-inside: avoid; break-inside: avoid; }
li > ul, li > ol { margin: 1.5mm 0 0 0; }
blockquote {
  margin: 1mm 0 4mm 0;
  padding: 3mm 4.5mm 1mm 4.5mm;
  background: #f4f7f8;
  border-inline-start: 3px solid #1f5468;
  page-break-inside: avoid;
  break-inside: avoid;
}
blockquote p:last-child { margin-bottom: 3mm; }
code {
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", "Liberation Mono", monospace;
  font-size: 0.92em;
  background: #eef1f3;
  padding: 0 0.25em;
  border-radius: 2px;
}
pre {
  margin: 0 0 4mm 0;
  padding: 3mm 4mm;
  background: #eef1f3;
  border-radius: 3px;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  page-break-inside: avoid;
  break-inside: avoid;
}
pre code { background: none; padding: 0; font-size: 9.5pt; }
hr { border: 0; border-top: 1px solid #c9d6dc; margin: 7mm 0; }
table { width: 100%; border-collapse: collapse; margin: 0 0 4mm 0; font-size: 10pt; }
th, td { padding: 2mm 2.5mm; text-align: start; vertical-align: top; border-bottom: 1px solid #dde3e6; }
th { border-bottom: 2px solid #1f5468; color: #1f5468; background: #f4f7f8; }
tr { page-break-inside: avoid; break-inside: avoid; }
.slot { background: #fff1b8; padding: 0 0.2em; border-radius: 2px; }
"""

CODE_SPAN = re.compile(r"`([^`\n]+)`")
LINK = re.compile(r"\[([^\]\n]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
BARE_URL = re.compile(r"https?://[^\s<>\"]*[^\s<>\".,;:!?)\]]")
BOLD = re.compile(r"\*\*(?=\S)(.+?)(?<=\S)\*\*")
ITALIC = re.compile(r"(?<![*\w])\*(?![\s*])(.+?)(?<![\s*])\*(?![*\w])")
SLOT = re.compile(r"\[([^\[\]\n]+)\]")
SAFE_URL = re.compile(r"(?i)^(https?:|mailto:|#|/|\./|\.\./)")
PLACEHOLDER = re.compile(r"\x00(\d+)\x00")

HEADING = re.compile(r"^ {0,3}(#{1,4})\s+(.+?)(?:\s+#+)?\s*$")
RULE = re.compile(r"^ {0,3}([-*_])(?:\s*\1){2,}\s*$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
QUOTE = re.compile(r"^ {0,3}>\s?")
ITEM = re.compile(r"^(\s*)([-*+]|\d{1,9}[.)])\s+(.*)$")
TABLE_SEPARATOR = re.compile(r"^\s*\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)+\|?\s*$|^\s*\|\s*:?-+:?\s*\|\s*$")
TABLE_CELL_SPLIT = re.compile(r"(?<!\\)\|")

Item = Tuple[int, str, List[str]]


def escape(text: str) -> str:
    return html.escape(text, quote=True)


def inline(text: str) -> str:
    held: List[str] = []

    def hold(markup: str) -> str:
        held.append(markup)
        return "\x00%d\x00" % (len(held) - 1)

    def emphasis(escaped: str) -> str:
        return ITALIC.sub(r"<em>\1</em>", BOLD.sub(r"<strong>\1</strong>", escaped))

    def link(match: "re.Match[str]") -> str:
        label, url = match.group(1), match.group(2)
        body = emphasis(escape(label))
        if not SAFE_URL.match(url):
            return hold(body)
        return hold('<a href="%s">%s</a>' % (escape(url), body))

    def bare(match: "re.Match[str]") -> str:
        url = match.group(0)
        return hold('<a href="%s">%s</a>' % (escape(url), escape(url)))

    text = text.replace("\x00", "")
    text = CODE_SPAN.sub(lambda m: hold("<code>%s</code>" % escape(m.group(1))), text)
    text = LINK.sub(link, text)
    text = BARE_URL.sub(bare, text)
    text = emphasis(escape(text))
    text = SLOT.sub(r'<span class="slot">[\1]</span>', text)
    while PLACEHOLDER.search(text):
        text = PLACEHOLDER.sub(lambda m: held[int(m.group(1))], text)
    return text


def text_html(lines: Sequence[str]) -> str:
    return inline("\n".join(line.strip() for line in lines)).replace("\n", "<br>\n")


def indent_of(line: str) -> int:
    expanded = line.expandtabs(4)
    return len(expanded) - len(expanded.lstrip())


def is_table_start(lines: Sequence[str], i: int) -> bool:
    return (
        "|" in lines[i]
        and i + 1 < len(lines)
        and "|" in lines[i + 1]
        and bool(TABLE_SEPARATOR.match(lines[i + 1]))
    )


def starts_block(lines: Sequence[str], i: int) -> bool:
    line = lines[i]
    return bool(
        HEADING.match(line)
        or FENCE.match(line)
        or RULE.match(line)
        or QUOTE.match(line)
        or ITEM.match(line)
        or is_table_start(lines, i)
    )


def split_row(line: str) -> List[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|") and not stripped.endswith("\\|"):
        stripped = stripped[:-1]
    return [cell.replace("\\|", "|").strip() for cell in TABLE_CELL_SPLIT.split(stripped)]


def alignment(cell: str) -> str:
    left, right = cell.startswith(":"), cell.endswith(":")
    if left and right:
        return ' style="text-align:center"'
    if right:
        return ' style="text-align:end"'
    return ""


def table_block(lines: Sequence[str], i: int) -> Tuple[str, int]:
    header = split_row(lines[i])
    aligns = [alignment(cell) for cell in split_row(lines[i + 1])]
    aligns += [""] * (len(header) - len(aligns))
    i += 2
    rows: List[List[str]] = []
    while i < len(lines) and lines[i].strip() and "|" in lines[i]:
        cells = split_row(lines[i])
        rows.append((cells + [""] * len(header))[: len(header)])
        i += 1

    def row(cells: Sequence[str], tag: str) -> str:
        inner = "".join(
            '<%s dir="auto"%s>%s</%s>' % (tag, aligns[n], inline(cell), tag)
            for n, cell in enumerate(cells)
        )
        return "<tr>%s</tr>" % inner

    head = "<thead>%s</thead>" % row(header, "th")
    body = "<tbody>%s</tbody>" % "".join(row(cells, "td") for cells in rows)
    return "<table>%s%s</table>" % (head, body), i


def fence_block(lines: Sequence[str], i: int) -> Tuple[str, int]:
    marker = FENCE.match(lines[i]).group(1)  # type: ignore[union-attr]
    i += 1
    code: List[str] = []
    while i < len(lines) and not lines[i].strip().startswith(marker):
        code.append(lines[i])
        i += 1
    return '<pre dir="auto"><code>%s</code></pre>' % escape("\n".join(code)), i + 1


def quote_block(lines: Sequence[str], i: int) -> Tuple[str, int]:
    inner: List[str] = []
    while i < len(lines) and QUOTE.match(lines[i]):
        inner.append(QUOTE.sub("", lines[i], count=1))
        i += 1
    return '<blockquote dir="auto">%s</blockquote>' % "\n".join(blocks(inner)), i


def collect_items(lines: Sequence[str], i: int) -> Tuple[List[Item], int]:
    items: List[Item] = []
    while i < len(lines):
        line = lines[i]
        match = ITEM.match(line)
        if match and not RULE.match(line):
            items.append((indent_of(line), match.group(2), [match.group(3)]))
            i += 1
        elif not line.strip():
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            follows_list = j < len(lines) and (ITEM.match(lines[j]) or indent_of(lines[j]) >= 2)
            if not follows_list:
                break
            i = j
        elif indent_of(line) > 0 or not starts_block(lines, i):
            items[-1][2].append(line)
            i += 1
        else:
            break
    return items, i


def list_runs(items: Sequence[Item]) -> List[List[Item]]:
    runs: List[List[Item]] = []
    for item in items:
        if runs and is_ordered(runs[-1][0]) == is_ordered(item):
            runs[-1].append(item)
        else:
            runs.append([item])
    return runs


def is_ordered(item: Item) -> bool:
    return item[1][0].isdigit()


def render_list(items: Sequence[Item]) -> str:
    base = items[0][0]
    tops: List[Tuple[Item, List[Item]]] = []
    for item in items:
        if item[0] > base and tops:
            tops[-1][1].append(item)
        else:
            tops.append((item, []))
    out: List[str] = []
    for run in list_runs([top for top, _ in tops]):
        children = {id(top): kids for top, kids in tops}
        tag = "ol" if is_ordered(run[0]) else "ul"
        start = int(run[0][1][:-1]) if tag == "ol" else 1
        attr = ' start="%d"' % start if start != 1 else ""
        entries = []
        for top in run:
            kids = children[id(top)]
            sub = render_list(kids) if kids else ""
            entries.append('<li dir="auto">%s%s</li>' % (text_html(top[2]), sub))
        out.append('<%s dir="auto"%s>%s</%s>' % (tag, attr, "".join(entries), tag))
    return "".join(out)


def paragraph_block(lines: Sequence[str], i: int) -> Tuple[str, int]:
    parts = [lines[i]]
    i += 1
    while i < len(lines) and lines[i].strip() and not starts_block(lines, i):
        parts.append(lines[i])
        i += 1
    return '<p dir="auto">%s</p>' % text_html(parts), i


def blocks(lines: Sequence[str]) -> List[str]:
    out: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        heading = HEADING.match(line)
        if not line.strip():
            i += 1
        elif FENCE.match(line):
            markup, i = fence_block(lines, i)
            out.append(markup)
        elif heading:
            level = len(heading.group(1))
            out.append('<h%d dir="auto">%s</h%d>' % (level, inline(heading.group(2)), level))
            i += 1
        elif RULE.match(line):
            out.append("<hr>")
            i += 1
        elif QUOTE.match(line):
            markup, i = quote_block(lines, i)
            out.append(markup)
        elif is_table_start(lines, i):
            markup, i = table_block(lines, i)
            out.append(markup)
        elif ITEM.match(line):
            items, i = collect_items(lines, i)
            out.append(render_list(items))
        else:
            markup, i = paragraph_block(lines, i)
            out.append(markup)
    return out


def split_lines(markdown: str) -> List[str]:
    return re.split(r"\r\n|\r|\n", markdown)


def plain(text: str) -> str:
    text = LINK.sub(lambda m: m.group(1), text)
    return re.sub(r"[*`]", "", text).strip()


def take_first_heading(lines: Sequence[str]) -> Tuple[Optional[str], List[str]]:
    in_fence = False
    for n, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
        match = None if in_fence else re.match(r"^ {0,3}#\s+(.+?)(?:\s+#+)?\s*$", line)
        if match:
            return plain(match.group(1)), list(lines[:n]) + list(lines[n + 1 :])
    return None, list(lines)


def convert(markdown: str) -> str:
    return "\n".join(blocks(split_lines(markdown)))


def build_document(body: str, title: str, lang: str, today: str) -> str:
    return (
        "<!DOCTYPE html>\n"
        '<html lang="%s">\n<head>\n<meta charset="utf-8">\n'
        "<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n"
        '<header class="title-block"><h1 dir="auto">%s</h1><p>%s</p></header>\n'
        "%s\n</body>\n</html>\n"
    ) % (escape(lang), escape(title), CSS, escape(title), today, body)


def chromium_candidates() -> List[str]:
    candidates: List[str] = []
    if os.environ.get("CHROME_PATH"):
        candidates.append(os.environ["CHROME_PATH"])
    for app in ("Google Chrome", "Chromium", "Microsoft Edge", "Brave Browser"):
        candidates.append("/Applications/%s.app/Contents/MacOS/%s" % (app, app))
    for name in (
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "microsoft-edge",
        "msedge",
    ):
        found = shutil.which(name)
        if found:
            candidates.append(found)
    roots = [
        os.environ.get("PROGRAMFILES", r"C:\Program Files"),
        os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
        os.environ.get("LOCALAPPDATA", ""),
    ]
    for root in filter(None, roots):
        for relative in (
            r"Google\Chrome\Application\chrome.exe",
            r"Chromium\Application\chrome.exe",
            r"Microsoft\Edge\Application\msedge.exe",
            r"BraveSoftware\Brave-Browser\Application\brave.exe",
        ):
            candidates.append(os.path.join(root, relative))
    unique = list(dict.fromkeys(candidates))
    return [path for path in unique if os.path.isfile(path)]


def printed(out: Path) -> bool:
    return out.is_file() and out.stat().st_size > 0


def print_with_chromium(binary: str, source: Path, out: Path) -> bool:
    is_root = getattr(os, "geteuid", lambda: 1)() == 0
    for headless in ("--headless=new", "--headless"):
        profile = tempfile.mkdtemp(prefix="render-pdf-profile-")
        command = [
            binary,
            headless,
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--user-data-dir=%s" % profile,
            "--print-to-pdf=%s" % out,
        ]
        if is_root:
            command.append("--no-sandbox")
        command.append(source.as_uri())
        out.unlink(missing_ok=True)
        try:
            done = subprocess.run(command, capture_output=True, timeout=ENGINE_TIMEOUT_SECONDS)
        except (OSError, subprocess.TimeoutExpired):
            continue
        finally:
            shutil.rmtree(profile, ignore_errors=True)
        if done.returncode == 0 and printed(out):
            return True
    return False


def engine_chromium(source: Path, out: Path) -> Optional[str]:
    for binary in chromium_candidates():
        if print_with_chromium(binary, source, out):
            return "Chromium-family browser (%s)" % binary
    return None


def engine_weasyprint(source: Path, out: Path) -> Optional[str]:
    try:
        from weasyprint import HTML  # type: ignore[import-not-found]
    except (ImportError, OSError):
        return None
    HTML(filename=str(source)).write_pdf(str(out))
    return "WeasyPrint" if printed(out) else None


def engine_wkhtmltopdf(source: Path, out: Path) -> Optional[str]:
    binary = shutil.which("wkhtmltopdf")
    if not binary:
        return None
    command = [
        binary,
        "--quiet",
        "--enable-local-file-access",
        "--page-size",
        "A4",
        "--margin-top",
        "22mm",
        "--margin-bottom",
        "22mm",
        "--margin-left",
        "20mm",
        "--margin-right",
        "20mm",
        str(source),
        str(out),
    ]
    try:
        done = subprocess.run(command, capture_output=True, timeout=ENGINE_TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return "wkhtmltopdf" if done.returncode == 0 and printed(out) else None


Engine = Callable[[Path, Path], Optional[str]]
ENGINES: Tuple[Engine, ...] = (engine_chromium, engine_weasyprint, engine_wkhtmltopdf)


def print_pdf(document: str, out: Path, engines: Sequence[Engine]) -> Optional[str]:
    workdir = tempfile.mkdtemp(prefix="render-pdf-")
    try:
        source = Path(workdir) / "report.html"
        source.write_text(document, encoding="utf-8")
        for engine in engines:
            label = engine(source, out)
            if label:
                return label
        return None
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def parse_args(argv: Optional[Sequence[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a markdown report to PDF.")
    parser.add_argument("report", type=Path, help="markdown file")
    parser.add_argument("-o", "--output", type=Path, required=True, help="PDF file to write")
    parser.add_argument("--title", help="document title (default: first # heading, else file name)")
    parser.add_argument("--lang", default="en", help="language tag for the document (default: en)")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None, engines: Sequence[Engine] = ENGINES) -> int:
    args = parse_args(argv)
    lines = split_lines(args.report.read_text(encoding="utf-8"))
    heading, remaining = take_first_heading(lines)
    if args.title:
        title, lines = args.title, lines
    else:
        title, lines = (heading, remaining) if heading else (args.report.stem, lines)
    document = build_document(
        "\n".join(blocks(lines)), title, args.lang, datetime.date.today().isoformat()
    )
    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    label = print_pdf(document, out, engines)
    if label:
        print(out)
        print("Rendered with %s." % label, file=sys.stderr)
        return 0

    fallback = out.with_suffix(".html")
    fallback.write_text(document, encoding="utf-8")
    print(
        "No PDF engine was found, so the report was saved as %s, which prints to PDF "
        "from any browser." % fallback
    )
    return EXIT_NO_ENGINE


if __name__ == "__main__":
    sys.exit(main())
