#!/usr/bin/env python3
"""
DATA PARITY GUARD — fail loudly if data.json drifts from the canonical index
engine, or if a published estimate sits on a year that already has an outturn.

The site keeps a copy of the economic/eraHistory series inline (so it renders
even when data.json can't be fetched). That convenience is a correctness hazard:
two copies can silently disagree. This guard makes drift impossible to merge.

Checks:
  1. Every shared numeric array in FALLBACK_DATA.economic   == data.json economic
  2. Every shared numeric array in FALLBACK_DATA.eraHistory == data.json eraHistory
  3. data.json ssi/fci/dqi (both eras) == data/compute_indices.py (the engine)

Exit 0 if all good; exit 1 with a diff if not.  Run: python3 tools/check_data_parity.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _slice_block(text, key):
    """Return the brace-balanced { ... } body following `key:` (or `"key":`)."""
    m = re.search(r'["\']?' + re.escape(key) + r'["\']?\s*[:=]\s*\{', text)
    if not m:
        return None
    i = text.index('{', m.start())
    depth, j = 0, i
    while j < len(text):
        if text[j] == '{':
            depth += 1
        elif text[j] == '}':
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
        j += 1
    return None


def _parse_arrays(block):
    """key -> list, for every `key: [ ... ]` of JSON-parseable values in block."""
    out = {}
    for k, arr in re.findall(r'(\w+)\s*:\s*(\[[^\]]*\])', block):
        try:
            out[k] = json.loads(arr)
        except json.JSONDecodeError:
            pass
    return out


def main():
    errors = []

    data = json.load(open(os.path.join(ROOT, 'data.json'), encoding='utf-8'))
    # 1: the old dashboard kept an inline copy of the series. The generated
    # /explore/ pages read data.json at build time, so there is no second copy
    # to drift. What can drift is the estimates block: an estimate for a year
    # that also has an outturn would be drawn twice.
    years = data['economic']['years']
    for key, est in (data.get('estimates') or {}).items():
        if key.startswith('_'):
            continue
        if key not in data['economic']:
            errors.append(f'estimates.{key}: not a series in economic')
            continue
        for y in est:
            if int(y) not in years:
                errors.append(f'estimates.{key}.{y}: outside {years[0]}-{years[-1]}')
            elif data['economic'][key][years.index(int(y))] is not None:
                errors.append(f'estimates.{key}.{y}: the year also has an outturn')

    # 3: data.json indices must equal the canonical engine
    sys.path.insert(0, os.path.join(ROOT, 'data'))
    try:
        import compute_indices as ci
        out = ci.build()
        fidx = {y: i for i, y in enumerate(out['years'])}
        for block_name, years in (('economic', range(2014, 2027)), ('eraHistory', range(2004, 2014))):
            blk = data[block_name]
            yrs = blk['years']
            for k in ('ssi', 'fci', 'dqi'):
                for y in years:
                    got = blk[k][yrs.index(y)]
                    exp = out[k][fidx[y]]
                    if abs(got - exp) > 1e-9:
                        errors.append(f'{block_name}.{k} {y}: data.json {got} != engine {exp}')
    except Exception as e:  # noqa: BLE001
        errors.append(f'could not cross-check against compute_indices.py: {e}')

    if errors:
        print('DATA PARITY FAILED:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    print('Data parity OK: estimates do not overlap outturns, data.json == compute_indices.py')


if __name__ == '__main__':
    main()
