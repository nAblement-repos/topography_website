"""Assemble the static pages for Topography Consulting (shared header/footer)."""
import os, re, sys
SITE = sys.argv[1]
URL = "https://www.topographyllc.com"

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..500;1,9..144,300..500'
         '&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&family=Montserrat:wght@500;700&display=swap" rel="stylesheet">')

def head(title, desc, path, image="assets/img/hero-wave.jpg", extra=""):
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{URL}/{path}">
<meta name="theme-color" content="#0E2836">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Topography Consulting LLC">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{URL}/{path}">
<meta property="og:image" content="{URL}/{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="assets/css/styles.css">
{extra}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
'''

def header(active):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Topography Consulting LLC — home">
      <img class="logo-light" src="assets/logo/Topography-Icon-White-Knockout.svg" alt="" width="46" height="46">
      <img class="logo-dark" src="assets/logo/Topography-Icon-Color.svg" alt="" width="46" height="46">
      <span class="brand-text"><strong>TOPOGRAPHY</strong><span>CONSULTING LLC</span></span>
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Primary">
      {a("services.html", "Services", "services")}
      {a("services.html#approach", "Approach", "approach")}
      {a("about.html", "About", "about")}
      <a class="btn" href="contact.html"{' aria-current="page"' if active == "contact" else ''}>Contact</a>
    </nav>
  </div>
</header>
<div class="gauge" aria-hidden="true"><div class="gauge__track"><i class="gauge__mark"></i></div><span class="gauge__val">DEPTH 0000 M</span></div>
'''

FOOTER = '''<footer class="site-footer on-dark">
  <div class="contours contours--soft" aria-hidden="true"></div>
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="assets/logo/Topography-Logo-White-Knockout.svg" alt="Topography Consulting LLC" width="220" height="192" loading="lazy">
        <p>Environmental Compliance Solutions</p>
      </div>
      <div>
        <h4>Navigate</h4>
        <ul>
          <li><a href="services.html">Services</a></li>
          <li><a href="services.html#approach">Approach</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Focus</h4>
        <ul>
          <li><a href="services.html#ballast-water">Ballast water</a></li>
          <li><a href="services.html#biofouling">Biofouling</a></li>
          <li><a href="services.html#programs">Compliance programs</a></li>
          <li><a href="services.html#approvals">BWMS approvals</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:marcie@topographyllc.com">marcie@topographyllc.com</a></li>
          <li><a href="tel:+18053310740">+1 805-331-0740</a></li>
          <li><address>P.O. Box 20014<br>Sedona, AZ 86341</address></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> Topography Consulting LLC. All rights reserved.</span>
      <span class="coord">34.8697&deg; N &middot; 111.7610&deg; W &mdash; Serving clients worldwide</span>
    </div>
  </div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''

def cta(title='Where is your <em>compliance</em> headed?', text="Tell us about the vessel, the system or the regulation in front of you. Every engagement starts with listening."):
    return f'''<section class="section section--dark on-dark cta">
  <div class="contours" aria-hidden="true"></div>
  <div class="wrap">
    <p class="label reveal">Start a conversation</p>
    <div class="cta__row">
      <div>
        <h2 class="display reveal">{title}</h2>
        <p class="lede reveal" style="--d:.1s">{text}</p>
      </div>
      <div class="reveal" style="--d:.2s">
        <div class="cta__details mb-0">
          <a href="mailto:marcie@topographyllc.com">marcie@topographyllc.com</a>
          <a href="tel:+18053310740">+1 805-331-0740</a>
        </div>
        <p class="mt-2 mb-0"><a class="btn" href="contact.html">Get in touch {ARROW}</a></p>
      </div>
    </div>
  </div>
