#!/usr/bin/env python3
"""
What GitHub Pages publishes, and what it must not.

Until v2.48.0 the deploy uploaded the whole checkout. CLAUDE.md, .claude/,
.githooks/, the Tailwind source, the build tools and ai-image-prompts.md were
all served at guessable URLs, linked from nothing, so nobody noticed.

Every top-level entry in the repository has to be named here, as published or
as kept back. A new one fails the check until somebody decides which it is.

    python3 tools/check_publish.py             # check only (CI)
    python3 tools/check_publish.py --stage DIR # check, then copy the site to DIR
"""
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PUBLISHED = {
    ".nojekyll", "CNAME", "robots.txt", "sitemap.xml", "feed.xml",
    "manifest.json", "sw.js", "og-preview.png", "og-preview.svg",
    "favicon.svg", "favicon-32.png", "apple-touch-icon.png", "assets",
    "index.html", "updates.html", "data.json",
    "analysis", "care", "explore", "inflation", "walkthrough", "downloads", "fonts", "js",
    "data", "replication_code.py", "replication_code.R",
    "LICENSE", "CITATION.cff", "README.md", "data_dictionary.md",
}

KEPT_BACK = {
    ".git", ".github", ".claude", ".githooks", ".gitmessage", ".gitignore",
    ".gitattributes", ".editorconfig", "node_modules", "_site",
    "CLAUDE.md", "CONTRIBUTING.md", "CHANGELOG.md", "ROADMAP.md",
    "ai-image-prompts.md", "paper", "package.json", "package-lock.json", "src", "tools",
}

# Inside a published directory, these are never served.
SKIP_NAMES = {"__pycache__", ".DS_Store"}


def tracked_top_level():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                         text=True, check=True).stdout.split()
    return {p.split("/")[0] for p in out}


def published_files():
    for top in sorted(PUBLISHED):
        path = os.path.join(ROOT, top)
        if os.path.isfile(path):
            yield top
        elif os.path.isdir(path):
            for d, dirs, files in os.walk(path):
                dirs[:] = [x for x in dirs if x not in SKIP_NAMES]
                for f in files:
                    if f in SKIP_NAMES or f.endswith(".pyc"):
                        continue
                    yield os.path.relpath(os.path.join(d, f), ROOT)


REF = re.compile(r'''(?<![:\w-])(?:href|src)=["']([^"'#][^"']*)["']''')


def main():
    errors = []
    top = tracked_top_level()
    unnamed = sorted(top - PUBLISHED - KEPT_BACK)
    if unnamed:
        errors.append("top-level entries named neither published nor kept back: "
                      + ", ".join(unnamed))
    both = sorted(PUBLISHED & KEPT_BACK)
    if both:
        errors.append("named as both published and kept back: " + ", ".join(both))
    missing = sorted(p for p in PUBLISHED if not os.path.exists(os.path.join(ROOT, p)))
    if missing:
        errors.append("named as published but absent: " + ", ".join(missing))

    files = set(published_files())
    for rel in sorted(f for f in files if f.endswith(".html")):
        html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S)
        # explore/index.html carries <base href="/">, so its relative links
        # resolve from the site root, not from its own folder.
        base = "" if re.search(r'<base href="/"', html) else os.path.dirname(rel)
        for ref in REF.findall(html):
            if re.match(r"^(https?:|mailto:|data:|javascript:|//|\{)", ref):
                continue
            target = ref.split("#")[0].split("?")[0]
            if not target:
                continue
            if target.startswith("/"):
                path = target.lstrip("/")
            else:
                path = os.path.normpath(os.path.join(base, target))
            if path in ("", "."):
                continue
            if path.endswith("/") or os.path.isdir(os.path.join(ROOT, path)):
                path = os.path.join(path, "index.html")
            if path not in files:
                errors.append(f"{rel} links {ref}, which is not published")

    if errors:
        for e in errors:
            print("FAIL:", e)
        sys.exit(1)

    if "--stage" in sys.argv:
        dest = os.path.abspath(sys.argv[sys.argv.index("--stage") + 1])
        if os.path.exists(dest):
            shutil.rmtree(dest)
        for rel in files:
            os.makedirs(os.path.join(dest, os.path.dirname(rel)), exist_ok=True)
            shutil.copy2(os.path.join(ROOT, rel), os.path.join(dest, rel))
        print(f"staged {len(files)} files in {dest}")
    print(f"PASS: {len(files)} files published, every page link resolves, "
          f"{len(KEPT_BACK)} entries kept back")


if __name__ == "__main__":
    main()
