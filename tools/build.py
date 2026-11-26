"""Assemble the static pages for Topography Consulting LLC.

Usage (from the repo root):
    python3 tools/build.py site                                   # staging (default)
    SITE_ENV=production SITE_URL=https://www.topographyllc.com python3 tools/build.py site

Staging builds (the default) emit `noindex`, a robots.txt that disallows all
crawling, no canonical URLs and no sitemap, so a preview URL never competes
with the real site in search results. Production builds require SITE_URL and
emit canonical/Open Graph URLs, an indexable robots.txt and sitemap.xml.

FORM_ENDPOINT: leave empty until a form service (e.g. Formspree) has been
approved, configured and tested. While empty, the contact form composes an
email in the visitor's mail app and says so; it never claims to send anything.
"""
import glob, json, os, re, sys

SITE = sys.argv[1] if len(sys.argv) > 1 else "site"
ENV = os.environ.get("SITE_ENV", "staging").strip().lower()
URL = os.environ.get("SITE_URL", "").strip().rstrip("/")
FORM_ENDPOINT = os.environ.get("FORM_ENDPOINT", "").strip()
if ENV not in ("staging", "production"):
    sys.exit("SITE_ENV must be 'staging' or 'production'")
if ENV == "production" and not URL.startswith("https://"):
    sys.exit("Production builds need SITE_URL, e.g. SITE_URL=https://www.topographyllc.com")
PROD = ENV == "production"

EMAIL = "marcie@topographyllc.com"
PHONE_DISPLAY = "+1 805-331-0740"
PHONE_HREF = "+18053310740"
YEAR = 2026

ARROW = ('<svg class="i-arrow" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" '
         'stroke-width="1.5" aria-hidden="true" focusable="false"><path d="M4 12h15M13 6l6 6-6 6"/></svg>')


# ---------------------------------------------------------------------------
# Images: <picture> with WebP srcset + original JPEG fallback
# ---------------------------------------------------------------------------
def _dims(name):
    with open(os.path.join(SITE, "assets/img", name + ".jpg"), "rb") as f:
        data = f.read()
    i = 2
    while i < len(data):
        if data[i] != 0xFF: i += 1; continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h = int.from_bytes(data[i + 5:i + 7], "big"); w = int.from_bytes(data[i + 7:i + 9], "big")
            return w, h
        i += 2 + int.from_bytes(data[i + 2:i + 4], "big")
    raise ValueError(name)


def pic(name, alt, sizes, cls="", eager=False, pos=None):
    w, h = _dims(name)
    widths = sorted(int(re.search(r"-(\d+)\.webp$", p).group(1))
                    for p in glob.glob(os.path.join(SITE, "assets/img/opt", name + "-*.webp")))
    srcset = ", ".join(f"assets/img/opt/{name}-{x}.webp {x}w" for x in widths)
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    style = f' style="object-position:{pos}"' if pos else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img{c} src="assets/img/{name}.jpg" alt="{alt}" width="{w}" height="{h}" {load}{style}></picture>')


# ---------------------------------------------------------------------------
# Logo: split the approved vector into its drawn elements (no geometry change)
# ---------------------------------------------------------------------------
LOGO = open(os.path.join(SITE, "assets/logo/Topography-Logo-White-Knockout.svg")).read()
LOGO_VIEWBOX = re.search(r'viewBox="([^"]+)"', LOGO).group(1)
_icon_d, _word_d = re.findall(r' d="([^"]+)"', LOGO)
_subs = [s.strip() for s in re.split(r"(?=M)", _icon_d) if s.strip()]
assert len(_subs) == 20, "Logo structure changed: re-check the subpath grouping below"

# Subpath indices, in drawing order of the approved file. Holes stay with the
# shape they cut (compass 11 + 12-16, bottom wave 0 + 1) so even-odd fill
# renders exactly as the original.
GROUPS = [
    ("waves",     [[0, 1], [2], [3]]),
    ("mountains", [[4], [5], [8]]),
    ("summit",    [[9], [10]]),
    ("compass",   [[11, 12, 13, 14, 15, 16]]),
    ("ring",      [[17], [18], [7], [6], [19]]),
]
_used = sorted(i for _, parts in GROUPS for p in parts for i in p)
assert _used == list(range(20)), "every logo subpath must be used exactly once"