</section>
'''

# ---- inline peak figure (compass ring + draw-on contours) ----
peak = open(os.path.join(SITE, "assets/img/contours-peak.svg")).read()
paths = re.findall(r'<path[^>]*/>', peak)
paths = [p.replace('/>', ' stroke="currentColor"/>') for p in paths]
ticks = []
import math
for deg in range(0, 360, 5):
    r1 = 368 if deg % 45 else 352
    if deg % 90 == 0: r1 = 340
    a = math.radians(deg)
    ticks.append(f'<line class="tick" x1="{400+r1*math.sin(a):.1f}" y1="{400-r1*math.cos(a):.1f}" x2="{400+378*math.sin(a):.1f}" y2="{400-378*math.cos(a):.1f}" stroke-width="{1.2 if deg%90==0 else .7}"/>')
PEAK_FIG = f'''<figure class="figure-peak reveal" aria-hidden="true">
  <svg viewBox="0 0 800 800" fill="none">
    <defs><clipPath id="disc"><circle cx="400" cy="400" r="330"/></clipPath></defs>
    <circle class="ring" cx="400" cy="400" r="378"/>
    <circle class="ring" cx="400" cy="400" r="330"/>
    {''.join(ticks)}
    <text class="cardinal" x="400" y="14" text-anchor="middle">N</text>
    <text class="cardinal" x="794" y="405" text-anchor="end">E</text>
    <text class="cardinal" x="400" y="798" text-anchor="middle">S</text>
    <text class="cardinal" x="6" y="405">W</text>
    <g class="contour-art draw" clip-path="url(#disc)" stroke-linecap="round" stroke-linejoin="round">{''.join(paths)}</g>
  </svg>
</figure>'''

# =====================================================================
# HOME
# =====================================================================
jsonld = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService","name":"Topography Consulting LLC","slogan":"Environmental Compliance Solutions",
"url":"https://www.topographyllc.com/","logo":"https://www.topographyllc.com/assets/logo/og-logo.png","email":"marcie@topographyllc.com","telephone":"+1-805-331-0740",
"address":{"@type":"PostalAddress","postOfficeBoxNumber":"20014","addressLocality":"Sedona","addressRegion":"AZ","postalCode":"86341","addressCountry":"US"},
"areaServed":"Worldwide","founder":{"@type":"Person","name":"Marcie M. Merksamer","jobTitle":"Founder"},
"knowsAbout":["Ballast water management","IMO Ballast Water Management Convention","US Coast Guard ballast water regulations","EPA Vessel General Permit","Biofouling management","Hull biofouling","Aquatic invasive species","Marine biosecurity","Maritime environmental compliance"]}
</script>'''

