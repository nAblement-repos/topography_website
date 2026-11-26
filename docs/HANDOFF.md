# Topography Consulting LLC website: developer handoff

Internal document. It lives outside `site/` and is never deployed.
Last updated: 25 November 2026 (redesign pass on top of commit `6e00400 preliminary_draft`).

## 1. Architecture (unchanged in principle)

A static site. No framework, no runtime dependencies, no third-party scripts.

| Path | What it is |
| --- | --- |
| `site/` | **The publish directory.** Everything in it is public once deployed. |
| `site/*.html` | Generated pages. Do not hand-edit; edit `tools/build.py` and rebuild. |
| `site/assets/css/styles.css` | The whole design system (tokens at the top). |
| `site/assets/js/main.js` | All interactions, about 400 lines, no dependencies. |
| `site/assets/fonts/` | Self-hosted Cormorant Garamond + Manrope (SIL Open Font License), latin subset. |
| `site/assets/img/*.jpg` | Source photos (also the `<picture>` fallback). |
| `site/assets/img/opt/` | Responsive WebP derivatives (640 / 1200 / 2000 px). |
| `site/assets/img/contours-*.svg` | Generated topographic line art. |
| `site/assets/logo/` | Approved logo SVGs, plus the generated horizontal header lockup. |
| `tools/build.py` | Assembles the four pages from shared header, footer and sections. |
| `tools/contours.py` | Generates the contour SVGs (needs `numpy`). |
| `tools/optimize-images.mjs` | Generates WebP derivatives and crops (needs `sharp`). |
| `content/` | Client source material. **Not public, but tracked in Git** (see section 9). |
| `vercel.json` | Static hosting config: publishes `site/`, no build step, security and cache headers. |

### Rebuilding

```bash
python3 tools/build.py site                     # staging build (default; noindex)
SITE_ENV=production SITE_URL=https://www.topographyllc.com python3 tools/build.py site
FORM_ENDPOINT=https://formspree.io/f/XXXXXXX python3 tools/build.py site   # once a form service is approved

# only when changing artwork or photos:
pip install numpy && python3 tools/contours.py site/assets/img
npm i --no-save sharp@0.33.5 && node tools/optimize-images.mjs
```

`build.py` uses only the Python standard library.

## 2. Local preview

```bash
cd site && python3 -m http.server 8000      # then open http://localhost:8000
```

Use a local server, not a double-click on the HTML file. Over `file://` Chrome blocks
self-hosted web fonts (a CORS rule), so the pages fall back to Georgia and the system
sans-serif. Everything else, contour art included, works over `file://`.

## 3. What changed

**Design system**: rebuilt `styles.css` around tokens. Colors come from the approved logo
files (forest `#215A39`, navy `#094368`, wordmark `#0A3F68`), with deep navy `#0E2836`, warm
ivory `#F7F6F0`, sand `#EEECE3`, sage `#B7C8BD` and copper `#D58B55`. Copper is used only
for the animated route, link dots, focus rings on dark surfaces and a few hairlines. Type is
Cormorant Garamond for display and Manrope for everything else, with `clamp()` sizes: hero
48 to 104 px, section headings 36 to 60 px, subheadings 24 to 32 px, body 16 to 18 px,
nav and footer 15 px, labels 12 to 13 px. The mono font, uppercase micro-labels,
coordinates, numbered labels, the depth gauge and the continuously drifting backgrounds
are gone.

**Content**: about 45% less visible copy. Removed: the readout cards, "Why Topography" on
the homepage, the image band slogans, the "range of experience" strip, the waypoint
"Approach" section and the repeated stakeholder descriptions. Navigation metaphors now
appear in two places only (hero heading and intro heading), plus the founder's own words on
About.

**Homepage**: an asymmetric hero (heading left, animated logo right) over a darkened ocean
photo. Then a short introduction with three inline credibility facts, interactive service
rows with a swapping image, the founder section with portrait and pull quote, and a forest
green closing CTA.

**Services**: split hero with the port photo, a one-line regulatory frameworks list, and
four accessible accordion items (ballast water, biofouling, compliance programs and project
management, system approvals and risk assessment). Then "Who we work with", engagement
terms, a clear statement that onboard sampling and testing is referred to
EnviroManagement, Inc., and a CTA.

**About**: three sections (professional background, the story behind the name with the
mountain photo, experience and qualifications timeline). All facts come from the client
questionnaire and bio. No awards, clients or statistics were added.

**Contact**: heading, clickable email and phone, "Sedona, Arizona / Serving clients
globally", and a five-field form (see section 6). The P.O. Box is no longer published (see
the checklist).

**Footer**: one consistent type system (Manrope 15 px), white knockout logo, tagline,
page links, contact, copyright, and a contour ridge along the bottom edge. No privacy link,
because no policy exists yet.

### Signature logo animation (home hero)