def mark_svg():
    groups = []
    for name, parts in GROUPS:
        paths = "".join(f'<path d="{" ".join(_subs[i] for i in p)}"/>' for p in parts)
        groups.append(f'<g class="mark__g" data-g="{name}">{paths}</g>')
    # The route: a thin line through the centre of the emblem, from the sea to
    # the north point. Hidden unless the animation runs.
    route = ('<path class="mark__route" d="M512.5 648 C 505 606 520 566 512.5 528 S 505 456 512.5 418 '
             'S 520 330 512.5 268" pathLength="1"/>')
    return (f'<svg class="mark" viewBox="{LOGO_VIEWBOX}" role="img" aria-labelledby="mark-title" data-mark data-anim="pending">'
            f'<title id="mark-title">Topography Consulting LLC</title>'
            f'<g class="mark__art" fill="#FFFFFF" fill-rule="evenodd">{"".join(groups)}</g>'
            f'{route}'
            f'<g class="mark__word" fill="#FFFFFF" fill-rule="evenodd"><path d="{_word_d}"/></g></svg>')


def write_lockups():
    """Horizontal header lockup built from the approved emblem and wordmark
    vectors (same paths, placed side by side). Flagged for client approval."""
    s = 170 / 474.6
    word_w, word_h = 848.4 - 176.0, 801.2 - 676.0
    gap = 44
    vw = round(170 + gap + word_w, 1)
    for variant, icon_fill, word_fill, defs in [
        ("White", "#FFFFFF", "#FFFFFF", ""),
        ("Color", "url(#g)", "#0A3F68",
         '<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="232" x2="0" y2="549">'
         '<stop offset="0" stop-color="#215A39"/><stop offset="0.45" stop-color="#1C5246"/>'
         '<stop offset="1" stop-color="#094368"/></linearGradient></defs>'),
    ]:
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw} 170">{defs}'
               f'<g transform="scale({s:.5f}) translate(-270.9 -189.4)"><path fill="{icon_fill}" fill-rule="evenodd" d="{_icon_d}"/></g>'
               f'<g transform="translate({170 + gap - 176.0:.1f} {(170 - word_h) / 2 - 676.0:.1f})"><path fill="{word_fill}" fill-rule="evenodd" d="{_word_d}"/></g></svg>')
        open(os.path.join(SITE, f"assets/logo/Topography-Lockup-Horizontal-{variant}.svg"), "w").write(svg)
    return vw


LOCKUP_W = write_lockups()


# ---------------------------------------------------------------------------
# Shared page parts
# ---------------------------------------------------------------------------
def head(title, desc, path, extra="", preload=""):
    if PROD:
        abs_url = f"{URL}/{path}"
        seo = (f'<link rel="canonical" href="{abs_url}">\n<meta property="og:url" content="{abs_url}">\n'
               f'<meta property="og:image" content="{URL}/assets/logo/og-logo.png">\n')
    else:
        seo = ('<meta name="robots" content="noindex, nofollow">\n'
               '<meta property="og:image" content="assets/logo/og-logo.png">\n')
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{seo}<meta name="theme-color" content="#0E2836">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Topography Consulting LLC">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="assets/css/styles.css">
<script>document.documentElement.classList.replace("no-js","js")</script>
{extra}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
'''


def header(active):
    def item(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    cur_contact = ' aria-current="page"' if active == "contact" else ""
    return f'''<header class="site-header" data-header>
  <div class="wrap site-header__inner">
    <a class="brand" href="index.html" aria-label="Topography Consulting LLC, home">
      <img src="assets/logo/Topography-Lockup-Horizontal-White.svg" alt="" width="{LOCKUP_W:.0f}" height="170">
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="visually-hidden">Menu</span><i aria-hidden="true"></i><i aria-hidden="true"></i>
    </button>
    <nav class="nav" id="site-nav" aria-label="Primary">
      <ul>
        {item("index.html", "Home", "home")}
        {item("services.html", "Services", "services")}
        {item("about.html", "About", "about")}
      </ul>
      <a class="btn btn--line nav__cta" href="contact.html"{cur_contact}>Contact</a>
    </nav>
  </div>