home = head("Topography Consulting | Ballast Water & Biofouling Compliance",
            "Specialized maritime environmental compliance consulting for ballast water management and biofouling management — IMO, USCG and EPA requirements, compliance programs and BWMS approvals.",
            "", extra=jsonld) + header("home") + f'''
<main id="main">
<section class="hero on-dark">
  <div class="hero__media"><img data-parallax="0.12" src="assets/img/hero-wave.jpg" alt="An ocean swell rising at dusk beneath copper-lit clouds" width="2400" height="1600" fetchpriority="high"></div>
  <div class="contours" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <div class="hero-in">
      <p class="label">Environmental Compliance Solutions</p>
      <h1 class="display">Charting a clear course to <em>compliance.</em></h1>
      <div class="hero__row">
        <p class="lede mb-0">Specialized consulting in ballast water and biofouling management, helping the maritime industry meet global biosecurity regulations and control the spread of aquatic invasive species.</p>
        <div class="hero__actions">
          <a class="btn" href="services.html">Explore services {ARROW}</a>
          <a class="btn btn--ghost" href="contact.html">Start a conversation</a>
        </div>
      </div>
      <div class="hero__meta coord">
        <span>IMO &middot; USCG &middot; EPA &middot; Classification societies</span>
        <span class="scroll-cue"><i></i>Scroll</span>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="label reveal">The practice</p>
        <h2 class="h2 reveal">A specialist firm for a <em>specialist</em> problem.</h2>
      </div>
      <p class="lede reveal" style="--d:.1s">Normal shipping operations can move aquatic organisms around the world without anyone noticing. Topography Consulting helps the people who build, operate and regulate ships manage that biosecurity risk with precision.</p>
    </div>
    <div class="readouts">
      <div class="readout reveal"><b>26<sup>YRS</sup></b><span>focused on ballast water management and aquatic invasive species</span></div>
      <div class="readout reveal" style="--d:.08s"><b>24<sup>YRS</sup></b><span>as an independent environmental consultant in the maritime sector</span></div>
      <div class="readout reveal" style="--d:.16s"><b>IMO</b><span>participant at the International Maritime Organization, tracking global biosecurity developments</span></div>
      <div class="readout reveal" style="--d:.24s"><b>Global</b><span>practice, with connections across the regulatory and scientific communities and a worldwide network of service providers</span></div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap grid-2">
    {PEAK_FIG}
    <div>
      <p class="label reveal">Why &ldquo;Topography&rdquo;</p>
      <h2 class="h2 reveal">The lines on a map <em>tell a story.</em></h2>
      <p class="reveal">Contour lines show where the peaks and valleys are, how steep the climb will be, where the water lies and where the coastline offers safe harbor. They also show that there is more than one way to reach a destination: over, under, around or through.</p>
      <p class="reveal">That is how we approach compliance. We learn the terrain of each client&rsquo;s operation, listen for the pinch points, and then lead the way through the regulations, from the summit of policy down to the deck of the ship.</p>
      <blockquote class="pull reveal">&ldquo;No problems; only solutions.&rdquo;<cite>Marcie Merksamer, Founder</cite></blockquote>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="label reveal">Core specializations</p>
        <h2 class="h2 reveal">Two disciplines. <em>One</em> objective.</h2>
      </div>
      <p class="lede reveal" style="--d:.1s">Ballast water and biofouling are the two main ways ships carry aquatic invasive species. They are what we work on, and what we know best.</p>
    </div>
    <div class="panels">
      <a class="panel reveal" href="services.html#ballast-water">
        <img src="assets/img/port-ship.jpg" alt="A loaded container ship berthed beneath gantry cranes" width="1800" height="1200" loading="lazy">
        <span class="coord">01 / Ballast water</span>
        <h3>Ballast Water Management</h3>
        <p>Compliance with the IMO Ballast Water Management Convention, US Coast Guard rules, the EPA Vessel General Permit and national, regional and class requirements.</p>
        <span class="link-arrow">Ballast water services {ARROW}</span>
      </a>
      <a class="panel reveal" style="--d:.12s" href="services.html#biofouling">
        <img src="assets/img/reef.jpg" alt="Divers beside a dense school of fish on a reef wall" width="1600" height="1067" loading="lazy">
        <span class="coord">02 / Biofouling</span>
        <h3>Biofouling Management</h3>
        <p>Practical preparation for the international biofouling management framework now taking shape, with direct involvement in how those regulations are developed.</p>
        <span class="link-arrow">Biofouling services {ARROW}</span>
      </a>
    </div>
  </div>
</section>

<section class="section section--ocean on-dark">
  <div class="contours contours--soft" aria-hidden="true"></div>
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="label reveal">Services</p>
        <h2 class="h2 reveal">From regulation to <em>the ship.</em></h2>
      </div>
      <p class="lede reveal" style="--d:.1s">Every engagement is scoped to the project, so you get the expertise you need without paying for the parts you don&rsquo;t.</p>
    </div>
    <ul class="legend">
      <li class="reveal"><a href="services.html#ballast-water"><span class="n">01</span><h3>Regulatory compliance support</h3><p>Ballast water and biofouling requirements under IMO, USCG, EPA, national and regional bodies, and classification societies.</p><span class="arrow">{ARROW}</span></a></li>
      <li class="reveal"><a href="services.html#programs"><span class="n">02</span><h3>Compliance program development</h3><p>Ballast water management plans, contingency planning, compliance monitoring programs and crew training.</p><span class="arrow">{ARROW}</span></a></li>
      <li class="reveal"><a href="services.html#management"><span class="n">03</span><h3>Program &amp; project management</h3><p>Hands-on management of compliance programs and projects from scoping through to closeout.</p><span class="arrow">{ARROW}</span></a></li>
      <li class="reveal"><a href="services.html#approvals"><span class="n">04</span><h3>BWMS approvals &amp; risk assessment</h3><p>Type approval support, aquatic toxicology, and environmental and human health risk assessment for chemical-based systems.</p><span class="arrow">{ARROW}</span></a></li>
      <li class="reveal"><a href="services.html#intelligence"><span class="n">05</span><h3>Regulatory insight &amp; access</h3><p>A subject matter expert who takes part at the IMO and has a global network across regulators, scientists and industry.</p><span class="arrow">{ARROW}</span></a></li>
    </ul>
  </div>
</section>

<section class="band on-dark">
  <img data-parallax="0.1" src="assets/img/cliffs-mist.jpg" alt="Green sea cliffs falling to the coast as morning mist lifts off the ridgeline" width="2000" height="1333" loading="lazy">
  <div class="wrap">
    <blockquote class="reveal">From the mountains to the sea, and every environment in between.</blockquote>
    <span class="coord reveal">Protect &middot; Explore &middot; Preserve</span>
  </div>
</section>

<section class="section section--dark on-dark">
  <div class="contours" aria-hidden="true"></div>
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="label reveal">Range of experience</p>
        <h2 class="h2 reveal">From the boiler suit to the <em>business suit.</em></h2>
      </div>
      <p class="lede reveal" style="--d:.1s">We have done the work at every level, so our advice holds up on deck, in the lab and in front of the regulator.</p>
    </div>
    <div class="range">
      <div class="range__line"></div>
      <div class="range__stops">
        <div class="reveal"><span class="coord">Onboard</span><b>Service technician</b><span>Logistics of scientific BWMS testing on working ships, including system operation, maintenance and crew interaction.</span></div>
        <div class="reveal" style="--d:.1s"><span class="coord">Laboratory</span><b>Environmental scientist</b><span>Aquatic toxicology and risk assessment of chemical disinfection by-products.</span></div>
        <div class="reveal" style="--d:.2s"><span class="coord">Approvals</span><b>Regulatory specialist</b><span>Dossiers, data analysis and agency interactions for system approvals worldwide.</span></div>
        <div class="reveal" style="--d:.3s"><span class="coord">Policy</span><b>Global expert</b><span>Represents industry on the delegation to the International Maritime Organization.</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="label reveal">Who we serve</p>
        <h2 class="h2 reveal">Bringing every <em>stakeholder</em> to the same chart.</h2>
      </div>
      <p class="lede reveal" style="--d:.1s">Compliance works best when everyone involved, including technology developers, regulators and the people who sail the ships, works from the same information.</p>
    </div>
    <div class="audience">
      <div class="reveal"><h3>Shipowners &amp; operators</h3><p>Clear, cost-effective paths to meeting ballast water and biofouling obligations across every port of call.</p></div>
      <div class="reveal" style="--d:.06s"><h3>Technology developers</h3><p>Expert support through type approval, testing and the scientific questions regulators ask.</p></div>
      <div class="reveal" style="--d:.12s"><h3>Equipment manufacturers</h3><p>Regulatory insight that shapes product strategy, documentation and market entry.</p></div>
      <div class="reveal"><h3>Maritime service providers</h3><p>Alignment with current requirements, and early warning of the requirements that are coming.</p></div>
      <div class="reveal" style="--d:.06s"><h3>Regulatory bodies</h3><p>Technical expertise and industry perspective for the development of practical, science-based rules.</p></div>
      <div class="reveal" style="--d:.12s"><h3>Industry associations</h3><p>Including the Biosecurity &amp; Environmental Marine Association (BEMA), a client of Topography Consulting.</p></div>
    </div>
  </div>
</section>
''' + cta() + "</main>\n" + FOOTER