- Uses the approved `Topography-Logo-White-Knockout.svg` paths. `build.py` splits the
  emblem's 20 sub-paths into five groups (waves, mountains, summit contours, compass, ring
  and letters). Holes stay with the shapes they cut, so even-odd fill renders identically.
  The script asserts every sub-path is used exactly once.
- Sequence, 1.9 s, Web Animations API, no library:
  1. Each contour's outline draws on (`pathLength` plus `stroke-dashoffset`), from the sea
     up to the north point.
  2. Two clipped copies of the emblem part about 16 units either side of the north line,
     and a copper route traces up through the opening.
  3. The halves close, fills arrive, the strokes and the route fade, and the wordmark
     settles in.
  4. The first ring contours open around the emblem. While the visitor scrolls through
     the hero, a growing `clip-path` circle extends those rings into a full topographic
     field (`contours-rings.svg` has no lines inside the emblem's radius).
- When the sequence ends, the temporary copies are removed and the untouched original
  vector is shown. **Verified pixel-identical** to the approved SVG (0 differing pixels at
  728 × 635).
- The heading and CTA are never delayed. The emblem is hidden at most 2.5 s by a CSS
  failsafe in case the script fails.
- `prefers-reduced-motion`: no drawing, no ring growth; the static logo and static rings
  show. Without JavaScript: the static logo shows and the ring field is hidden.
- Under 900 px wide, the hero shows the approved emblem-only crop (same vectors, icon
  viewBox), because the header already shows the full name.
- The header logo is static: a horizontal lockup generated from the approved emblem and
  wordmark vectors (`Topography-Lockup-Horizontal-*.svg`). **This arrangement needs client
  approval.**

## 4. Functional now

Navigation (desktop and mobile; Escape closes, focus moves into the menu and back, the
page behind is `inert`). Logo animation and scroll stage. Scroll reveals. Accordion (click,
keyboard, deep links such as `services.html#biofouling`, content open without JS).
Clickable email and phone. Contact form validation. Staging and production SEO switch.

## 5. Needs configuration before launch

1. **Production build**: `SITE_ENV=production SITE_URL=<confirmed hostname>`. This adds
   canonical and `og:url`, absolute `og:image`, an indexable `robots.txt` and `sitemap.xml`.
   The committed files are a staging build (`noindex`, `Disallow: /`, no sitemap).
2. **Contact form service** (section 6). Until then the form opens the visitor's email app
   and says so.
3. **Photography and headshot** (client checklist).

## 6. Contact form

- **Now (`FORM_ENDPOINT` empty):** submit validates the fields, then opens a pre-filled
  email to marcie@topographyllc.com in the visitor's mail app. The button reads "Continue in
  your email app", and a note under it says exactly that. Nothing is sent by the website and
  nothing is stored. Without JS the form is hidden and a direct email and phone fallback is
  shown.
- **When a service is approved:** rebuild with `FORM_ENDPOINT=<url>`. The form then POSTs
  `FormData` with `Accept: application/json` and shows a loading state ("Sending…"),
  success and error messages (the error message includes the direct email). A honeypot
  field (`_gotcha`, Formspree's convention) is included. Formspree also offers reCAPTCHA
  or hCaptcha in its dashboard if spam becomes a problem.
- Test before launch: a real submission reaches Marcie's inbox, the success message shows,
  an error shows when offline, and the spam filtering works.
- Fields: full name, company (optional), email, area of interest, message. Nothing else
  is collected.

## 7. Hosting and domain

`site/` is the publish directory as-is. There is no build step on the host; the HTML is
committed.

### Staging (Vercel, matching other Nablement projects)

1. Import the GitHub repo in Vercel. `vercel.json` sets output `site`, no build, no
   install, `cleanUrls: false` (so `about.html` links don't redirect).
2. The preview URL (`*.vercel.app`) is the staging site. The committed staging build
   already sends `noindex` and `Disallow: /`. Vercel also adds `X-Robots-Tag: noindex` on
   preview deployments.
3. Optionally turn on Vercel Deployment Protection (password) for previews.

**Netlify alternative:** publish directory `site`, build command empty. Put the headers
from `vercel.json` in a `netlify.toml` `[[headers]]` block.

### Production domain (only after ownership and DNS provider are confirmed)

1. Rebuild with `SITE_ENV=production SITE_URL=https://<chosen hostname>` and commit.
2. In the host's dashboard, add both `topographyllc.com` and `www.topographyllc.com`, and
   set one as primary. **Recommendation: `www` primary, apex redirects to it (308).**
   The hostname must match `SITE_URL`.
3. At the **existing** DNS provider, add only the records the host shows. For Vercel these
   have typically been `A @ 76.76.21.21` and `CNAME www cname.vercel-dns.com`; use the
   exact values shown in the dashboard at the time.
   - **Do not move nameservers to the host and do not delete or edit existing records.**
     Marcie's email runs on this domain: keep every `MX`, `TXT` (SPF, domain
     verification), DKIM (`CNAME`/`TXT` under `_domainkey`), DMARC (`_dmarc`) and any
     autodiscover or SRV records exactly as they are.
   - If an old `A`/`CNAME` for `@` or `www` points at a parking page, replace only that
     record.
   - Screenshot the full DNS zone before touching anything.
4. HTTPS: the host provisions the certificate automatically once DNS resolves (minutes to
   a few hours).
5. Verify:
   - both hostnames load over HTTPS and the non-primary one redirects;
   - `/robots.txt` allows crawling and `/sitemap.xml` lists the four pages on the right
     host;
   - view the source: canonical URLs use the final host and there is no `noindex`;
   - email to and from marcie@topographyllc.com still works (send a test both ways after
     the DNS change);
   - submit the sitemap in Google Search Console (needs a DNS TXT verification record:
     add it, don't replace anything).

### Recurring costs to confirm (check current pricing before committing)

- **Vercel**: the free Hobby plan is for non-commercial use. A business site should be on
  Pro (historically about $20 per member per month). Netlify's free tier permits
  commercial sites.
- **Formspree** (if chosen): has a free tier with a monthly submission cap; paid plans
  start at roughly $10 per month.
- **Domain renewal**: already owned by the client (registrar to be confirmed).
- **Stock photography**, if purchased.

## 8. Testing performed (25 November 2026)

Chrome 158 (headless, through Playwright), local server.

- Automated checks of all four pages at 375, 390, 768, 1024, 1280, 1440 and 1920 px:
  0 px horizontal overflow, no off-screen content, no text under 12 px and no console
  errors at any width. Full-page screenshots were reviewed visually at 375, 768 and
  1440 px, and the homepage hero at 1024 and 1920 px.
- Console and network: no errors or failed requests on any page.
- Logo: mid-animation and final frames captured. After the animation, the DOM is restored
  (no leftover clip paths or strokes) and the result is pixel-identical to the approved
  SVG.
- Accordion: deep link opens the right item; click and Enter toggle it; closed panels are
  `visibility: hidden` (not focusable).
- Mobile menu: opens, moves focus to the first link, makes the page `inert`, Escape closes
  and returns focus.
- Form: empty submit flags name, email and message, focuses the first field and announces
  a status message; a valid submit triggers the email hand-off and its status message.
  `endpoint` mode is **not tested** because no endpoint exists.
- JavaScript disabled: all content visible, accordion panels open, static logo, form
  replaced by the direct-contact note.
- Reduced motion: static logo, no reveals.
- HTML: all four pages pass `html-validate` (recommended rules, minus stylistic ones).
  No broken internal links, anchors or asset references.
- Lighthouse 12.2 (simulated throttling):

| Page | Mobile perf | Desktop perf | A11y | Best practices | SEO (production build) |
| --- | --- | --- | --- | --- | --- |
| Home | 88 | 99 | 100 | 100 | 100 |
| Services | 95 | 100 | 100 | 100 | 100 |
| About | 98 | 100 | 100 | 100 | 100 |
| Contact | 99 | 100 | 100 | 100 | 100 |

  Mobile numbers were measured with gzip but with an extra local `.html` → clean-URL
  redirect (about 750 ms) that `vercel.json` avoids. Staging builds score SEO 66 by
  design (`noindex`).

**Not tested:** Safari, Firefox, Edge, real iOS and Android devices, screen readers
(VoiceOver, NVDA), the form endpoint, and the deployed host's headers. Test these on the
staging URL before launch.

## 9. Security and confidential material

- No credentials, API keys or external scripts anywhere. Fonts are self-hosted, so there
  are no third-party requests at all.
- `content/` (client questionnaire with the mailing address, the bio .docx with the
  original headshot, the logo zip) is **not deployed**, because only `site/` is published.
  It **is tracked in Git** in this private repo, though. Recommended:
  1. Move these files to the shared Nablement drive and add `content/` to `.gitignore`
     going forward.
  2. They also remain in Git history (commit `6e00400`). If the repo could ever become
     public or be shared outside Nablement, purge them with `git filter-repo` and
     force-push. That rewrites history, so get approval and coordinate with anyone who
     has cloned the repo. Not done here.

## 10. Known limitations and open items

- Headshot is a 550 × 366 px crop from the bio document: soft on high-density screens.
- The nine stock photos came with the preliminary draft; their source and licence are
  undocumented. Biofouling uses a crop of `reef.jpg` without the divers; there is no
  ship-hull or onboard-operations photo yet.
- Unused in the current design but still in `site/`: `hero-wave`, `cliffs-mist`,
  `forest-lake`, the full `reef.jpg` (and their WebP files), and `contours-peak.svg`.
  Remove them before launch if they aren't chosen, to keep the deploy lean.
- "EPA Vessel General Permit" is listed because the client names it as a core regulation.
  No statement is made about its current status or its transition under the Vessel
  Incidental Discharge Act. Marcie should confirm the wording.
- `og:image` is the logo PNG; a 1200 × 630 social card would look better.
- CSS and JS are not minified: 31 KB and 15 KB uncompressed, small enough to leave.