</header>
'''


FOOTER = f'''<footer class="site-footer">
  <div class="wrap site-footer__top">
    <div class="site-footer__brand">
      <img src="assets/logo/Topography-Logo-White-Knockout.svg" alt="Topography Consulting LLC" width="152" height="132" loading="lazy">
      <p>Environmental Compliance Solutions</p>
    </div>
    <nav class="site-footer__nav" aria-label="Footer">
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="services.html">Services</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </nav>
    <div class="site-footer__contact">
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="tel:{PHONE_HREF}">{PHONE_DISPLAY}</a>
      <p>Sedona, Arizona<br>Serving clients globally</p>
    </div>
  </div>
  <div class="wrap site-footer__base">
    <p>&copy; <span data-year>{YEAR}</span> Topography Consulting LLC</p>
  </div>
  <div class="site-footer__contours" aria-hidden="true"></div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''


def cta(tone="forest", title="Let&rsquo;s discuss your compliance needs.",
        text="Practical guidance for the environmental challenges facing the maritime industry."):
    return f'''<section class="section cta cta--{tone} on-dark">
  <div class="contours" aria-hidden="true"></div>
  <div class="wrap cta__inner">
    <h2 class="h2 reveal">{title}</h2>
    <p class="lead reveal">{text}</p>
    <p class="reveal"><a class="btn" href="contact.html">Get in Touch {ARROW}</a></p>
  </div>
</section>
'''


# ---------------------------------------------------------------------------
# Structured data (facts supplied by the client only)
# ---------------------------------------------------------------------------
def jsonld():
    data = {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": "Topography Consulting LLC", "slogan": "Environmental Compliance Solutions",
        "email": EMAIL, "telephone": "+1-805-331-0740",
        "address": {"@type": "PostalAddress", "addressLocality": "Sedona", "addressRegion": "AZ", "addressCountry": "US"},
        "areaServed": "Worldwide",
        "founder": {"@type": "Person", "name": "Marcie M. Merksamer"},
        "knowsAbout": ["Maritime environmental compliance", "Ballast water management",
                       "IMO Ballast Water Management Convention", "US Coast Guard ballast water regulations",
                       "EPA Vessel General Permit", "Biofouling management", "Hull biofouling",
                       "Aquatic invasive species", "Marine biosecurity"],
    }
    if PROD:
        data["url"] = URL + "/"
        data["logo"] = URL + "/assets/logo/og-logo.png"
    return '<script type="application/ld+json">' + json.dumps(data, separators=(",", ":")) + "</script>"


# =====================================================================
# HOME
# =====================================================================
SERVICES_INDEX = [
    ("ballast-water", "Ballast Water Management", "port-ship", "60% 50%",
     "Guidance on the IMO Ballast Water Management Convention, US Coast Guard regulations and the EPA Vessel General Permit, from management plans to day-to-day compliance."),
    ("biofouling", "Biofouling Management", "reef-wall", "40% 50%",
     "Practical preparation for hull biofouling requirements as international regulations develop, informed by direct involvement in that work."),
    ("regulatory", "Regulatory Compliance", "open-ocean", "50% 50%",
     "Clear answers on IMO, USCG, EPA, national, regional and classification society requirements, from someone who takes part at the IMO."),
    ("programs", "Compliance Programs and Project Management", "coast-aerial", "50% 60%",
     "Compliance programs, training and monitoring for ships, managed from scope to completion."),
]

svc_rows = "".join(f'''
        <li class="svc__item reveal" data-svc="{i}">
          <a class="svc__link" href="services.html#{key}">
            <h3 class="svc__title">{title}</h3>
            <p class="svc__text">{text}</p>
            <span class="svc__more">Learn more {ARROW}</span>
          </a>
        </li>''' for i, (key, title, img, pos, text) in enumerate(SERVICES_INDEX))
svc_media = "".join(f'''
        <div class="svc__img{' is-active' if i == 0 else ''}" data-svc-img="{i}">{pic(img, "", "(min-width: 1000px) 40vw, 1px", pos=pos)}</div>'''
                    for i, (key, title, img, pos, text) in enumerate(SERVICES_INDEX))