# =====================================================================
# SERVICES
# =====================================================================
services = head("Services | Ballast Water & Biofouling Compliance Consulting",
                "Ballast water management compliance (IMO BWM Convention, USCG, EPA VGP), biofouling management, compliance program development, BWMS approvals and marine biosecurity expertise.",
                "services.html", image="assets/img/ocean-surface.jpg") + header("services") + f'''
<main id="main">
<section class="hero page-hero on-dark">
  <div class="hero__media"><img data-parallax="0.12" src="assets/img/ocean-surface.jpg" alt="The surface of the open ocean in soft evening light" width="2000" height="1333" fetchpriority="high"></div>
  <div class="contours" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <div class="hero-in">
      <p class="label">Services</p>
      <h1 class="display">Maritime environmental compliance, <em>mapped.</em></h1>
      <p class="lede">Everything we do supports one goal: helping our clients achieve and maintain compliance with global ballast water and biofouling management regulations.</p>
      <div class="hero__meta coord"><span>Scoped per project &middot; Hourly consulting</span><span class="scroll-cue"><i></i>Scroll</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">

    <article class="service" id="ballast-water">
      <div class="service__aside reveal">
        <span class="n">01 / Core specialization</span>
        <h2>Ballast Water Management</h2>
        <p class="coord">IMO BWM Convention &middot; USCG &middot; EPA VGP</p>
      </div>
      <div class="service__body">
        <figure class="service__img reveal"><img src="assets/img/port-ship.jpg" alt="Container ship alongside at a working port" width="1800" height="1200" loading="lazy"></figure>
        <p class="lede reveal">Support for compliance with ballast water requirements under the International Maritime Organization, the US Coast Guard, the US Environmental Protection Agency, national and regional authorities and ship classification societies.</p>
        <ul class="checklist checklist--2 reveal">
          <li>IMO International Convention for the Control and Management of Ships&rsquo; Ballast Water and Sediments</li>
          <li>US Coast Guard ballast water regulations</li>
          <li>EPA Vessel General Permit (VGP)</li>
          <li>National and regional requirements</li>
          <li>Classification society requirements</li>
          <li>Interpretation across trade routes and flag states</li>
        </ul>
        <div class="when reveal"><p class="label">When clients call</p><p>When you need a clear reading of which requirements apply to your vessels and trade, and a realistic plan for meeting them.</p></div>
      </div>
    </article>

    <article class="service" id="biofouling">
      <div class="service__aside reveal">
        <span class="n">02 / Core specialization</span>
        <h2>Biofouling Management</h2>
        <p class="coord">Hull &amp; niche-area biosecurity</p>
      </div>
      <div class="service__body">
        <figure class="service__img reveal"><img src="assets/img/reef.jpg" alt="Marine life gathered along an underwater reef wall" width="1600" height="1067" loading="lazy"></figure>
        <p class="lede reveal">Biofouling on ship hulls is the other major way aquatic invasive species travel. We apply more than two decades of ballast water experience to the international biofouling management regulations, which we are helping to develop.</p>
        <ul class="checklist reveal">
          <li>Guidance on emerging international biofouling management requirements</li>
          <li>Biofouling management planning and program development</li>
          <li>Connection to technology, service providers and the scientific community</li>
        </ul>
        <div class="when reveal"><p class="label">When clients call</p><p>When you want to get ahead of biofouling requirements and build management practices that are practical, defensible and ready for what comes next.</p></div>
      </div>
    </article>

    <article class="service" id="programs">
      <div class="service__aside reveal">
        <span class="n">03</span>
        <h2>Compliance Program Development</h2>
        <p class="coord">Plans &middot; Contingency &middot; Monitoring &middot; Training</p>
      </div>
      <div class="service__body">
        <p class="lede reveal">Environmental compliance programs for ships, built to work in the real conditions on board.</p>
        <ul class="checklist checklist--2 reveal">
          <li>Ballast water management plans</li>
          <li>Contingency planning</li>
          <li>Compliance monitoring programs</li>
          <li>Crew training programs</li>
        </ul>
      </div>
    </article>

    <article class="service" id="management">
      <div class="service__aside reveal">
        <span class="n">04</span>
        <h2>Program &amp; Project Management</h2>
        <p class="coord">Scope &middot; Coordinate &middot; Deliver</p>
      </div>
      <div class="service__body">
        <p class="lede reveal">Compliance programs and projects managed with honesty and integrity, so your goals are met as efficiently and cost-effectively as possible.</p>
        <p class="reveal">We coordinate among owners, technology suppliers, service providers and regulators so that each part of the work reaches the right party at the right time.</p>
      </div>
    </article>

    <article class="service" id="approvals">
      <div class="service__aside reveal">
        <span class="n">05</span>
        <h2>BWMS Approvals &amp; Risk Assessment</h2>
        <p class="coord">Toxicology &middot; Dossiers &middot; Data</p>
      </div>
      <div class="service__body">
        <p class="lede reveal">In-depth knowledge of chemical-based ballast water management systems, and of the chemistry, aquatic toxicology and human health questions that come with them.</p>
        <ul class="checklist checklist--2 reveal">
          <li>Approval support through classification societies and international administrations</li>
          <li>Aquatic toxicology research for chemical-based systems</li>
          <li>Environmental &amp; human health risk assessment of disinfection by-products</li>
          <li>Dossier preparation and data analysis</li>
          <li>Regulatory agency interactions</li>
          <li>Onboard testing logistics</li>
        </ul>
      </div>
    </article>

    <article class="service" id="intelligence">
      <div class="service__aside reveal">
        <span class="n">06</span>
        <h2>Regulatory Insight &amp; Access</h2>
        <p class="coord">IMO &middot; Global network</p>
      </div>
      <div class="service__body">
        <p class="lede reveal">Direct access to a subject matter expert who takes part at the International Maritime Organization and follows global biosecurity regulation as it develops.</p>
        <p class="reveal">Clients also benefit from long-standing connections across the regulatory and scientific communities and from a global network of service providers.</p>
      </div>
    </article>

  </div>
</section>

<section class="section section--ocean on-dark" id="approach">
  <div class="contours contours--soft" aria-hidden="true"></div>
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="label reveal">Approach</p>
        <h2 class="h2 reveal">Over, under, around <em>or through.</em></h2>
      </div>
      <p class="lede reveal" style="--d:.1s">There is always more than one route to the destination. Our work is finding the one that fits your vessel, your budget and your schedule.</p>
    </div>
    <div class="steps">
      <div class="step reveal"><span class="coord">Waypoint 01</span><h3>Explore</h3><p>Learn the terrain: your fleet, your systems, your trade and the regulations that apply.</p></div>
      <div class="step reveal" style="--d:.1s"><span class="coord">Waypoint 02</span><h3>Listen</h3><p>Understand the pinch points, challenges and constraints that matter most to you.</p></div>
      <div class="step reveal" style="--d:.2s"><span class="coord">Waypoint 03</span><h3>Chart</h3><p>Plot the most efficient, cost-effective route to compliance.</p></div>
      <div class="step reveal" style="--d:.3s"><span class="coord">Waypoint 04</span><h3>Guide</h3><p>Lead the way there, and stay alongside as the rules continue to change.</p></div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="grid-2">
      <div>
        <p class="label reveal">Engagement</p>
        <h2 class="h2 reveal">Scoped to the <em>project.</em></h2>
        <p class="reveal">There are no fixed packages. Each engagement is scoped to your needs and billed at an hourly consulting rate, so you pay only for the expertise the work requires.</p>
        <p class="reveal mb-0"><a class="link-arrow" href="contact.html">Discuss a project {ARROW}</a></p>
      </div>
      <div class="note-card reveal">
        <h3 class="h3">Onboard sampling &amp; testing</h3>
        <p>For hands-on compliance sampling and testing aboard ships, we refer clients to our trusted collaborator <strong>EnviroManagement, Inc.</strong>, an environmental services and consulting company co-founded by Marcie Merksamer in 2002.</p>
      </div>
    </div>
  </div>
</section>
''' + cta() + "</main>\n" + FOOTER

