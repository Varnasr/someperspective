"""
SOCIAL — the link-preview tags and the share row, shared by every builder.

Every page gets its own preview card, og/<name>.png, drawn by tools/build_og.py
from the page's own title and description. The name is derived from the
page's canonical URL, so a builder and the card generator agree on it without
either reading the other.

The share row is plain links: WhatsApp with the text already written, X,
LinkedIn and email. They work without JavaScript and load nothing from the
networks until a reader taps one. One small inline script adds "Copy link"
where the browser allows it.
"""
from html import escape
from urllib.parse import quote

SITE = "https://someperspective.info"
SITE_NAME = "Some Perspective"


def og_name(url):
    """https://someperspective.info/explore/economy/ -> explore-economy"""
    path = url.replace(SITE, "").split("#")[0].split("?")[0].strip("/")
    if not path:
        return "home"
    if path.endswith(".html"):
        path = path[:-5]
    if path.endswith("/index"):
        path = path[:-6]
    return path.replace("/", "-")


def og_image(url):
    return f"{SITE}/og/{og_name(url)}.png"


def head(title, desc, url, typ="website", alt=None):
    """Open Graph and Twitter tags for one page. Title and desc are plain text."""
    img = og_image(url)
    alt = alt or f"{title}. {SITE_NAME}, India 2004-2026."
    t, d, a = escape(title), escape(desc), escape(alt)
    return (
        f'<meta property="og:site_name" content="{SITE_NAME}">\n'
        f'<meta property="og:locale" content="en_IN">\n'
        f'<meta property="og:title" content="{t}">\n'
        f'<meta property="og:description" content="{d}">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:type" content="{typ}">\n'
        f'<meta property="og:image" content="{img}">\n'
        f'<meta property="og:image:width" content="1200">\n'
        f'<meta property="og:image:height" content="630">\n'
        f'<meta property="og:image:alt" content="{a}">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{t}">\n'
        f'<meta name="twitter:description" content="{d}">\n'
        f'<meta name="twitter:image" content="{img}">\n'
        f'<meta name="twitter:image:alt" content="{a}">\n'
    )


SHARE_CSS = """
.share{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin-top:1rem;font-size:.85rem}
.share span{font-weight:800;font-stretch:112.5%;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;margin-right:.25rem}
.share a,.share button{all:unset;cursor:pointer;display:inline-block;border:2px solid var(--ink,#0d0e12);padding:.3rem .7rem;
font-weight:700;color:var(--ink,#0d0e12);background:var(--paper,#f5f5f2);min-height:1.6rem;line-height:1.6rem}
.share a:hover,.share button:hover{background:var(--ink,#0d0e12);color:var(--paper,#f5f5f2)}
.share a:focus-visible,.share button:focus-visible{outline:3px solid var(--nda,#5a2a8c);outline-offset:2px}
"""


CONTACT_CSS = """
.contact{margin-top:.7rem;padding-top:.7rem;border-top:2px solid var(--ink,#0d0e12);max-width:40rem;color:var(--ink,#0d0e12)}
.contact a{color:var(--ink,#0d0e12);text-decoration:underline}
"""

CONTACT = ('<p class="contact">Need help setting out your story, what sets your work apart, the context, '
           'the return on investment and the projections? Pinpoint Ventures can help. Write to '
           '<a href="mailto:hello@pinpointventures.in?subject=Enquiry%20from%20someperspective.info">'
           'hello@pinpointventures.in</a> or message on '
           '<a href="https://wa.me/919871777110?text=Hi%20Pinpoint%20Ventures%2C%20I%20found%20you%20through%20'
           'someperspective.info.%20I%27d%20like%20to%20discuss%20a%20research%20or%20advisory%20engagement." '
           'target="_blank" rel="noopener">WhatsApp</a>.</p>')


def contact():
    """The Pinpoint Ventures contact line shared by every generated page's footer."""
    return CONTACT


def share(title, text, url):
    """A row of share links. `text` is the sentence the WhatsApp message carries."""
    msg = f"{title}\n{text}\n{url}" if text else f"{title}\n{url}"
    wa = "https://wa.me/?text=" + quote(msg)
    x = "https://twitter.com/intent/tweet?text=" + quote(title) + "&url=" + quote(url)
    li = "https://www.linkedin.com/sharing/share-offsite/?url=" + quote(url)
    mail = "mailto:?subject=" + quote(title) + "&body=" + quote(f"{text}\n\n{url}" if text else url)
    return (
        '<p class="share" aria-label="Share this page"><span>Share</span>'
        f'<a href="{escape(wa)}" rel="noopener" target="_blank">WhatsApp</a>'
        f'<a href="{escape(x)}" rel="noopener" target="_blank">X</a>'
        f'<a href="{escape(li)}" rel="noopener" target="_blank">LinkedIn</a>'
        f'<a href="{escape(mail)}">Email</a>'
        f'<button type="button" data-copy="{escape(url)}" hidden>Copy link</button></p>'
    )


COPY_JS = ("<script>document.querySelectorAll('[data-copy]').forEach(function(b){if(!navigator.clipboard)return;"
           "b.hidden=false;b.addEventListener('click',function(){navigator.clipboard.writeText(b.dataset.copy)"
           ".then(function(){b.textContent='Link copied';setTimeout(function(){b.textContent='Copy link';},2000);});});});</script>")