home = head("Topography Consulting | Maritime Environmental Compliance",
            "Ballast water management, biofouling management and maritime environmental compliance consulting. IMO, USCG and EPA expertise from an independent consultant with 26 years in the field.",
            "", extra=jsonld(),
            preload='<link rel="preload" as="image" type="image/webp" href="assets/img/opt/ocean-surface-1200.webp" imagesrcset="assets/img/opt/ocean-surface-640.webp 640w, assets/img/opt/ocean-surface-1200.webp 1200w, assets/img/opt/ocean-surface-2000.webp 2000w" imagesizes="100vw" fetchpriority="high">\n'
            ) + header("home") + f'''
<main id="main">
<section class="hero hero--home on-dark" data-hero>
  <div class="hero__media">{pic("ocean-surface", "", "100vw", eager=True, pos="50% 70%")}</div>
  <div class="hero__field" aria-hidden="true"><div class="hero__rings" data-rings></div></div>
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <p class="eyebrow">Environmental Compliance Solutions</p>
      <h1 class="display">Navigating complexity. <em>Charting solutions.</em></h1>
      <p class="hero__lede">Specialized environmental compliance consulting for the global maritime industry.</p>
      <div class="actions">
        <a class="btn" href="services.html">Explore Our Services {ARROW}</a>
        <a class="link" href="contact.html">Get in Touch</a>
      </div>
    </div>
    <div class="hero__mark">{mark_svg()}</div>
  </div>
</section>

<section class="section intro">
  <div class="intro__trace" aria-hidden="true"></div>
  <div class="wrap intro__grid">
    <h2 class="h2 reveal">A clearer path to compliance.</h2>
    <div>
      <p class="lead reveal">Topography Consulting helps the maritime industry navigate complex environmental regulations through specialized expertise, practical guidance and solutions tailored to each client.</p>
      <ul class="facts reveal">
        <li><strong>26 years</strong><span>of specialized experience</span></li>
        <li><strong>Global</strong><span>regulatory expertise</span></li>
        <li><strong>Independent</strong><span>environmental consulting</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--navy on-dark services-index">
  <div class="wrap">
    <div class="split-head">
      <h2 class="h2 reveal">Areas of expertise</h2>
      <p class="reveal">Ballast water and hull biofouling are the main ways ships carry aquatic invasive species. That is where we focus.</p>
    </div>
    <div class="svc" data-svc-root>
      <ol class="svc__list">{svc_rows}
      </ol>
      <div class="svc__media" aria-hidden="true">{svc_media}
      </div>
    </div>
  </div>
</section>

<section class="section founder">
  <div class="wrap founder__grid">
    <figure class="founder__portrait reveal">
      {pic("marcie-merksamer", "Marcie Merksamer, founder of Topography Consulting", "(min-width: 900px) 300px, 60vw")}
    </figure>
    <div class="founder__text">
      <h2 class="h2 reveal">Experience grounded in the real world.</h2>
      <p class="reveal">Marcie Merksamer is an environmental biologist who has worked on ballast water management and aquatic invasive species for 26 years. Her work runs from onboard system testing and crew training to type-approval dossiers, toxicology and risk assessment, and regulatory work at the International Maritime Organization.</p>
      <blockquote class="quote reveal"><p>&ldquo;We&rsquo;ve done everything from the boiler suit to the business suit.&rdquo;</p></blockquote>
      <p class="reveal"><a class="link" href="about.html">About Marcie</a></p>
    </div>
  </div>
</section>
''' + cta("forest") + "</main>\n" + FOOTER


# =====================================================================
# SERVICES
# =====================================================================
def acc(key, title, summary, items, note=""):
    lis = "".join(f"<li>{x}</li>" for x in items)
    note_html = f'<p class="acc__note">{note}</p>' if note else ""
    return f'''
    <article class="acc__item reveal" id="{key}">
      <h2 class="acc__title" id="{key}-title"><button type="button" class="acc__btn" aria-expanded="true" aria-controls="{key}-panel" data-acc-btn>
        <span>{title}</span><i class="acc__icon" aria-hidden="true"></i></button></h2>
      <p class="acc__summary">{summary}</p>
      <section class="acc__panel" id="{key}-panel" aria-labelledby="{key}-title">
        <div class="acc__inner"><div class="acc__body">
          <ul class="ticks">{lis}</ul>{note_html}
        </div></div>
      </section>
    </article>'''


