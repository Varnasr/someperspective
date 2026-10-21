"""The phone layout of the site header, shared by every builder that writes one.

Under 700px the two-column header (wordmark left of the seam, six links right of
it) cannot hold: the wordmark ran across the seam and printed over the links,
and the links wrapped to three rows beside it. On a phone the header is the
wordmark on its own row and the six links as a grid of 44px targets beneath it.
The links stay in the markup, so nothing depends on a script. The reading-font
button joins the nav at runtime, so it is lifted into the wordmark row.
"""

PHONE = """
.top{display:block;position:relative;background:var(--paper)}
.top::before{content:"";display:block;height:6px;background:linear-gradient(90deg,var(--field-upa) 0,var(--field-upa) calc(var(--seam) - 1px),var(--ink) calc(var(--seam) - 1px),var(--ink) calc(var(--seam) + 1px),var(--field-nda) calc(var(--seam) + 1px),var(--field-nda) 100%)}
.top>.l,.top>.r{padding:0;text-align:left}
.top .l{padding:.15rem 4.2rem .15rem 1rem;min-height:48px;display:flex;align-items:center}
.top .name{font-size:.82rem;letter-spacing:.02em;gap:.5rem;min-height:44px}
.top .name span{white-space:nowrap}
.top nav{display:grid;grid-template-columns:repeat(3,1fr);gap:0;font-size:.82rem;border-top:1px solid var(--line)}
.top nav a{display:flex;align-items:center;justify-content:center;text-align:center;min-height:44px;padding:.35rem .3rem;border-right:1px solid var(--line);border-bottom:1px solid var(--line);line-height:1.15}
.top nav a:nth-of-type(3n){border-right:0}
.top nav a:nth-of-type(n+4){border-bottom:0}
.top #dys-font-btn{position:absolute;top:8px;right:.6rem;min-width:44px;min-height:44px}
"""
