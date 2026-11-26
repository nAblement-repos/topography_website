# Topography Consulting LLC: client approval checklist

Internal working list for Nablement. It lives outside `site/` and is never deployed.
Items marked **Blocks launch** must be settled before the site goes live on the real domain.

## Blocks launch

| # | Item | Current state | Needed from Marcie |
| --- | --- | --- | --- |
| 1 | Final website design | Redesign ready for review on a local or staging URL | Approval, or change requests |
| 2 | Condensed copy | All visible copy shortened by about 45%. Wording drawn from the questionnaire and bio | Read every page and approve or correct |
| 3 | Headshot | Using a 550 × 366 px crop from the bio document; soft on modern screens | A high-resolution original (at least 1200 px on the short side), plus approval of the crop |
| 4 | Photography and usage rights | 9 stock photos came with the draft; their source and licence are unknown. No ship-hull or onboard photo | Confirm the licences or supply or approve replacements. Her own Sedona and Arizona photos are welcome on About |
| 5 | Domain ownership and DNS provider | `topographyllc.com` is assumed; registrar and DNS host unknown | Registrar and DNS login (or a contact), and who manages the email records |
| 6 | Preferred address | Recommend `www.topographyllc.com`, with the bare domain redirecting to it | Choose `www` or the bare domain |
| 7 | Hosting arrangement | `vercel.json` prepared; no account created, nothing deployed | Approve the host and who pays for it (commercial use needs a paid Vercel plan; Netlify's free tier also works) |
| 8 | Contact form or direct email | Form validates, then opens the visitor's email app (clearly labelled). No form service connected | Choose: keep the email hand-off, or approve a form service such as Formspree (free tier, or about $10 per month) |
| 9 | Mailing address | Questionnaire says "P.O. Box 20014, Sedona, **AS** 86341". "AS" is the code for American Samoa, so presumably AZ. The address is **not published** right now; the site shows "Sedona, Arizona" | Confirm the full mailing address and ZIP code, and whether it should appear on the site at all |
| 10 | EnviroManagement wording | "For onboard compliance sampling and testing, we refer clients to EnviroManagement, Inc., the environmental services company Marcie co-founded in 2002." Not described as a partner | Approve the wording, or supply a preferred term |

## Should be settled before launch (not blocking)

| # | Item | Current state | Needed from Marcie |
| --- | --- | --- | --- |
| 11 | BEMA references | About timeline (co-founder, Secretary-General, IMO delegation) and "Industry associations, including BEMA" on Services. No BEMA logo used | Approve; confirm whether the BEMA logo should appear (needs BEMA's permission) |
| 12 | Privacy policy | None, and no privacy link in the footer. The site sets no cookies and has no analytics | Decide whether one is wanted, especially if a form service or analytics is added later |
| 13 | Horizontal header logo | Header uses the approved emblem and wordmark vectors side by side (a new arrangement, same artwork) | Approve the horizontal lockup, or ask for the stacked logo |
| 14 | "Boiler suit to business suit" quote | Used as a pull quote on the homepage, quoted as she wrote it | Confirm she is comfortable with it (she called it "kinda corny") |
| 15 | EPA Vessel General Permit wording | Listed as a framework she works with; no claim about its current status | Confirm the wording is current |
| 16 | Maintenance responsibility | Not agreed | Who updates content, renews the domain and hosting, and monitors the form inbox |

## Optional improvements

- A 1200 × 630 social sharing image (currently the logo PNG).
- The short "how I got into aquatic invasive species" story she offered, as a short section on About.
- Her own photos of Sedona and Arizona for the About story section.
- Google Search Console setup after launch (needs one added DNS TXT record).
- Privacy-friendly analytics (for example Plausible or Fathom, paid) if she wants traffic numbers.
