#!/usr/bin/env python3
"""
PROJECTIONS — the site's own projections, for series no institution forecasts.

Writes data/projections.json. Run: python3 tools/build_projections.py (--check
to fail if the committed file is stale).

The method is deliberately small, because the series are short and a short
series cannot support a rich model:

  1. Three candidate models, each fitted only on data before the forecast
     origin: no change from the last value; the last value plus the average
     yearly change over the previous five years; and a straight-line trend
     fitted to the previous eight years.
  2. Rolling-origin back-test: for every origin with enough history, each
     model forecasts one to four years ahead, and the forecast is scored
     against what was later published.
  3. The model with the smallest back-test error is used. Its interval at
     each horizon is the 80th percentile of its absolute back-test errors at
     that horizon. Where the back-test has fewer than three errors at a
     horizon, the one-year-ahead error is scaled by the square root of the
     horizon, and the output says so.

Projections are never observations. data.json is not touched, no average,
index or scorecard reads this file, and charts draw these points as hollow
markers with their interval.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "projections.json")
YEARS = list(range(2004, 2027))

# key: (label, the publisher's last year, years to project, minimum training points)
TARGETS = {
    "top1Share": ("Income share of the top 1%", 2026, 6),
    "bottom50Share": ("Income share of the bottom 50%", 2026, 6),
    "formalEmployment": ("Workers in regular jobs with social security", 2026, 3),
}
MAX_H = 4


def series(d, key):
    era = d["eraHistory"].get(key) or [None] * 10
    return list(era) + list(d["economic"][key])


def m_last(hist, h):
    return hist[-1]


def m_drift(hist, h):
    k = min(5, len(hist) - 1)
    if k < 1:
        return hist[-1]
    return hist[-1] + h * (hist[-1] - hist[-1 - k]) / k


def m_trend(hist, h):
    y = hist[-8:]
    n = len(y)
    if n < 3:
        return hist[-1]
    xm = (n - 1) / 2
    ym = sum(y) / n
    b = sum((i - xm) * (v - ym) for i, v in enumerate(y)) / sum((i - xm) ** 2 for i in range(n))
    return ym + b * (n - 1 - xm + h)


METHOD = ("Three simple models compete: no change from the last value, the last value plus the average yearly "
          "change over the previous five years, and a straight line fitted to the previous eight years. Each is "
          "scored by a rolling-origin back-test: from every starting year with enough history it forecasts one to "
          "four years ahead using only the data available then, and the forecast is compared with what was later "
          "published. The model with the smallest average error is used. The interval is the 80th percentile of "
          "its back-test errors at that horizon, never narrower than at a shorter horizon; where fewer than three "
          "errors exist at a horizon, the one-year error is scaled by the square root of the horizon.")

MODELS = {
    "no change": m_last,
    "recent average change": m_drift,
    "eight-year straight line": m_trend,
}


def backtest(obs, min_train):
    """Return {model: {h: [errors]}} over every rolling origin."""
    errs = {m: {h: [] for h in range(1, MAX_H + 1)} for m in MODELS}
    for t in range(min_train, len(obs)):
        hist = obs[:t]
        for h in range(1, MAX_H + 1):
            if t - 1 + h < len(obs):
                actual = obs[t - 1 + h]
                for name, f in MODELS.items():
                    errs[name][h].append(f(hist, h) - actual)
    return errs


def rmse(e):
    return math.sqrt(sum(x * x for x in e) / len(e)) if e else None


def q80(e):
    a = sorted(abs(x) for x in e)
    return a[min(len(a) - 1, math.ceil(0.8 * len(a)) - 1)]


def build():
    d = json.load(open(os.path.join(ROOT, "data.json"), encoding="utf-8"))
    out = {"generated_from": "data.json", "method": METHOD, "series": {}}
    for key, (label, last, min_train) in TARGETS.items():
        vals = series(d, key)
        first = next(i for i, v in enumerate(vals) if v is not None)
        lastobs = max(i for i, v in enumerate(vals) if v is not None)
        obs = vals[first:lastobs + 1]
        if any(v is None for v in obs):
            raise SystemExit(f"{key}: gap inside the observed span; the back-test assumes none")
        errs = backtest(obs, min_train)
        score = {m: rmse([x for h in errs[m] for x in errs[m][h]]) for m in MODELS}
        best = min(score, key=lambda m: score[m])
        f = MODELS[best]
        e1 = errs[best][1]
        points = []
        prev = 0.0
        horizon = YEARS.index(last) - (first + len(obs) - 1)
        for h in range(1, horizon + 1):
            e = errs[best].get(h, [])
            if len(e) >= 3:
                half, basis = q80(e), f"80th percentile of {len(e)} back-test errors at {h} years"
            else:
                half, basis = q80(e1) * math.sqrt(h), "one-year error scaled by the square root of the horizon"
            half = max(half, prev)
            prev = half
            v = f(obs, h)
            points.append({"year": YEARS[first + len(obs) - 1 + h], "value": round(v, 1),
                           "lo": round(v - half, 1), "hi": round(v + half, 1), "interval": basis})
        out["series"][key] = {
            "label": label,
            "observed_to": YEARS[lastobs],
            "model": best,
            "backtest_rmse": {m: round(score[m], 2) for m in MODELS},
            "backtest_n": {h: len(errs[best][h]) for h in errs[best]},
            "points": points,
        }
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


def main():
    text = build()
    if "--check" in sys.argv:
        if not os.path.exists(OUT) or open(OUT, encoding="utf-8").read() != text:
            print("FAIL: data/projections.json is stale. Run python3 tools/build_projections.py")
            sys.exit(1)
        print("Projections up to date.")
        return
    open(OUT, "w", encoding="utf-8").write(text)
    print("Wrote data/projections.json")


if __name__ == "__main__":
    main()
