#!/usr/bin/env python3
"""
The owner's writing rules, the part a regex can hold.

Plain full sentences, facts and explanations, no em dashes, no flourishes, no
"X, not Y". This check fails on em dashes (as a character or an entity), on a
double hyphen standing in for one, on "not only" and on the stock words below,
in every published page and in the sources the pages are built from.

It cannot see a fragment, a punchline ending or an "X, not Y" without the word
"not". Read what you write.

Verbatim quotations and the titles of cited works are left as written. Each
exemption names the file, the exact text and the reason, and a stale one
fails, so the list cannot rot into a blindfold.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOURCES = [
    "index.html", "data.json", "paper/paper.md", "data/METHODOLOGY.md",
    "data/updates.json", "data/features.json", "data/walkthrough.json",
    "data/inflation.json", "data/care.json", "tools/walkthrough_shell.html",
]
GENERATED_DIRS = ["analysis", "care", "inflation", "walkthrough", "downloads"]
GENERATED_FILES = ["updates.html", "feed.xml"]

DASH = re.compile(r"—|&mdash;|&#8212;|&#x2014;| -- ")

# "robust" is the econometric term (robust standard errors, robustness check)
# and "navigation" is the site's own menu; neither is on this list.
BANNED = re.compile(r"\b(" + "|".join([
    r"delv(e|es|ed|ing)", r"certainly", r"utili[sz]\w*", r"leverag(e|es|ed|ing)",
    r"streamlin\w*", r"harness\w*", r"foster(s|ed|ing)?", r"underscor\w*",
    r"enhanc\w*", r"testament", r"pivotal", r"intricat\w*", r"crucial\w*",
    r"transformative", r"groundbreaking", r"tapestry", r"landscape", r"paradigm\w*",
    r"synerg\w*", r"showcas\w*", r"meticulous\w*", r"notabl[ey]", r"noteworthy",
    r"seamless\w*", r"multifaceted", r"nuanced", r"holistic", r"invaluable",
    r"unparalleled", r"garner\w*", r"bolster\w*", r"elucidat\w*", r"interplay",
    r"underpin\w*", r"vibrant", r"empower\w*", r"amplif\w*", r"resonat\w*",
    r"realm", r"myriad", r"plethora", r"genuine(ly)?", r"honestly", r"truly",
    r"arguably", r"stark(er|est|ly)?", r"moreover", r"furthermore", r"additionally",
    r"ultimately", r"importantly", r"not only",
]) + r")\b", re.I)

# (file, exact text, reason). Keep each one a verbatim quotation or a title.
EXEMPT = [
    ("index.html", "Algorithm decides everything—one bad rating and income drops 40%.",
     "Data story quotation. The owner says it is a real person's words; source to be "
     "added beside it (asked 2026-10-10). Quotations stay verbatim."),
    ("index.html", "My son will never farm—I'll sell the land first.",
     "Data story quotation, as above."),
    ("index.html", "It's not a choice—it's survival.",
     "Data story quotation, as above."),
    ("index.html", "To read any number honestly is to ask who chose it",
     "Pull-quote from the owner's published primer, Reading the Indian Economy "
     "(16 June 2026), quoted as printed."),
]


def files():
    for rel in SOURCES + GENERATED_FILES:
        if os.path.exists(os.path.join(ROOT, rel)):
            yield rel
    for d in GENERATED_DIRS:
        for dirpath, _, names in os.walk(os.path.join(ROOT, d)):
            for n in sorted(names):
                if n.endswith((".html", ".md")):
                    yield os.path.relpath(os.path.join(dirpath, n), ROOT)


def main():
    bad = []
    used = set()
    for rel in files():
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        for i, ex in enumerate(EXEMPT):
            if ex[0] == rel and ex[1] in text:
                used.add(i)
                text = text.replace(ex[1], " " * len(ex[1]))
        for n, line in enumerate(text.splitlines(), 1):
            for m in DASH.finditer(line):
                bad.append(f"{rel}:{n}: em dash: ...{line[max(0, m.start()-50):m.end()+30]}...")
            for m in BANNED.finditer(line):
                bad.append(f"{rel}:{n}: '{m.group(0)}': ...{line[max(0, m.start()-50):m.end()+30]}...")
    stale = [EXEMPT[i] for i in range(len(EXEMPT)) if i not in used]
    for s in stale:
        bad.append(f"stale exemption, text no longer in {s[0]}: {s[1][:60]!r}")
    if bad:
        print("\n".join(bad[:200]))
        print(f"FAIL: {len(bad)} problem(s)")
        sys.exit(1)
    print(f"PASS: writing rules hold in every published page and its sources "
          f"({len(EXEMPT)} quotation exemptions)")


if __name__ == "__main__":
    main()