# =====================================================================
# ABOUT
# =====================================================================
about = head("About Marcie Merksamer | Topography Consulting",
             "Marcie M. Merksamer: 26 years in aquatic invasive species and ballast water management, Secretary-General of BEMA, IMO delegate and founder of Topography Consulting LLC.",
             "about.html", image="assets/img/peaks-clouds.jpg") + header("about") + f'''
<main id="main">
<section class="hero page-hero on-dark">
  <div class="hero__media"><img data-parallax="0.12" src="assets/img/peaks-clouds.jpg" alt="Mountain peaks rising above a sea of clouds at first light" width="2400" height="1600" fetchpriority="high"></div>
  <div class="contours" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <div class="hero-in">
      <p class="label">About</p>
      <h1 class="display">Driven by a passion for <em>the Earth.</em></h1>
      <p class="lede">Topography Consulting was founded to protect what we explore, and to preserve it for the generations who will explore it next.</p>
      <div class="hero__meta coord"><span>Founded by Marcie M. Merksamer</span><span class="scroll-cue"><i></i>Scroll</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap grid-2 grid-2--wide-right">
    <!-- Replace with Marcie's headshot when supplied: assets/img/marcie.jpg (4:5 crop recommended) -->
    <figure class="portrait reveal">
      <img src="assets/img/forest-lake.jpg" alt="A still alpine lake framed by evergreen forest" width="1600" height="1067" loading="lazy">
      <figcaption><span class="coord" style="color:var(--sage)">Founder</span><span class="coord" style="color:var(--sage)">Sedona, AZ</span></figcaption>
    </figure>
    <div>
      <p class="label reveal">Founder</p>
      <h2 class="h2 reveal">Marcie M. <em>Merksamer</em></h2>
      <div class="prose reveal">
        <p>Trained as an environmental biologist, Marcie has worked on aquatic invasive species and ballast water management for 26 years, 24 of them as an independent environmental consultant in the maritime sector.</p>
        <p>Much of her ballast water work has involved helping clients obtain approvals for ballast water management systems (BWMS) through classification societies and international administrations. In managing those approvals she has carried out extensive research on aquatic toxicology for chemical-based systems, performed environmental and human health risk assessments of chemical disinfection by-products, and handled complex agency interactions, dossier preparation and data analysis.</p>
        <p>She knows the logistics of scientific BWMS testing on board ships, as well as system operation, maintenance, crew interaction and crew training. Marcie now applies that expertise to current developments in the biofouling management sector. A primary goal in her work is to build productive working relationships among scientists, technology developers, industry and regulators.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap grid-2">
    <div>
      <p class="label reveal">Credentials</p>
      <h2 class="h2 reveal">A record built <em>over decades.</em></h2>
      <p class="reveal muted">Experience that spans technical, regulatory and industry-association work, at home and at the IMO.</p>
    </div>
    <ul class="credentials">
      <li class="reveal"><span class="k">Current</span><span class="v"><b>Owner &amp; Founder</b><span>Topography Consulting LLC</span></span></li>
      <li class="reveal"><span class="k">Since 2018</span><span class="v"><b>Secretary-General &amp; Co-founder</b><span>Biosecurity &amp; Environmental Marine Association (BEMA), a non-profit, technically based association with Consultative Status at the IMO. Marcie represents BEMA on the delegation to the IMO.</span></span></li>
      <li class="reveal"><span class="k">2002 &ndash; present</span><span class="v"><b>Co-founder &amp; former Vice President</b><span>EnviroManagement, Inc., an environmental services and consulting company</span></span></li>
      <li class="reveal"><span class="k">Education</span><span class="v"><b>B.S., Biological Sciences</b><span>Concentration in Environmental Science, California Polytechnic State University, San Luis Obispo</span></span></li>
    </ul>
  </div>
</section>

<section class="band on-dark">
  <img data-parallax="0.1" src="assets/img/coast-aerial.jpg" alt="Aerial view of surf meeting a pale sand shoreline" width="1400" height="2100" loading="lazy">
  <div class="wrap">
    <blockquote class="reveal">The ocean&rsquo;s surface has a topography too, in every swell and ripple.</blockquote>
    <span class="coord reveal">Land &middot; Sea &middot; Everything between</span>
  </div>
</section>

<section class="section">
  <div class="wrap grid-2 grid-2--wide-left">
    <div>
      <p class="label reveal">The name</p>
      <h2 class="h2 reveal">It&rsquo;s all about <em>exploration.</em></h2>
      <div class="reveal">
        <p>Nature, planet Earth, exploration and adventure. From the mountains to the sea and every environment in between, this planet is endlessly fascinating, and worth protecting, exploring and preserving for future generations.</p>
        <p>Marcie still plans her explorations on old-school paper maps and charts, on land and at sea. Their lines show where the peaks and valleys lie, how hard the climb will be, where the coastline offers safe harbor and how deep the trenches run. They also show that there is always more than one way to reach a destination.</p>
        <p>Many people think of topography only on land, but the ocean&rsquo;s surface has one too: the peaks and valleys of waves and the ripples drawn by wind and current. The name is a reminder that the journey continues, wherever it leads.</p>
      </div>
    </div>
    <div>
      <blockquote class="pull reveal">&ldquo;We&rsquo;ve done everything from the boiler suit to the business suit.&rdquo;<cite>Marcie Merksamer</cite></blockquote>
      <blockquote class="pull reveal">&ldquo;No problems; only solutions.&rdquo;<cite>A guiding principle</cite></blockquote>
    </div>
  </div>
</section>
''' + cta(title='Let&rsquo;s chart the <em>path</em> together.') + "</main>\n" + FOOTER

