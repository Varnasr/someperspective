#!/usr/bin/env python3
"""
PAPER BUILD — paper/paper.md  ->  downloads/paper.html  ->  downloads/paper.pdf

The Markdown file is the source of record; the HTML and PDF are generated and
committed, in keeping with the rest of this repository (see tools/build_site.py).

Markdown rendering is done here rather than with a library because no Markdown
package is available in this toolchain and the paper uses a deliberately small
subset: headings, paragraphs, tables, lists, fenced code, bold/italic, links, and
display maths. Supporting a small grammar exactly is more predictable than
depending on a general renderer for a document whose formatting we control.

Maths is left as literal TeX inside styled blocks rather than rendered. The paper
contains four display formulas and MathJax would mean an external script on a
page with a strict CSP; the formulas are readable as written, and Appendix A
restates them.

PDF generation uses the headless Chromium already present for testing. If it is
unavailable the HTML is still written and the script reports the PDF as skipped,
so a machine without Chromium can still build the site.

Run: python3 tools/build_paper.py            (--check to verify freshness)
"""
import html as ihtml
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "paper", "paper.md")
OUT_HTML = os.path.join(ROOT, "downloads", "paper.html")
OUT_PDF = os.path.join(ROOT, "downloads", "paper.pdf")
CHECK = "--check" in sys.argv


# ---------------------------------------------------------------- front matter
def split_front_matter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.index("\n---", 3)
    meta = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, text[end + 4:]


