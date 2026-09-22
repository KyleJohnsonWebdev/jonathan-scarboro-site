# maletherapistinportland.com: temporary site

This is a static HTML and Bootstrap 5.3.8 site. It stands in until the Astro/Sanity build is ready. It has no build step: every file here is what gets served.

**Domains:** `maletherapistinportland.com` is the main one. `jscar.care` (printed on the zines) and `therapyformenportland.com` redirect to it with permanent 301 redirects. Email stays `hi@jscar.care`, since email and websites are set up separately.

## Deploy

Step-by-step instructions for GitHub Pages, the Cloudflare redirects, and SEO setup are in **`LAUNCH-GUIDE.md`**.

Old mmm.page URLs are handled by meta-refresh stubs: `/about`, `/main` → `/` · `/approach` → `/help/` · `/dudes` → `/help/#mens-issues` · `/blocks` → `/help/#creative-blocks` · `/business` → `/fees/`. `/zine/` exists, so the printed zines resolve via the jscar.care redirect.

All links are relative and point at `index.html` files, so the site works when you open it straight from disk, from a `username.github.io/repo/` preview, and on the custom domain. The canonical tags still use clean URLs (`/help/`). The one exception is `404.html`, which only works properly on the custom domain.

## What's here

- `index.html`: About, used as the home page
- `help/`, `fees/`, `contact/`, `zine/`
- `crisis/`, `privacy/`, `accessibility/`, `404.html`
- `sitemap.xml`, `robots.txt`, `.nojekyll`
- Bootstrap is served from `assets/`, not a CDN, so there are no third-party requests. That keeps the privacy page accurate.
- `bootstrap.purged.css` is Bootstrap with the unused rules stripped out (232 KB down to 34 KB). If you add Bootstrap classes that aren't used yet, either re-run PurgeCSS or point the pages at `bootstrap.full.min.css`.
- `zine/checking-the-box.pdf` is the zine compressed from 15 MB to 4.3 MB, now served from this site instead of the awards repo. `robots.txt` keeps it out of search because its credits page names private people.
- Favicons (`favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`) are cropped from Jon's diagonal-marks ink drawing (the one he calls "one of my all time favorite drawings" in the zine), keeping three whole strokes so they read at 16px. Jon should OK it along with the design direction.

## SEO

- Every page has a unique title (60 characters or fewer), a meta description (160 or fewer), a canonical URL, link-preview tags, and one H1.
- Home page structured data (JSON-LD): `WebSite`, `Person`, and `MedicalBusiness` (schema.org has no therapist type; `ProfessionalService` is deprecated). `Person` includes his Oregon LPC license (C8085, confirmed on the OBLPCT register 2026-09-22) as a credential. The address has city, state, and ZIP 97214 only. **Add the street address and phone once Jon confirms them.**
- Fees page: `FAQPage` markup that matches the visible Q&A word for word. Google stopped showing FAQ rich results in 2026; it's kept because it's valid and other engines still read it.
- `sitemap.xml` (with lastmod dates) and `robots.txt`.
- Footer has name, city/ZIP, and email in an `<address>` element. Keep this identical to Psychology Today, TherapyDen, and similar listings.
- Lighthouse, mobile: SEO 100, accessibility 100, best practices 100, performance 99–100. LCP about 2 s, CLS 0.

### AI search (ChatGPT, Perplexity, Google AI Overviews, Claude)
- The pages are plain HTML, so every crawler reads the full text. Nothing depends on JavaScript.
- The home page's at-a-glance box states the facts AI answers pull from, in one place: location, focus areas, approach, credentials, fee, and how to start.
- Structured data includes `sameAs`, linking to his Psychology Today profile so engines treat the two as one person.
- `robots.txt` lets all crawlers in, including AI ones. Whether to block AI *training* crawlers (as opposed to AI search crawlers) is Jon's call. It's on the sign-off list.
- No `llms.txt`: there's little evidence answer engines use it. Add it later if that changes.

### After launch
See `LAUNCH-GUIDE.md`, Part 4.

## Verified

- HTML validates (html-validate) on every page
- axe (WCAG 2.0/2.1 A + AA): 0 violations on every page
- All 100 internal links resolve, both when opened from disk and when served
- Keyboard: skip link is the first Tab stop and moves focus to `<main>`; visible focus ring on everything
- Mobile: no horizontal scroll at 320, 360, 390, 414 or 768px on any page, including with the menu open. Standalone tap targets (crisis links, menu button, nav, footer, buttons) are at least 44×44px. Body text is 18px, and images scale to fit the screen.
- Contrast on #faf8f3: ink 16.2:1, accent 7.9:1, muted 8.4:1
- Zero external requests at page load
- **Not done: a VoiceOver pass.** Do one before calling it AA.

## Editing

You can edit the HTML directly, or change `_build.py` and run `python3 _build.py` to regenerate every page with the shared header and footer. Leave `_build.py` in the repo or remove it; nothing depends on it.
