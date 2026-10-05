# maletherapistinportland.com: temporary site

This is a static HTML and Bootstrap 5.3.8 site. It stands in until the Astro/Sanity build is ready. It has no build step: every file here is what gets served.

**Domains:** `maletherapistinportland.com` is the main one. `jscar.care` (printed on the zines) and `therapyformenportland.com` redirect to it with permanent 301 redirects. Email stays `hi@jscar.care`, since email and websites are set up separately.

## Deploy (Cloudflare Pages)

Hosted on Cloudflare Pages from a **private** GitHub repo. Framework preset: none. Build command: none. Output directory: `/`. Full steps are in the launch guide, kept outside this repo.

- `_redirects`: real 301s for the old mmm.page paths (`/about`, `/main` → `/`; `/approach` → `/help/`; `/dudes` → `/help/#mens-issues`; `/blocks` → `/help/#creative-blocks`; `/business` → `/fees/`), with and without a trailing slash. `/zine/` exists, so printed zines resolve through the jscar.care redirect.
- `_headers`: security headers (CSP, nosniff, referrer policy, permissions policy, frame blocking), `X-Robots-Tag: noindex` on the zine PDF, and 7-day caching for `/assets/`.
- Links and asset paths are relative to each page and point at `index.html` files, so the site works in all three places it gets viewed: opened from disk, on a `github.io/<repo>/` project URL, and at a domain root. On Cloudflare, `/help/index.html` links redirect to the clean `/help/` (the canonical tags already use clean URLs). The 404 page uses root-absolute paths because servers show it at any depth.
- **Local preview:** open `index.html` directly, or run `python3 -m http.server`. To preview redirects and headers exactly as Cloudflare serves them: `npx wrangler pages dev .`

## What's here

- `index.html`: About, used as the home page
- `help/`, `fees/`, `contact/`, `zine/`
- `crisis/`, `privacy/`, `accessibility/`, `404.html`
- `sitemap.xml`, `robots.txt`, `_redirects`, `_headers`
- Bootstrap is served from `assets/`, not a CDN, so there are no third-party requests. That keeps the privacy page accurate.
- `bootstrap.purged.css` is Bootstrap with the unused rules stripped out (232 KB down to 34 KB). If you add Bootstrap classes that aren't used yet, either re-run PurgeCSS or point the pages at `bootstrap.full.min.css`.
- `zine/checking-the-box.pdf` is the zine compressed from 15 MB to 4.3 MB, now served from this site instead of the awards repo. A `noindex` header keeps it out of search results; named AI training crawlers are blocked from it in `robots.txt`.
- Photos of Jon (`jon-portrait`, `jon-seated`, `jon-smiling`, `office`) are resized from his originals, with all metadata (including any location data) stripped. `og.jpg` (the link preview) is cropped from the portrait.
- Layout: two columns on desktop (text left, image right); one column on phones. Home, What I help with and Fees + FAQ open with a photo: on desktop its top lines up with the page heading, and on phones it comes right after the heading (portrait, seated, and smiling photos respectively). On desktop, What I help with also shows his diagonal-marks drawing under the intro to fill the space beside the tall photo; it is decorative (aria-hidden) and hidden on phones. The drawings on What I help with sit on a light, lopsided splotch in the armchair green (`#9aa33a` at 22%), stay in view beside their section on desktop, and multiply into the paper.
- Colour, from Jon's office: couch blue `#1f4e8c` is the one accent (links, buttons, focus outline, at-a-glance border; 7.8:1 on the page). Armchair olive `#8a8f3a` is decorative only (the pull-quote rules). A faint paper grain (inline SVG noise, 14% opacity, multiplied) sits over the whole page so the drawings, photos and background share the same "paper". It's off for visitors who ask for more contrast or reduced transparency, and when printing. To remove it, delete the `body::after` block at the end of `site.css`. Photos have rounded corners and a soft shadow; drawings sit directly on the page.
- Favicons (`favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`) are cropped from Jon's diagonal-marks ink drawing (the one he calls "one of my all time favorite drawings" in the zine), keeping three whole strokes so they read at 16px. Jon should OK it along with the design direction.

## SEO

- Every page has a unique title (60 characters or fewer), a meta description (160 or fewer), a canonical URL, link-preview tags, and one H1.
- Home page structured data (JSON-LD): `WebSite`, `Person`, and `MedicalBusiness` (schema.org has no therapist type; `ProfessionalService` is deprecated). `Person` includes his Oregon LPC license (C8085, confirmed on the OBLPCT register 2026-09-22) as a credential. Address: 1210 SE Oak St, Portland, OR 97214 (from Jon, 2026-09-30), plus a `hasMap` link to Google Maps. **Phone is still unconfirmed.**
- Fees page: `FAQPage` markup that matches the visible Q&A word for word. Google stopped showing FAQ rich results in 2026; it's kept because it's valid and other engines still read it.
- `sitemap.xml` (with lastmod dates) and `robots.txt`.
- Footer has name, license, full street address, and email in an `<address>` element. Keep this identical to Psychology Today, TherapyDen, and similar listings.
- Lighthouse, mobile: SEO 100, accessibility 100, best practices 100, performance 99–100. LCP about 2 s, CLS 0.

### AI search (ChatGPT, Perplexity, Google AI Overviews, Claude)
- The pages are plain HTML, so every crawler reads the full text. Nothing depends on JavaScript.
- The home page's at-a-glance box states the facts AI answers pull from, in one place: location, focus areas, approach, credentials, fee, and how to start.
- Structured data includes `sameAs`, linking to his Psychology Today profile so engines treat the two as one person.
- `robots.txt`: every crawler may read every page (search, AI search, AI training). Named AI *training* crawlers can't read the zine PDF. Search engines can, and they see its `noindex` header.
- No `llms.txt`: there's little evidence answer engines use it. Add it later if that changes.

### After launch
See the launch guide (kept outside this repo). The Google Business Profile can be set up now that the address is known.

## Verified

- HTML validates (html-validate) on every page
- Footer on every page carries the "email isn't secure" notice next to the email link
- axe (WCAG 2.0/2.1 A + AA): 0 violations on every page
- Every internal link resolves (crawled under Cloudflare's local emulator), and none hits a redirect
- Keyboard: skip link is the first Tab stop and moves focus to `<main>`; visible focus ring on everything
- Mobile: no horizontal scroll at 320, 360, 390, 414 or 768px on any page, including with the menu open. Standalone tap targets (crisis links, menu button, nav, footer, buttons) are at least 44×44px. Body text is 18px, and images scale to fit the screen.
- Contrast on #faf8f3: ink 16.2:1, accent (couch blue) 7.8:1, muted 8.4:1; button text on blue 7.8:1
- Zero external requests at page load
- **Not done: a VoiceOver pass.** Do one before calling it AA.

## Editing

You can edit the HTML directly, or change `_build.py` and run `python3 _build.py` to regenerate every page with the shared header and footer. Leave `_build.py` in the repo or remove it; nothing depends on it.
