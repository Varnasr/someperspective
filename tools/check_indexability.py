#!/usr/bin/env python3
"""Every published page is either indexed on purpose or excluded on purpose.

    python3 tools/check_indexability.py

A page that is in neither the sitemap nor an exclusion is a page the site
publishes without having decided to. That is how `tools/walkthrough_shell.html`
came to be live: it is the build input `build_site.py` copies verbatim into
`walkthrough/index.html`, it sits in the published tree, it was crawlable, and
landing on it directly renders the deck engine with `DATA = null`, so a visitor
gets the chrome and no slides.

Note that the shell **must not** carry a `noindex` meta tag. It is copied byte
for byte into the real walkthrough, which the sitemap gives priority 0.9, so a
tag there would deindex the page it builds. The exclusion belongs in
robots.txt, which the build does not copy.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
checks = 0


def check(name, ok, detail=''):
    global checks
    checks += 1
    if not ok:
        errors.append('%s: %s' % (name, detail))


def read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8', errors='replace') as fh:
        return fh.read()


def canon(path):
    path = path.strip('/')
    if path.endswith('index.html'):
        path = path[:-len('index.html')].strip('/')
    return path or 'index'


def main():
    pages = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {'.git', 'node_modules', '.github'}]
        for f in filenames:
            if f.endswith('.html'):
                pages.append(os.path.relpath(os.path.join(dirpath, f), ROOT).replace('\\', '/'))
    pages.sort()
    check('there are pages to check', pages, 'none found')

    sitemap = read('sitemap.xml')
    indexed = {canon(re.sub(r'^https?://[^/]+/?', '', x))
               for x in re.findall(r'<loc>([^<]+)</loc>', sitemap)}

    robots = read('robots.txt')
    disallowed = [d.strip() for d in re.findall(r'^\s*Disallow:\s*(\S+)', robots, re.M | re.I)]
    check('robots.txt names the sitemap', 'sitemap.xml' in robots.lower(), 'absent')

    stray = []
    for page in pages:
        if canon(page) in indexed:
            continue
        body = read(page)
        if re.search(r'<meta[^>]*name=["\']?robots["\']?[^>]*noindex', body, re.I):
            continue
        if any(d != '/' and page.startswith(d.lstrip('/')) for d in disallowed):
            continue
        stray.append(page)
    check('every page is indexed on purpose or excluded on purpose', not stray,
          '%d neither in sitemap.xml nor noindexed nor disallowed: %s' % (len(stray), stray))

    # The shell is copied verbatim into the real page, so a noindex on it
    # would take the walkthrough out of the index along with it.
    shell = 'tools/walkthrough_shell.html'
    if os.path.exists(os.path.join(ROOT, shell)):
        check('the walkthrough shell carries no noindex meta tag',
              not re.search(r'<meta[^>]*name=["\']?robots["\']?[^>]*noindex', read(shell), re.I),
              'build_site.py copies this file byte for byte into '
              'walkthrough/index.html, so the tag would deindex the real page')
        check('the walkthrough shell is disallowed in robots.txt',
              any(shell.startswith(d.lstrip('/')) for d in disallowed if d != '/'),
              'it is a build input sitting in the published tree and renders '
              'an empty deck if a visitor lands on it')

    if errors:
        print('FAIL: %d of %d checks' % (len(errors), checks))
        for e in errors:
            print('  - %s' % e)
        return 1
    print('PASS: %d checks (%d pages)' % (checks, len(pages)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