services = head("Services | Ballast Water &amp; Biofouling Management Consulting",
                "Ballast water management (IMO BWM Convention, US Coast Guard, EPA Vessel General Permit), hull biofouling management, compliance programs and BWMS approvals for the maritime industry.",
                "services.html") + header("services") + f'''
<main id="main">
<section class="page-hero page-hero--split on-dark">
  <div class="contours" aria-hidden="true"></div>
  <div class="wrap page-hero__grid">
    <div class="page-hero__copy">
      <h1 class="h1">Specialized expertise. <em>Practical solutions.</em></h1>
      <p class="lead">Environmental compliance consulting tailored to the operational and regulatory needs of the maritime industry.</p>
    </div>
  </div>
  <div class="page-hero__media reveal-img">{pic("port-ship", "A loaded container ship alongside at a working port", "(min-width: 900px) 45vw, 100vw", eager=True)}</div>
</section>

<section class="section services-main">
  <div class="wrap">
    <div class="frameworks reveal" id="regulatory">
      <h2 class="frameworks__title">Regulatory frameworks</h2>
      <ul>
        <li>International Maritime Organization (IMO)</li>
        <li>IMO Ballast Water Management Convention</li>
        <li>United States Coast Guard (USCG)</li>
        <li>Environmental Protection Agency (EPA)</li>
        <li>EPA Vessel General Permit</li>
        <li>National and regional authorities</li>
        <li>Classification societies</li>
      </ul>
    </div>
    <div class="acc" data-acc>''' + acc(
    "ballast-water", "Ballast Water Management",
    "Guidance on meeting ballast water requirements set by the IMO, the US Coast Guard, the EPA, national and regional authorities and classification societies.",
    ["IMO Ballast Water Management Convention", "US Coast Guard ballast water regulations", "EPA Vessel General Permit",
     "Ballast water management plans", "Contingency planning", "Compliance monitoring and operational guidance"],
    "When you need a clear reading of which requirements apply to your vessels and trade, and a practical plan for meeting them.") + acc(
    "biofouling", "Biofouling Management",
    "Hull biofouling is the other main pathway for aquatic invasive species. We help clients prepare as international requirements develop.",
    ["Guidance on developing international biofouling management requirements", "Biofouling management planning and strategy",
     "Marine biosecurity risk considerations", "Connections to technology developers, service providers and the scientific community"],
    "Topography is involved in the development of international biofouling management regulations and brings more than two decades of ballast water experience to the work.") + acc(
    "programs", "Compliance Programs and Project Management",
    "Environmental compliance programs for ships, and the project management to put them in place.",
    ["Environmental compliance program development", "Training programs", "Compliance monitoring programs",
     "Coordination among owners, technology suppliers, service providers and regulators", "Implementation support"],
    "Each engagement is scoped to the project and managed with honesty and integrity, so goals are met as efficiently and cost-effectively as possible.") + acc(
    "approvals", "System Approvals and Risk Assessment",
    "Support for ballast water management system approvals, with in-depth knowledge of chemical-based systems.",
    ["BWMS approvals through classification societies and international administrations", "Aquatic toxicology for chemical-based systems",
     "Environmental and human health risk assessment of disinfection by-products", "Dossier preparation and data analysis",
     "Regulatory agency interactions", "Onboard testing logistics"]) + f'''
    </div>
  </div>
</section>

<section class="section section--navy on-dark clients">
  <div class="wrap clients__grid">
    <h2 class="h2 reveal">Who we work with</h2>
    <ul class="clients__list reveal">
      <li>Shipowners and operators</li>
      <li>Technology developers</li>
      <li>Equipment manufacturers</li>
      <li>Maritime service providers</li>
      <li>Regulatory bodies</li>
      <li>Industry associations, including BEMA</li>
    </ul>
  </div>
</section>

<section class="section section--sand engagement">
  <div class="wrap engagement__grid">
    <div class="reveal">
      <h2 class="h3">How engagements work</h2>
      <p>Every engagement is scoped to the project and billed at an hourly consulting rate. There are no fixed packages.</p>
    </div>
    <div class="reveal">
      <h2 class="h3">Onboard sampling and testing</h2>
      <p>Topography provides consulting and compliance guidance. For onboard compliance sampling and testing, we refer clients to EnviroManagement, Inc., the environmental services company Marcie co-founded in 2002.</p>
    </div>
  </div>
</section>
''' + cta("ocean") + "</main>\n" + FOOTER