# ---------------------------------------------------------------- inline spans
def inline(s):
    s = ihtml.escape(s)
    # display maths is handled by the block pass; protect inline code first
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    s = re.sub(r"`([^`]+)`", stash, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\$([^$]+)\$", r'<span class="m">\1</span>', s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)
    return s


def slugify(s):
    slug = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    # Section headings start with a number ("6.9 The cross-era scorecard"), which would
    # produce an id like "6-9-…". That is legal HTML and the browser will still jump to
    # it, but "#6-9-…" is not a valid CSS selector, so querySelector and any JS or CSS
    # that targets it will throw. Prefix to keep ids selector-safe.
    return "s-" + slug if slug[:1].isdigit() else slug


# ---------------------------------------------------------------- block parser
def render(md):
    out, toc = [], []
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        # fenced code
        if line.startswith("```"):
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j])
                j += 1
            out.append("<pre><code>" + ihtml.escape("\n".join(buf)) + "</code></pre>")
            i = j + 1
            continue

        # display maths ($$ ... $$), possibly spanning lines
        if line.strip().startswith("$$"):
            body = line.strip()[2:]
            if body.endswith("$$"):
                body = body[:-2]
            else:
                j = i + 1
                while j < len(lines) and "$$" not in lines[j]:
                    body += "\n" + lines[j]
                    j += 1
                if j < len(lines):
                    body += "\n" + lines[j].replace("$$", "")
                i = j
            out.append('<div class="math">' + ihtml.escape(body.strip()) + "</div>")
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r"-{3,}", line.strip()):
            out.append("<hr>")
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            md_lvl, txt = len(m.group(1)), m.group(2).strip()
            sid = slugify(txt)
            # Demote by one: the page's <h1> is the paper title, so a top-level
            # Markdown section becomes <h2>. Otherwise every section is an <h1>,
            # which is wrong for both document outline and assistive technology.
            tag_lvl = min(md_lvl + 1, 6)
            out.append(f'<h{tag_lvl} id="{sid}">{inline(txt)}</h{tag_lvl}>')
            if md_lvl <= 2:
                toc.append((md_lvl, txt, sid))
            i += 1
            continue

        # tables
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[-: |]+\|\s*$", lines[i + 1]):
            head = [c.strip() for c in line.strip().strip("|").split("|")]
            j = i + 2
            rows = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            th = "".join(f"<th>{inline(c)}</th>" for c in head)
            tb = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows)
            out.append(f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
            i = j
            continue

        # lists (ordered and unordered)
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if m:
            ordered = bool(re.match(r"\d+\.", m.group(2)))
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines):
                mm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                if not mm:
                    break
                items.append(mm.group(3))
                i += 1
                # continuation lines
                while i < len(lines) and lines[i].strip() and not re.match(r"^(\s*)([-*]|\d+\.)\s+", lines[i]) \
                        and not lines[i].startswith("#") and not lines[i].strip().startswith("|"):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue

        # blank
        if not line.strip():
            i += 1
            continue

        # paragraph
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|\||```|\$\$|\s*[-*]\s|\s*\d+\.\s|-{3,}$)", lines[i]):
            buf.append(lines[i])
            i += 1
        out.append("<p>" + inline(" ".join(buf)) + "</p>")

    return "\n".join(out), toc


CSS = """
:root{--paper:#fff;--ink:#1b1b22;--ink-soft:#34343f;--muted:#6b6b78;--line:rgba(27,27,34,.12);
--accent:#b4530e;--accent-2:#0e7490;--surface-2:#faf7f1}
@media (prefers-color-scheme:dark){:root{--paper:#0b0c11;--ink:#edeff5;--ink-soft:#d3d7e0;
--muted:#99a0b1;--line:rgba(255,255,255,.12);--accent:#fb923c;--accent-2:#22d3ee;--surface-2:#161922}}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Source Serif 4',Georgia,serif;background:var(--paper);color:var(--ink);
line-height:1.62;font-size:17px;padding:2.5rem 1.25rem 5rem}
.wrap{max-width:46rem;margin:0 auto}
.hdr{border-bottom:3px solid var(--accent);padding-bottom:1.4rem;margin-bottom:2rem}
.kicker{font-family:Inter,system-ui,sans-serif;font-size:.7rem;font-weight:800;letter-spacing:.1em;
text-transform:uppercase;color:var(--accent)}
h1{font-family:Inter,system-ui,sans-serif;font-size:2rem;line-height:1.18;margin:.5rem 0 .7rem;font-weight:800}
.byline{font-family:Inter,system-ui,sans-serif;color:var(--ink-soft);font-size:.95rem}
.sub{font-family:Inter,system-ui,sans-serif;color:var(--muted);font-size:.8rem;margin-top:.5rem}
h2{font-family:Inter,system-ui,sans-serif;font-size:1.45rem;font-weight:800;margin:2.6rem 0 .8rem;
padding-top:.6rem;border-top:1px solid var(--line)}
h3{font-family:Inter,system-ui,sans-serif;font-size:1.12rem;font-weight:700;margin:1.9rem 0 .5rem}
h4{font-family:Inter,system-ui,sans-serif;font-size:1rem;font-weight:700;margin:1.4rem 0 .4rem;color:var(--ink-soft)}
p{margin:0 0 1rem}
a{color:var(--accent)}
ul,ol{margin:0 0 1rem 1.3rem}
li{margin:.3rem 0}
code{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.87em;background:var(--surface-2);
padding:.1em .35em;border-radius:4px;overflow-wrap:anywhere}
td,th{overflow-wrap:anywhere}
pre{background:var(--surface-2);border:1px solid var(--line);border-radius:10px;padding:.9rem 1.1rem;
overflow-x:auto;margin:0 0 1.2rem}
pre code{background:none;padding:0}
.tw{overflow-x:auto;margin:0 0 1.4rem}
table{border-collapse:collapse;width:100%;font-family:Inter,system-ui,sans-serif;font-size:.85rem}
th{text-align:left;border-bottom:2px solid var(--line);padding:.5rem .6rem;font-weight:700;
text-transform:uppercase;letter-spacing:.04em;font-size:.72rem;color:var(--muted)}
td{border-bottom:1px solid var(--line);padding:.5rem .6rem;vertical-align:top}
.math{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.88rem;background:var(--surface-2);
border-left:3px solid var(--accent-2);padding:.85rem 1.1rem;margin:0 0 1.2rem;overflow-x:auto;white-space:pre-wrap}
.m{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.9em}
hr{border:0;border-top:1px solid var(--line);margin:2rem 0}
.toc{background:var(--surface-2);border:1px solid var(--line);border-radius:12px;padding:1.1rem 1.4rem;
margin:0 0 2.4rem;font-family:Inter,system-ui,sans-serif;font-size:.85rem}
.toc div{font-weight:800;text-transform:uppercase;letter-spacing:.08em;font-size:.7rem;color:var(--muted);margin-bottom:.5rem}
.toc a{display:block;text-decoration:none;padding:.16rem 0;color:var(--ink-soft)}
.toc a.l2{padding-left:1rem;font-size:.8rem;color:var(--muted)}
.toc a:hover{color:var(--accent)}
.back{font-family:Inter,system-ui,sans-serif;font-size:.85rem;margin-bottom:1.5rem}
.back a{text-decoration:none;font-weight:600}
@media print{
  body{font-size:10.5pt;padding:0;background:#fff;color:#000}
  .wrap{max-width:100%}
  .toc,.back{display:none}
  h2{page-break-after:avoid;border-top:none}
  h3,h4{page-break-after:avoid}
  table,pre,.math{page-break-inside:avoid}
  a{color:#000;text-decoration:none}
}
"""


def build_html(meta, body, toc):
    toc_html = "".join(
        f'<a class="l{lvl}" href="#{sid}">{ihtml.escape(txt)}</a>'
        for lvl, txt, sid in toc if txt.lower() not in ("abstract",))
    title = meta.get("title", "Paper")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{ihtml.escape(title)}</title>
<meta name="description" content="Full research paper: India's institutional and distributional transformation, 2004-2026.">
<meta name="author" content="{ihtml.escape(meta.get('author',''))}">
<link rel="canonical" href="https://someperspective.info/downloads/paper.html">
<meta property="og:title" content="{ihtml.escape(title)}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://someperspective.info/downloads/paper.html">
<meta property="og:image" content="https://someperspective.info/og-preview.png">
<meta name="twitter:card" content="summary_large_image">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body><div class="wrap">
<p class="back"><a href="../">&larr; Some Perspective</a> &nbsp;·&nbsp; <a href="paper.pdf">Download PDF</a></p>
<div class="hdr">
<span class="kicker">Working paper · v{ihtml.escape(meta.get('version','1.0'))}</span>
<h1>{ihtml.escape(title)}</h1>
<p class="byline">{ihtml.escape(meta.get('author',''))} &nbsp;·&nbsp; {ihtml.escape(meta.get('affiliation',''))}</p>
<p class="sub">{ihtml.escape(meta.get('date',''))} &nbsp;·&nbsp; Data vintage {ihtml.escape(meta.get('data_vintage',''))}
&nbsp;·&nbsp; {ihtml.escape(meta.get('license','CC BY 4.0'))}
&nbsp;·&nbsp; <a href="{ihtml.escape(meta.get('repository',''))}">Replication repository</a></p>
</div>
<nav class="toc"><div>Contents</div>{toc_html}</nav>
{body}
</div></body></html>
"""


def find_chromium():
    for p in ("/opt/pw-browsers/chromium", shutil.which("chromium"),
              shutil.which("chromium-browser"), shutil.which("google-chrome")):
        if p and os.path.exists(p):
            return p
    return None


def build_pdf(html_path, pdf_path):
    exe = find_chromium()
    if not exe:
        return False, "no Chromium found"
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [exe, "--headless", "--disable-gpu", "--no-sandbox",
               f"--user-data-dir={tmp}", "--no-pdf-header-footer",
               f"--print-to-pdf={pdf_path}", "file://" + html_path]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=180)
        except subprocess.TimeoutExpired:
            return False, "Chromium timed out"
    if not os.path.exists(pdf_path):
        return False, (r.stderr.decode()[:200] or "no output")
    return True, None


def main():
    meta, md = split_front_matter(open(SRC, encoding="utf-8").read())
    body, toc = render(md)
    html_out = build_html(meta, body, toc)

    old = open(OUT_HTML, encoding="utf-8").read() if os.path.exists(OUT_HTML) else None
    changed = old != html_out

    if CHECK:
        if changed:
            print("STALE: downloads/paper.html does not match paper/paper.md — run tools/build_paper.py")
            sys.exit(1)
        if not os.path.exists(OUT_PDF):
            print("STALE: downloads/paper.pdf is missing — run tools/build_paper.py")
            sys.exit(1)
        print(f"Paper artifacts up to date ({len(md.split())} words).")
        return

    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    with open(OUT_HTML, "w", encoding="utf-8") as fh:
        fh.write(html_out)
    print(f"Wrote {os.path.relpath(OUT_HTML, ROOT)} ({len(html_out):,} bytes, {len(md.split()):,} words)")

    ok, err = build_pdf(OUT_HTML, OUT_PDF)
    if ok:
        print(f"Wrote {os.path.relpath(OUT_PDF, ROOT)} ({os.path.getsize(OUT_PDF):,} bytes)")
    else:
        print(f"PDF skipped: {err}")


if __name__ == "__main__":
    main()
