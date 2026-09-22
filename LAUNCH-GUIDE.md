# Launch guide: maletherapistinportland.com

The full sequence, in order. The DNS facts were checked against GitHub's and Cloudflare's current docs on 2026-09-22.

**Domains:** `maletherapistinportland.com` is the main site. `jscar.care` (printed on the zines) and `therapyformenportland.com` send visitors there with a permanent (301) redirect that keeps the rest of the address. Email stays `hi@jscar.care`.

---

## Part 1: GitHub Pages

**1. Create the repo.** On GitHub: New repository → e.g. `jonathan-scarboro-site` → **Public** (free accounts only get Pages on public repos). Don't add a README, license, or `.gitignore`.

**2. Push the files.** Unzip `maletherapist-stopgap.zip`. Push what's *inside* the folder, so `index.html` sits at the repo root:
```bash
cd maletherapist-stopgap
git init
git add -A
git commit -m "Stopgap site"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

**3. Turn on Pages.** Repo → Settings → Pages → Source: **Deploy from a branch** → `main` / `(root)` → Save. After a minute or two it's live at `https://<username>.github.io/<repo>/`. Click through every page there.

**4. Verify the domain** (stops anyone else claiming it on GitHub). GitHub profile → Settings → Pages → **Add a domain** → `maletherapistinportland.com` → add the TXT record GitHub shows you at your DNS provider → Verify.

**5. Add the custom domain in the repo, before touching DNS.** Repo → Settings → Pages → Custom domain → `maletherapistinportland.com` → Save. GitHub commits a `CNAME` file for you; run `git pull` before your next push. GitHub's docs say to do this *before* the DNS step, so the domain is never left open to takeover.

**6. Point maletherapistinportland.com at GitHub.** At its DNS provider:

| Type | Name | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA (optional) | `@` | `2606:50c0:8000::153` · `2606:50c0:8001::153` · `2606:50c0:8002::153` · `2606:50c0:8003::153` |
| CNAME | `www` | `<username>.github.io` |

- Don't add wildcard (`*`) records. GitHub warns they invite domain takeover.
- If this domain's DNS is on Cloudflare, set these records to **DNS only (grey cloud)**, not Proxied. Otherwise GitHub can't issue the certificate.
- GitHub redirects `www` to the bare domain automatically.

**7. HTTPS.** Once the DNS check passes (minutes to a few hours), tick **Enforce HTTPS** in Pages settings. The certificate can take up to about an hour.

---

## Part 2: Redirect domains (Cloudflare, free plan)

GitHub Pages serves one domain per site, so the other two redirect through Cloudflare. Registrar "forwarding" usually can't do https, and browsers now try https first, so someone typing `jscar.care/zine` from a printed zine would hit a security warning.

Do this for **jscar.care** and **therapyformenportland.com**:

1. **Add the domain to Cloudflare** (free plan). It scans the existing DNS records.
2. **jscar.care only: protect email.** Before changing nameservers, confirm Cloudflare imported every email record: **MX**, **TXT** (SPF, DMARC), and any **CNAME/TXT for DKIM**. Compare against the current DNS provider. If one is missing, `hi@jscar.care` stops receiving mail. Leave these records **DNS only**.
3. **Remove the old website records** (anything pointing at mmm.page), then add:
   - `A` · `@` · `192.0.2.1` · **Proxied**
   - `A` · `www` · `192.0.2.1` · **Proxied**

   192.0.2.1 is a placeholder from Cloudflare's own guide. Cloudflare answers before traffic goes anywhere.
4. **Switch nameservers** at the registrar to the two Cloudflare gives you.
5. **Create the redirect.** Rules → Overview → Create rule → **Redirect Rule**:
   - When: custom filter expression `(http.host in {"jscar.care" "www.jscar.care"})` (use the matching names for therapyformenportland.com)
   - Then: type **Dynamic**, expression `concat("https://maletherapistinportland.com", http.request.uri.path)`
   - Status code **301**, **Preserve query string** on → Deploy