# =====================================================================
# ABOUT
# =====================================================================
about = head("About Marcie Merksamer | Topography Consulting",
             "Marcie M. Merksamer: environmental biologist with 26 years in aquatic invasive species and ballast water management, founder of Topography Consulting LLC and Secretary-General of BEMA.",
             "about.html") + header("about") + f'''
<main id="main">
<section class="page-hero page-hero--about on-dark">
  <div class="contours" aria-hidden="true"></div>
  <div class="wrap page-hero__grid">
    <div class="page-hero__copy">
      <p class="eyebrow">About</p>
      <h1 class="h1">Marcie M. Merksamer</h1>
      <p class="lead">Founder of Topography Consulting LLC. Environmental biologist. Twenty-six years helping the maritime industry manage aquatic invasive species.</p>
    </div>
  </div>
</section>

<section class="section bio">
  <div class="wrap bio__grid">
    <figure class="bio__portrait reveal">
      {pic("marcie-merksamer", "Portrait of Marcie Merksamer", "(min-width: 900px) 300px, 70vw")}
    </figure>
    <div class="bio__text">
      <h2 class="h2 reveal">Professional background</h2>
      <div class="prose reveal">
        <p>Trained as an environmental biologist, Marcie has worked on aquatic invasive species and ballast water management for 26 years, 24 of them as an independent environmental consultant in the maritime sector.</p>
        <p>Much of that work has involved helping clients obtain approvals for ballast water management systems through classification societies and international administrations. That has meant research on aquatic toxicology for chemical-based systems, environmental and human health risk assessments of disinfection by-products, dossier preparation, data analysis and complex agency interactions.</p>
        <p>She also knows the practical side, from the logistics of testing systems on board ships to their operation, maintenance and crew training. She now applies that experience to biofouling management, with a constant aim: productive working relationships between scientists, technology developers, industry and regulators.</p>
      </div>
    </div>
  </div>
</section>

<section class="story on-dark">
  <div class="story__media reveal-img">{pic("peaks-clouds", "Mountain peaks rising above a sea of cloud at first light", "(min-width: 900px) 50vw, 100vw")}</div>
  <div class="story__text">
    <h2 class="h2 reveal">Why Topography</h2>
    <p class="reveal">Marcie plans her own explorations on paper maps and charts, on land and at sea. Their lines show where the peaks and valleys are, how hard the climb will be and where the coastline offers safe harbor. They also show that there is more than one way to a destination: over, under, around or through.</p>
    <p class="reveal">The ocean has a topography too, in the peaks and valleys of its waves. The name reflects a passion for the planet, from the mountains to the sea, and a commitment to protecting it.</p>
    <blockquote class="quote reveal"><p>&ldquo;No problems; only solutions.&rdquo;</p></blockquote>
  </div>
</section>

<section class="section section--sand experience">
  <div class="wrap experience__grid">
    <div>
      <h2 class="h2 reveal">Experience and qualifications</h2>
      <p class="reveal">Twenty-six years in aquatic invasive species and ballast water management. Twenty-four years as an independent environmental consultant in the maritime sector.</p>
    </div>
    <ol class="timeline reveal">
      <li><span class="timeline__when">Today</span><div><h3>Founder and Owner</h3><p>Topography Consulting LLC</p></div></li>
      <li><span class="timeline__when">2018</span><div><h3>Co-founder and Secretary-General</h3><p>Biosecurity &amp; Environmental Marine Association (BEMA), a non-profit, technically based industry association with Consultative Status at the IMO. Marcie represents BEMA on the delegation to the IMO.</p></div></li>
      <li><span class="timeline__when">2002</span><div><h3>Co-founder and former Vice President</h3><p>EnviroManagement, Inc., an environmental services and consulting company</p></div></li>
      <li><span class="timeline__when">Education</span><div><h3>B.S., Biological Sciences</h3><p>Concentration in Environmental Science, California Polytechnic State University, San Luis Obispo</p></div></li>
    </ol>
  </div>
</section>
''' + cta("navy") + "</main>\n" + FOOTER


# =====================================================================
# CONTACT
# =====================================================================
form_mode = "endpoint" if FORM_ENDPOINT else "email"
form_attrs = (f'action="{FORM_ENDPOINT}" method="POST"' if FORM_ENDPOINT else 'action="#" method="get"')
submit_label = "Send message" if FORM_ENDPOINT else "Continue in your email app"
form_note = ("" if FORM_ENDPOINT else
             f'<p class="form__note" id="form-note">This opens a pre-filled message in your email app. You can also write directly to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>')