# =====================================================================
# CONTACT
# =====================================================================
contact = head("Contact | Topography Consulting LLC",
               "Contact Topography Consulting LLC about ballast water management, biofouling management and maritime environmental compliance. Based in Sedona, Arizona and serving clients worldwide.",
               "contact.html", image="assets/img/open-ocean.jpg") + header("contact") + f'''
<main id="main">
<section class="hero page-hero on-dark">
  <div class="hero__media"><img data-parallax="0.12" src="assets/img/open-ocean.jpg" alt="Calm open ocean meeting a pale horizon" width="2000" height="1333" fetchpriority="high"></div>
  <div class="contours" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <div class="hero-in">
      <p class="label">Contact</p>
      <h1 class="display">Every route starts with a <em>conversation.</em></h1>
      <p class="lede">Tell us about your vessel, your system or the regulation you&rsquo;re facing, and we&rsquo;ll help you find the way forward.</p>
      <div class="hero__meta coord"><span>34.8697&deg; N &middot; 111.7610&deg; W</span><span>Serving clients worldwide</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap contact-grid">
    <div>
      <p class="label reveal">Direct</p>
      <ul class="contact-list reveal">
        <li><span class="k">Email</span><a href="mailto:marcie@topographyllc.com">marcie@topographyllc.com</a></li>
        <li><span class="k">Phone</span><a href="tel:+18053310740">+1 805-331-0740</a></li>
        <li><span class="k">Mailing address</span><address>P.O. Box 20014<br>Sedona, AZ 86341<br>United States</address></li>
      </ul>
    </div>
    <div>
      <p class="label reveal">Send a message</p>
      <form class="form reveal" data-mailto-form novalidate>
        <div class="two">
          <div class="field"><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
        </div>
        <div class="two">
          <div class="field"><label for="org">Organization</label><input id="org" name="org" autocomplete="organization"></div>
          <div class="field"><label for="sector">You are a&hellip;</label>
            <select id="sector" name="sector">
              <option>Shipowner / operator</option>
              <option>Technology developer</option>
              <option>Equipment manufacturer</option>
              <option>Maritime service provider</option>
              <option>Regulatory body</option>
              <option>Other</option>
            </select>
          </div>
        </div>
        <div class="field"><label for="topic">Topic</label>
          <select id="topic" name="topic">
            <option>Ballast water management</option>
            <option>Biofouling management</option>
            <option>Compliance program development</option>
            <option>BWMS approvals &amp; risk assessment</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="field"><label for="message">How can we help?</label><textarea id="message" name="message" required></textarea></div>
        <div><button class="btn" type="submit">Compose email {ARROW}</button></div>
        <small>This opens a pre-filled message in your email app. Nothing is stored on this site.</small>
      </form>
    </div>
  </div>
</section>
</main>
''' + FOOTER

for name, html in [("index.html", home), ("services.html", services), ("about.html", about), ("contact.html", contact)]:
    open(os.path.join(SITE, name), "w", encoding="utf-8").write(html)
    print(name, len(html)//1024, "KB")

open(os.path.join(SITE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {URL}/sitemap.xml\n")
open(os.path.join(SITE, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{URL}/{p}</loc></url>\n" for p in ["", "services.html", "about.html", "contact.html"]) + "</urlset>\n")