6. **Test:**
   - `https://jscar.care/zine` → `https://maletherapistinportland.com/zine/`
   - `https://www.therapyformenportland.com` → the home page
   - `https://jscar.care/dudes` → `/help/#mens-issues` (redirect, then the site's own forwarding page)
   - Send an email to `hi@jscar.care` and confirm it arrives.

---

## Part 3: Launch check

- [ ] Every page loads on `https://maletherapistinportland.com`, and `www` redirects to it
- [ ] Old addresses work on the new domain and via jscar.care: `/about` `/main` `/approach` `/dudes` `/blocks` `/business`
- [ ] `/zine/` loads and the PDF downloads
- [ ] A made-up address (e.g. `/nope`) shows the 404 page
- [ ] Menu, crisis bar, and the 988 link work on a real iPhone and a real Android phone
- [ ] Email to `hi@jscar.care` arrives
- [ ] Unpublish the old mmm.page site
- [ ] Delete `Checking_the_Box_zine_Scarboro_final.pdf` from the `awards` repo

---

## Part 4: SEO

### Week 1: tell the search engines
1. **Google Search Console** → add a **Domain** property for `maletherapistinportland.com` (verified with a DNS TXT record; covers http, https, www).
   - Sitemaps → submit `https://maletherapistinportland.com/sitemap.xml`
   - URL Inspection → request indexing for `/`, `/help/`, `/zine/`
2. **Tell Google jscar.care moved.** Add `jscar.care` as a second Domain property, then Settings → **Change of Address** → choose maletherapistinportland.com. Only do this after the jscar.care redirects are live and tested.
3. **Bing Webmaster Tools** → sign in → **Import from Google Search Console**. This covers Bing and DuckDuckGo, and part of ChatGPT's search, which draws partly on Bing's index.
4. **Check the structured data:** paste the home page URL into Google's **Rich Results Test** and **validator.schema.org**. You should see Person (with the LPC credential) and MedicalBusiness, with no errors.

### Week 1: make his listings match
These feed Google's local results and AI answers as much as his own site does. Use the same details everywhere:

> **Jonathan Scarboro, MS, LPC, NCC** · Portland, OR 97214 · hi@jscar.care · https://maletherapistinportland.com

5. **Psychology Today:** update the website link. This is also the time to soften the claims language ("potent form of traumatic memory processing," "the key difference between successful therapy…"). AI tools are most likely to quote that profile.
6. **Portland Therapy Center:** remove his profile, since he's left, or update it if it stays.
7. **TherapyDen**, **GoodTherapy**, and **Yelp**, if listings exist: same details, new link.

### When Jon answers the sign-off list
8. **Google Business Profile.** This is the biggest single boost for local search, and it needs the street address. business.google.com → add the business → the closest category (e.g. Psychotherapist or Counselor) → office address → verify (usually a video or a postcard) → website: maletherapistinportland.com. Then add the street address to the site's structured data.
9. **Trauma section:** publish once he approves the draft. It's what makes the site findable for "trauma therapy Portland."
10. **Insurance:** when the first plan is active, follow the checklist in `JON-SIGNOFF.md`.
11. **AI crawlers:** he decides whether AI *training* crawlers are blocked. AI *search* crawlers stay allowed either way.

### Ongoing
12. **After 2–4 weeks:** in Search Console, check **Pages** (anything not indexed, and why) and **Performance** (which searches he shows up for). New domains usually take a few weeks to appear.
13. **When a fact changes** (address, phone, insurance, availability, session length), update the site and every listing on the same day.

---

## Found in the final review (2026-09-22)

Fixed before this package:
- **Good Faith Estimate timing was wrong.** It said the estimate arrives "at least 1 business day before your first session." CMS says it's due within 1 business day of scheduling (3–9 business days out), or within 3 business days (10 or more out). Corrected.
- **Deploy order.** Earlier instructions pointed DNS before adding the domain in GitHub. Reversed, per GitHub's docs.
- **Cloudflare proxy setting** for the main domain's GitHub records (must be DNS only). Added.
- **Vague link text** ("more," "details") in the home page's at-a-glance box. It cost 8 SEO points and hurts screen reader users. Now "What I help with" and "Fees and FAQ".
- **HTML validity:** unescaped `&` in two page titles, and the crisis bar now uses a `<section>` element instead of an ARIA role. All pages now pass an HTML validator.
- **Duplicate license line** on the home page removed. The at-a-glance box and footer carry it.
- **Privacy page** now names Cloudflare as well as GitHub, since the redirect domains pass through it.
- **Favicon** replaced: the placeholder "JS" monogram is now three strokes from Jon's diagonal-marks drawing, checked at 16px, 32px and on an iOS home screen.

Still open (on Jon's list, not blockers):
- Session length says 55 minutes. The old disclosure statement said 50, and it may depend on payer type.
- "Currently accepting new clients" is hardcoded.
- The trauma section, street address, and phone number.
- The robots.txt block on the zine PDF stops Google *crawling* it, but Google can still list the bare link if other sites point to it. GitHub Pages can't send the header that would prevent that. Removing the credits page from the PDF is the real fix, and it's Jon's call.
- No VoiceOver session yet. Do one before calling the site WCAG 2.1 AA.

## Verified (this package)
HTML validates on every page · axe: 0 violations · Lighthouse, mobile: SEO 100, accessibility 100, best practices 100, performance 99–100 · 100 internal links resolve, both served and opened from disk · keyboard: skip link first, visible focus · no horizontal scroll at 320–768px · 44px minimum tap targets · FAQ markup matches the page word for word · no external requests · no stale credentials, addresses, or claims language anywhere on the site.