def field(fid, label, control, required=True):
    req = '<span class="field__req" aria-hidden="true">*</span>' if required else '<span class="field__opt">Optional</span>'
    return (f'<div class="field"><label for="{fid}">{label} {req}</label>{control}'
            f'<p class="field__error" id="{fid}-error" hidden></p></div>')


contact = head("Contact | Topography Consulting LLC",
               "Contact Topography Consulting LLC about ballast water management, biofouling management and maritime environmental compliance. Based in Sedona, Arizona, serving clients globally.",
               "contact.html") + header("contact") + f'''
<main id="main">
<section class="page-hero page-hero--contact on-dark">
  <div class="contours" aria-hidden="true"></div>
  <div class="wrap page-hero__grid">
    <div class="page-hero__copy">
      <h1 class="h1">Let&rsquo;s discuss your compliance needs.</h1>
    </div>
  </div>
</section>

<section class="section contact">
  <div class="wrap contact__grid">
    <dl class="contact__details reveal">
      <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      <div><dt>Phone</dt><dd><a href="tel:{PHONE_HREF}">{PHONE_DISPLAY}</a></dd></div>
      <div><dt>Location</dt><dd>Sedona, Arizona<br><span>Serving clients globally</span></dd></div>
    </dl>

    <div class="contact__form reveal">
      <h2 class="h3">Send a note</h2>
      <form class="form" {form_attrs} data-form data-mode="{form_mode}" data-email="{EMAIL}" novalidate{' aria-describedby="form-note"' if not FORM_ENDPOINT else ''}>
        <div class="form__row">
          {field("name", "Full name", '<input id="name" name="name" type="text" autocomplete="name" required aria-describedby="name-error">')}
          {field("company", "Company", '<input id="company" name="company" type="text" autocomplete="organization">', required=False)}
        </div>
        {field("email", "Email address", '<input id="email" name="email" type="email" autocomplete="email" required aria-describedby="email-error">')}
        {field("interest", "Area of interest", """<select id="interest" name="interest">
            <option>Ballast water management</option>
            <option>Biofouling management</option>
            <option>Regulatory compliance</option>
            <option>Compliance programs and project management</option>
            <option>System approvals and risk assessment</option>
            <option>Something else</option>
          </select>""", required=False)}
        {field("message", "Message", '<textarea id="message" name="message" rows="6" required aria-describedby="message-error"></textarea>')}
        <div class="form__hp" aria-hidden="true"><label for="website">Leave this field empty</label><input id="website" name="_gotcha" type="text" tabindex="-1" autocomplete="off"></div>
        <div class="form__actions">
          <button class="btn btn--dark" type="submit">{submit_label} {ARROW}</button>
        </div>
        {form_note}
        <p class="form__status" role="status" aria-live="polite" data-form-status></p>
      </form>
      <noscript><p class="form__note">The form needs JavaScript. Please email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_HREF}">{PHONE_DISPLAY}</a>.</p></noscript>
    </div>
  </div>
</section>
</main>
''' + FOOTER


# ---------------------------------------------------------------------------
for name, html in [("index.html", home), ("services.html", services), ("about.html", about), ("contact.html", contact)]:
    html = re.sub(r"\n\s*\n\s*\n+", "\n\n", html)
    open(os.path.join(SITE, name), "w", encoding="utf-8").write(html)
    print(name, len(html) // 1024, "KB")

PAGES = ["", "services.html", "about.html", "contact.html"]
if PROD:
    open(os.path.join(SITE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {URL}/sitemap.xml\n")
    open(os.path.join(SITE, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{URL}/{p}</loc></url>\n" for p in PAGES) + "</urlset>\n")
else:
    open(os.path.join(SITE, "robots.txt"), "w").write("# Staging build: keep out of search results.\nUser-agent: *\nDisallow: /\n")
    if os.path.exists(os.path.join(SITE, "sitemap.xml")):
        os.remove(os.path.join(SITE, "sitemap.xml"))
print(f"built for {ENV}" + (f" at {URL}" if PROD else " (noindex, no sitemap)"))
