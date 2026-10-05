#!/usr/bin/env python3
"""Builds the stopgap site (maletherapistinportland.com) into ./site. Plain static HTML output."""
import json
from datetime import date
from pathlib import Path

OUT = Path(__file__).parent  # writes HTML next to this script
EMAIL = "hi@jscar.care"
ZINE_PDF = "checking-the-box.pdf"  # relative to /zine/; compressed from the 15 MB original
SITE = "https://maletherapistinportland.com"  # canonical. jscar.care and therapyformenportland.com 301 here.
NAME = "Jonathan Scarboro, MS, LPC, NCC"
STREET = "1210 SE Oak St"  # from Jon, 2026-09-30
MAPS = "https://www.google.com/maps/search/?api=1&query=1210+SE+Oak+St+Portland+OR+97214"
PT = "https://www.psychologytoday.com/us/therapists/jonathan-scarboro-portland-or/1035351"
LICENSE = "C8085"  # OBLPCT register: LPC, active, issued 2026-06-10, expires 2027-06-30

NAV = [
    ("./", "About"),
    ("help/", "What I help with"),
    ("fees/", "Fees + FAQ"),
    ("contact/", "Free consultation"),
    ("zine/", "Zine"),
]

# ---------------------------------------------------------------- Structured data
# Types checked against schema.org (Sept 2026). ProfessionalService is deprecated;
# there is no therapist/counselor type, and Psychiatric would imply a psychiatrist,
# so the practice is MedicalBusiness (a LocalBusiness subtype). No street address or
# phone yet: both unconfirmed. License confirmed on the OBLPCT register 2026-09-22.
PRACTICE_ID = SITE + "/#practice"
PERSON_ID = SITE + "/#jonathan"
HOME_SCHEMA = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME},
        {
            "@type": "Person", "@id": PERSON_ID, "name": "Jonathan Scarboro", "honorificSuffix": "MS, LPC, NCC",
            "jobTitle": "Licensed Professional Counselor", "url": SITE + "/", "email": EMAIL,
            "image": SITE + "/assets/img/jon-portrait.jpg",
            "alumniOf": {"@type": "CollegeOrUniversity", "name": "Portland State University"},
            "knowsAbout": ["Gestalt therapy", "Men's issues", "Creative blocks", "Trauma therapy", "Screen-related addictions"],
            "worksFor": {"@id": PRACTICE_ID},
            # Same person elsewhere: helps search and AI engines tie profiles to one entity.
            # Portland Therapy Center left out on purpose: he no longer practices there.
            "sameAs": ["https://www.psychologytoday.com/us/therapists/jonathan-scarboro-portland-or/1035351"],
            "hasCredential": {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "license",
                "name": "Licensed Professional Counselor (LPC)",
                "identifier": LICENSE,
                "recognizedBy": {"@type": "GovernmentOrganization",
                                 "name": "Oregon Board of Licensed Professional Counselors and Therapists",
                                 "url": "https://www.oregon.gov/oblpct"},
                "validIn": {"@type": "State", "name": "Oregon"},
            },
        },
        {
            "@type": "MedicalBusiness", "@id": PRACTICE_ID, "name": NAME,
            "description": "Therapy practice in Portland, Oregon working primarily with men. In person in inner Southeast Portland and online for clients located in Oregon.",
            "url": SITE + "/", "email": EMAIL, "image": SITE + "/assets/img/og.jpg",
            "address": {"@type": "PostalAddress", "addressLocality": "Portland", "addressRegion": "OR",
                        "postalCode": "97214", "addressCountry": "US", "streetAddress": STREET},
            "hasMap": MAPS,
            "areaServed": {"@type": "State", "name": "Oregon"},
            "priceRange": "$140 per session; limited sliding scale",
            "paymentAccepted": "American Express, Discover, Mastercard, Visa, Venmo",
            "founder": {"@id": PERSON_ID},
        },
    ],
}

# Mirrors the visible Q&A on /fees/ word for word (required: markup must match the page).
# Google stopped showing FAQ rich results in 2026; kept because it's valid, cheap,
# and other engines and AI answer tools still read it.
FAQ_PAIRS = [
    ("Do you offer a consultation?",
     f"Yes — I offer a free 15-minute consultation to see if we're a good fit. You can reach me through Psychology Today or at {EMAIL}."),
    ("Do you work only with men?",
     "I specialize in working with men because I felt there were too few providers with specialized training in the issues I saw affecting the men around me and in my care. I also enjoy working with women/femme, trans, and non-binary clients."),
    ("Do you take insurance?",
     "I do not bill insurance directly, but I can provide a superbill to help you seek reimbursement."),
    ("Can I see you online if I don't live in Oregon?",
     "Online sessions are for clients who are physically located in Oregon at the time of the session."),
    ("How can I get ahold of you?",
     f"Through Psychology Today or at {EMAIL}. I typically respond within 1–2 business days."),
]
FAQ_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in FAQ_PAIRS
    ],
}

EMAIL_NOTE = (
    '<p class="small">Heads up: email isn\'t a secure way to send private information. '
    "Keep it to scheduling and logistics, and save the details for when we talk.</p>"
)


def mail(text=None):
    return f'<a href="mailto:{EMAIL}">{text or EMAIL}</a>'


def fig(p, src, alt, caption=None, cls="", color="green", photo=False):
    """WebP with JPEG fallback; width/height set so the layout doesn't jump as images load.
    color: the decorative splotch behind the image (green, blue, orange, mustard, teal)."""
    cls = f"{cls} {'photo' if photo else ''}".strip()  # color arg kept for later; unused
    from PIL import Image
    w, h = Image.open(OUT / "assets/img" / src).size
    webp = src.rsplit(".", 1)[0] + ".webp"
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    hidden = ' aria-hidden="true"' if not alt else ""
    return (f'<figure class="drawing {cls}"{hidden}><picture>'
            f'<source srcset="{p}assets/img/{webp}" type="image/webp">'
            f'<img src="{p}assets/img/{src}" alt="{alt}" width="{w}" height="{h}" decoding="async">'
            f'</picture>{cap}</figure>')


def link(p, target):
    """Link to a page folder, relative to the current page: 'help/' -> '../help/index.html'.
    On a server that serves / for index.html (Cloudflare) these redirect to the clean URL."""
    if p == "/":                                   # 404 page: served at any depth, so root-absolute clean URLs
        return "/" if target in ("./", "") else "/" + target
    base = "" if target in ("./", "") else target
    return f"{p}{base}index.html"


def page(path, title, desc, body, current=None, noindex=False, schema=None, root=None):
    # Relative to this page's folder, so the site works opened from disk, on a github.io/repo/ subpath,
    # and at a domain root. The 404 page overrides this with "/" (servers show it at any depth).
    p = root if root is not None else "../" * path.count("/")
    canonical = SITE + "/" + path.replace("index.html", "")
    cur = ' aria-current="page"'
    nav = "\n".join(
        f'<li class="nav-item"><a class="nav-link" href="{link(p, href)}"'
        f'{cur if href == current else ""}>{label}</a></li>'
        for href, label in NAV
    )
    from html import escape
    title, desc = escape(title, quote=True), escape(desc, quote=True)
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/og.jpg">
<meta property="og:image:alt" content="Jonathan Scarboro sitting on a blue couch in his office">
<link rel="icon" href="{p}favicon.ico" sizes="any">
<link rel="icon" href="{p}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="stylesheet" href="{p}assets/css/bootstrap.purged.css">
<link rel="stylesheet" href="{p}assets/css/site.css">
{ld}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<section class="crisis-bar" aria-label="Crisis support">
  <div class="container">In crisis? Call or text <a href="tel:988">988</a>, or call 911. This site isn't crisis care. <a href="{link(p, "crisis/")}">More on getting help now</a></div>
</section>
<header class="site-header">
  <nav class="navbar navbar-expand-lg" aria-label="Main">
    <div class="container">
      <a class="navbar-brand" href="{link(p, "./")}">Jonathan Scarboro<small>MS, LPC, NCC · Therapy in Portland, OR</small></a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#site-nav" aria-controls="site-nav" aria-expanded="false" aria-label="Menu">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse site-nav" id="site-nav">
        <ul class="navbar-nav ms-auto">
{nav}
        </ul>
      </div>
    </div>
  </nav>
</header>
<main id="main" tabindex="-1">
  <div class="container">
{body}
  </div>
</main>
<footer class="site-footer">
  <div class="container">
    <div class="row gy-3">
      <div class="col-md-6">
        <address class="mb-0">
          <strong>{NAME}</strong><br>
          Licensed Professional Counselor · Oregon license {LICENSE}<br>
          {STREET}, Portland, OR 97214<br>
          In person in inner Southeast Portland · Online for clients located in Oregon<br>
          {mail()}
        </address>
        <p class="muted small mt-2 mb-0">Email isn't secure. Please keep it to scheduling and logistics.</p>
      </div>
      <div class="col-md-6">
        <ul class="list-unstyled mb-2">
          <li><a href="{link(p, "crisis/")}">Crisis resources</a></li>
          <li><a href="{link(p, "privacy/")}">Privacy</a></li>
          <li><a href="{link(p, "accessibility/")}">Accessibility</a></li>
        </ul>
        <p class="muted mb-0">Drawings by Jonathan Scarboro, <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>.</p>
      </div>
    </div>
  </div>
</footer>
<script src="{p}assets/js/bootstrap.bundle.min.js" defer></script>
</body>
</html>
"""
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html)


# ---------------------------------------------------------------- About (home)
def about():
    p = ""
    body = f"""
<div class="home-hero">
  <h1 class="home-h1">Hi — Jonathan here.</h1>
  <div class="home-text">
    <div class="prose">
      <p class="lede">I'm a therapist who works primarily with men. I offer in-person therapy in Portland and online therapy throughout Oregon.</p>
      <ul class="at-a-glance" aria-label="At a glance">
        <li><strong>Where:</strong> In person at {STREET} in inner Southeast Portland, or online for clients in Oregon</li>
        <li><strong>Focus:</strong> Men's issues, creative blocks, trauma therapy, screen-related addictions · <a href="{link(p, 'help/')}">What I help with</a></li>
        <li><strong>Approach:</strong> Gestalt therapy, a relational and experiential approach</li>
        <li><strong>Credentials:</strong> Licensed Professional Counselor (Oregon {LICENSE}), MS in Clinical Mental Health Counseling (Portland State), NCC</li>
        <li><strong>Fee:</strong> $140 per session, limited sliding scale · <a href="{link(p, 'fees/')}">Fees and FAQ</a></li>
        <li><strong>First step:</strong> <a href="{link(p, 'contact/')}">Free 15-minute consultation</a></li>
      </ul>
      <h2>How I got here</h2>
      <p>I first came to therapy as a client after getting divorced and watching my small business fall apart. Therapy helped me through one of the hardest periods of my life, and it's deeply meaningful to now support other people navigating their own transitions and setbacks.</p>
      <p class="pull">We'll likely be a good fit if you appreciate humor, a straightforward no-BS approach, and are open to doing real work.</p>
      <h2>Who I usually work with</h2>
      <p>Most of my clients are thoughtful, capable people who look like they're holding things together on the outside — careers, relationships, responsibilities — but feel disconnected or stuck underneath. Many come in after a painful relationship, burnout, or the realization that long-standing patterns just aren't working anymore. They're often dealing with avoidance, overwhelm, or distraction habits that keep them from addressing what actually matters.</p>
      <p>I also work with many artists, musicians, entrepreneurs, and other creative people on nonlinear paths who want change without sacrificing meaning or identity.</p>
      <p>If you're starting to think we might be a good fit, you can learn more about <a href="{link(p, 'help/')}">my approach</a> or <a href="{link(p, 'contact/')}">schedule a free consultation</a>.</p>
      <p class="mt-4"><a class="btn btn-ink" href="{link(p, 'contact/')}">Book a free 15-minute consultation</a></p>
    </div>
  </div>
  <div class="home-photo">
    {fig(p, "jon-portrait.jpg", "Jonathan Scarboro sitting on a blue velvet couch in his office, leaning forward with his hands clasped.", color="orange", photo=True)}
  </div>
</div>
"""
    page("index.html",
         "Male Therapist in Portland, OR | Jonathan Scarboro, LPC",
         "Gestalt therapist in Portland, OR working mostly with men: relationships, burnout, transitions, creative blocks. In person in SE Portland or online in Oregon.",
         body, current="./", schema=HOME_SCHEMA)


# ---------------------------------------------------------------- What I help with
def help_page():
    p = "../"
    body = f"""
<div class="home-hero">
  <h1 class="home-h1">What I help with</h1>
  <div class="home-text prose">
  <p class="lede">My style is active, direct, playful, and practical. I offer clear feedback and concrete strategies while keeping our work oriented toward meaning, purpose, and the bigger picture of your life.</p>
  <p>I specialize in:</p>
  <ul>
    <li><a href="#mens-issues">Men's issues</a></li>
    <li><a href="#creative-blocks">Creative blocks</a></li>
    <li>Trauma therapy</li>
    <li>Screen-related addictions (gaming, phones, porn)</li>
  </ul>
  {fig(p, "marks.jpg", "", cls="hero-filler")}
  </div>
  <div class="home-photo">
    {fig(p, "jon-seated.jpg", "Jonathan Scarboro sitting on a step in his office, one boot up, next to a stack of books.", photo=True)}
  </div>
</div>

<section aria-labelledby="mens-issues" class="row gy-4 gx-lg-5 mt-1">
  <div class="col-lg-7 prose">
    <h2 id="mens-issues">Men's issues counseling</h2>
    <p>Many of the clients I work with are men who appear competent and functional on the outside but feel stuck, disconnected, or under constant pressure internally.</p>
    <p>You might recognize yourself in:</p>
    <ul>
      <li>Difficulty accessing or expressing emotions</li>
      <li>Feeling numb, shut down, or stuck in your head</li>
      <li>Repeating relationship patterns you don't fully understand</li>
      <li>Anxiety, irritability, or chronic stress</li>
      <li>Creative blocks or loss of direction</li>
      <li>Understanding things intellectually but still feeling stuck</li>
      <li>Checking out through work, screens, gaming, or porn</li>
    </ul>
    <p>For many men, there's an unspoken rule that you're supposed to handle things yourself — stay in control, don't need too much, don't fall apart. That strategy often works until it doesn't, snapping catastrophically rather than bending flexibly.</p>
    <p>My approach respects the strengths that got you this far while helping you become more flexible, more connected, and more effective — without losing your edge.</p>
    <p>If this resonates, <a href="{link(p, 'contact/')}">get in touch to schedule a free consultation</a> so we can discuss your needs and see if we're a good fit.</p>
  </div>
  <div class="col-lg-5">
    {fig(p, "shoes.jpg", "Pen drawing of a pair of wingtip dress shoes with textured leather and wooden soles.", "I bought these at a thrift store years ago with no occasion to wear them. Someone told me, “Maybe your life will grow into them.” They're now the shoes I wear to work most often.")}
  </div>
</section>

<section aria-labelledby="creative-blocks" class="row gy-4 gx-lg-5 mt-1">
  <div class="col-lg-7 prose">
    <h2 id="creative-blocks">Creative blocks</h2>
    <p>Most of my clients have some form of creative impulse — art, music, writing, entrepreneurship, problem-solving, or simply a sense that something important on the inside isn't getting fully expressed.</p>
    <h3>What it looks like</h3>
    <p>Creative blocks rarely exist in isolation. The same patterns often show up across the rest of life: perfectionism, avoidance, self-doubt, overwhelm, fear of judgment, difficulty finishing, or loss of momentum.</p>
    <p>The encouraging part is that changes in one area often unlock movement in another.</p>
    <h3>How we work on it</h3>
    <p>I don't do art therapy. Instead, we explore how your creative process actually works — where it gets stuck, what conditions help it move, and what the block might be communicating. From there, we develop practical ways to help you re-engage with motivation and forward movement.</p>
    <h3>Where I'm coming from</h3>
    <p>My perspective is shaped by both clinical training and my own background as a visual artist, including formal arts education, leadership in creative communities, and professional museum work. I also spent about a decade in a significant creative block myself and eventually found my way through it, which deeply informs how I approach this work.</p>
    <p>I wrote a long-form zine about that experience. <a href="{link(p, 'zine/')}">It's free to read</a> :)</p>
    <p>Creative work can be integrated into ongoing therapy or approached in a shorter-term, focused format depending on your goals.</p>
  </div>
  <div class="col-lg-5">
    {fig(p, "pen-cup.jpg", "Pen drawing of a ceramic cup crammed with paintbrushes, markers, and pens.", color="green")}
  </div>
</section>

<section aria-labelledby="training" class="row gy-4 gx-lg-5 mt-1">
  <div class="col-lg-7 prose">
    <h2 id="training">Gestalt therapy: training and approach</h2>
    <p>I hold a Master of Science in Clinical Mental Health Counseling from Portland State University and have post-graduate training in multiple therapeutic modalities. I am trained most extensively in Gestalt therapy, a relational and experiential approach.</p>
    <p>As a Gestalt therapist, I don't define health as simply adjusting to the expectations of dominant culture. Instead, we focus on developing awareness of your particular wants, needs, and values — and finding more effective ways to live those out in the real conditions of your life.</p>
  </div>
  <div class="col-lg-5">
    {fig(p, "books.jpg", "Pen drawing of a stack of books: The Courage to Create, The Power of Fun, Free Play, The Denial of Death, Make Your Art No Matter What, The Creative Act, Atomic Habits, The Artist's Way, and Gestalt Therapy on the bottom.", "Books that were on my mind or on my desk while I made my zine.", color="teal")}
  </div>
</section>
"""
    page("help/index.html",
         "Men's Issues Counseling & Gestalt Therapy, Portland OR",
         "Counseling for men's issues, creative blocks, trauma, and screen habits (gaming, phones, porn) in Portland, OR. In person or online in Oregon.",
         body, current="help/")


# ---------------------------------------------------------------- Fees + FAQ
def fees():
    p = "../"
    body = f"""
<div class="home-hero">
  <h1 class="home-h1">Fees + FAQ</h1>
  <div class="home-text prose">
    <p class="lede">I have a limited number of openings and am currently accepting new clients. Sessions are available in person at my office in inner Southeast Portland and online throughout Oregon. I prefer in-person work whenever possible.</p>

    <h2 id="fees">Fees</h2>
    <ul>
      <li>55-minute session: $140</li>
      <li>Limited sliding scale spots available</li>
      <li>I am an out-of-network behavioral health provider, meaning fees are out-of-pocket. I can, however, provide superbills for insurance reimbursement.</li>
      <li>I accept Amex, Discover, Mastercard, Visa, and Venmo.</li>
    </ul>

    <div class="notice" role="note" aria-labelledby="gfe-title">
      <h3 id="gfe-title" class="h5">Your right to a Good Faith Estimate</h3>
      <p>Under the federal No Surprises Act, you have the right to receive a “Good Faith Estimate” explaining how much your care will cost if you don't have insurance or aren't using it.</p>
      <ul>
        <li>You can ask for a Good Faith Estimate before you schedule a service, or at any time.</li>
        <li>If you schedule at least 3 business days ahead, you'll get it in writing within 1 business day of scheduling (within 3 business days if you schedule 10 or more business days ahead).</li>
        <li>If you get a bill that's at least $400 more than your Good Faith Estimate, you can dispute the bill.</li>
        <li>Keep a copy or photo of your Good Faith Estimate.</li>
      </ul>
      <p class="mb-0">For questions or more information, visit <a href="https://www.cms.gov/nosurprises">cms.gov/nosurprises</a> or call 1-800-985-3059.</p>
    </div>

    <h2 id="faq">Frequently asked questions</h2>
    <dl class="faq">
      <dt>Do you offer a consultation?</dt>
      <dd>Yes — I offer a free 15-minute consultation to see if we're a good fit. You can reach me through <a href="{PT}">Psychology Today</a> or at {mail()}.</dd>

      <dt>Do you work only with men?</dt>
      <dd>I specialize in working with men because I felt there were too few providers with specialized training in the issues I saw affecting the men around me and in my care. I also enjoy working with women/femme, trans, and non-binary clients.</dd>

      <dt>Do you take insurance?</dt>
      <dd>I do not bill insurance directly, but I can provide a superbill to help you seek reimbursement.</dd>

      <dt>Can I see you online if I don't live in Oregon?</dt>
      <dd>Online sessions are for clients who are physically located in Oregon at the time of the session.</dd>

      <dt>How can I get ahold of you?</dt>
      <dd>Through <a href="{PT}">Psychology Today</a> or at {mail()}. I typically respond within 1–2 business days.</dd>
    </dl>
    {EMAIL_NOTE}
  </div>
  <div class="home-photo">
    {fig(p, "jon-smiling.jpg", "Jonathan Scarboro laughing, sitting on the blue couch in his office.", photo=True)}
  </div>
</div>
"""
    page("fees/index.html",
         "Therapy Fees & FAQ | Jonathan Scarboro, Portland, OR",
         "Session fees, sliding scale, superbills for out-of-network reimbursement, and common questions about starting therapy with Jonathan Scarboro in Portland, OR.",
         body, current="fees/", schema=FAQ_SCHEMA)


# ---------------------------------------------------------------- Contact
def contact():
    p = "../"
    body = f"""
<div class="row gy-4 gx-lg-5">
  <div class="col-lg-7 prose">
    <h1>Book a free consultation</h1>
    <p class="lede">I offer a free 15-minute consultation to see if we're a good fit.</p>
    <p>Email me at {mail()} and we'll find a time. I typically respond within 1–2 business days. You can also reach me through <a href="{PT}">Psychology Today</a>.</p>
    {EMAIL_NOTE}
    <p>Sessions are in person at my office, {STREET}, Portland, OR 97214 (inner Southeast), or online for clients located in Oregon. <a href="{MAPS}">Get directions on Google Maps</a>.</p>
    <p class="mt-4"><a class="btn btn-ink" href="mailto:{EMAIL}?subject=Free%20consultation">Email to book a consultation</a></p>
    <div class="notice" role="note">
      <strong>If you're in crisis right now,</strong> please don't wait on email. Call or text <a href="tel:988">988</a>, or call 911. <a href="{link(p, 'crisis/')}">More crisis resources</a>.
    </div>
  </div>
  <div class="col-lg-5">
    {fig(p, "office.jpg", "Jonathan's office: a blue velvet loveseat under a window with green striped curtains, a lamp on a green filing cabinet, plants, and framed art on white walls.", "My office in inner Southeast Portland.", color="orange", photo=True)}
  </div>
</div>
"""
    page("contact/index.html",
         "Free Consultation | Therapist for Men, Portland OR",
         "Book a free 15-minute consultation with Jonathan Scarboro, a therapist in Portland, OR. In person in inner Southeast Portland or online in Oregon.",
         body, current="contact/")


# ---------------------------------------------------------------- Zine
def zine():
    p = "../"
    body = f"""
<div class="row gy-4 gx-lg-5">
  <div class="col-lg-7 prose">
    <h1>Checking the Box</h1>
    <p class="lede">A not-too woo-woo guide to unblocking your creativity using a simple checklist.</p>
    <p>Guidelines for making a simple tool to help you get unstuck and establish a creative habit with whatever you have available today.</p>
    <p>I spent about a decade in a creative block. This zine is about how I got out of it, illustrated with my own drawings. It's free, and you're welcome to share it with whomever.</p>
    <p class="mt-4"><a class="btn btn-ink" href="{ZINE_PDF}">Download the zine (PDF, about 4 MB)</a></p>
    <p class="small">An easier-to-read web version is on the way. <em>Checking the Box</em> © 2024 Jonathan E Scarboro, licensed <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>. It's not psychotherapy or medical advice.</p>
  </div>
  <div class="col-lg-5">
    {fig(p, "checklist.jpg", "Pen drawing of Jonathan's handwritten daily checklist, pinned up with a pen clipped to the top. Items include write in journal, draw or paint something, dance or sing, contact a friend, and leave one or more items unchecked.", "My actual list, as it was while I made the zine.", color="orange")}
  </div>
</div>
"""
    page("zine/index.html",
         "Checking the Box: A Free Zine on Creative Blocks",
         "A free, illustrated zine by Portland therapist Jonathan Scarboro: a not-too woo-woo guide to unblocking your creativity with a simple daily checklist.",
         body, current="zine/")


# ---------------------------------------------------------------- Crisis
def crisis():
    body = """
<div class="prose">
  <h1>If you need help right now</h1>
  <p class="lede">This website isn't crisis care, and I can't respond to emergencies by email or voicemail.</p>
  <ul>
    <li><strong>Call or text <a href="tel:988">988</a></strong> to reach the 988 Suicide &amp; Crisis Lifeline, any time. You can also chat at <a href="https://988lifeline.org">988lifeline.org</a>.</li>
    <li><strong>Call <a href="tel:911">911</a></strong> or go to the nearest emergency room if you or someone else is in immediate danger.</li>
  </ul>
</div>
"""
    page("crisis/index.html", "Crisis Resources | Jonathan Scarboro",
         "This site isn't crisis care. If you need help now, call or text 988 or call 911.", body)


# ---------------------------------------------------------------- Privacy
def privacy():
    body = f"""
<div class="prose">
  <h1>Privacy</h1>
  <p class="lede">Short version: this site doesn't track you.</p>
  <ul>
    <li>No cookies, analytics, ad pixels, or social media trackers.</li>
    <li>No forms. The site doesn't collect or store anything you type.</li>
    <li>Fonts, styles, and scripts are served from this site, not from third parties.</li>
    <li>Cloudflare hosts this site and may keep standard server logs, such as IP addresses, for security and operations. I don't use them to identify visitors.</li>
    <li>Links to Google Maps and Psychology Today take you to their sites, which have their own privacy practices. Nothing from them loads on this site.</li>
    <li>If you email me, that email is handled by my email provider. Email isn't a secure channel, so please keep it to scheduling and logistics.</li>
  </ul>
  <p>Questions? {mail()}</p>
</div>
"""
    page("privacy/index.html", "Privacy | Jonathan Scarboro",
         "This site uses no cookies, analytics, or trackers, and collects no personal information.", body)


# ---------------------------------------------------------------- Accessibility
def accessibility():
    body = f"""
<div class="prose">
  <h1>Accessibility</h1>
  <p class="lede">I want this site to work for everyone, including people who use screen readers, keyboards, or magnification.</p>
  <p>The site aims to meet the Web Content Accessibility Guidelines (WCAG) 2.1 at level AA. It's a temporary site while a new one is built, and it's tested with automated tools and keyboard navigation.</p>
  <p>Known limitation: the zine is currently only available as a PDF that isn't accessible to screen readers. A web version is in progress.</p>
  <p>If something doesn't work for you, email {mail()} and I'll get you the information another way.</p>
</div>
"""
    page("accessibility/index.html", "Accessibility | Jonathan Scarboro",
         "Accessibility statement for Jonathan Scarboro's therapy practice website.", body)


# ---------------------------------------------------------------- 404
def not_found():
    p = "/"  # served by the server at any depth: root-absolute
    body = f"""
<div class="row gy-4 gx-lg-5">
  <div class="col-lg-7 prose">
    <h1>That page isn't here.</h1>
    <p class="lede">The site's been rearranged. Try <a href="/">the home page</a>, <a href="{link(p, 'help/')}">what I help with</a>, or <a href="{link(p, 'zine/')}">the zine</a>.</p>
  </div>
  <div class="col-lg-5">
    <figure class="drawing"><picture><source srcset="/assets/img/slept-on.webp" type="image/webp"><img src="/assets/img/slept-on.jpg" width="800" height="1000" alt="Hand-lettered drawing titled Things I Have Slept On This Week: a conventional mattress, an air mattress with a hole, a majestic granite boulder, a section of carpet by the wall farthest from a suspicious stain, and a second air mattress with a smaller hole."></picture></figure>
  </div>
</div>
"""
    page("404.html", "Page Not Found | Jonathan Scarboro", "Page not found.", body, noindex=True, root="/")


if __name__ == "__main__":
    about(); help_page(); fees(); contact(); zine(); crisis(); privacy(); accessibility(); not_found()
    # Legacy URLs from the mmm.page site: real 301s via Cloudflare Pages _redirects
    # (redirects run before static assets; both slash forms listed because Pages treats them separately)
    legacy = {"/about": "/", "/main": "/", "/approach": "/help/", "/dudes": "/help/#mens-issues",
              "/blocks": "/help/#creative-blocks", "/business": "/fees/"}
    lines = [f"{src}{slash} {dst} 301" for src, dst in legacy.items() for slash in ("", "/")]
    (OUT / "_redirects").write_text("# Old jscar.care (mmm.page) paths -> new pages\n" + "\n".join(lines) + "\n")
    urls = ["", "help/", "fees/", "contact/", "zine/", "crisis/", "privacy/", "accessibility/"]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>{date.today().isoformat()}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    # Search and AI-search crawlers: everything. AI *training* crawlers: everything except the zine PDF.
    # (A crawler follows only the most specific group naming it, so these bots can still crawl all pages.)
    (OUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        "# Training crawlers may read every page, but not the full zine PDF.\n"
        + "".join(f"User-agent: {ua}\n" for ua in
                  ["GPTBot", "ClaudeBot", "CCBot", "Google-Extended", "Applebot-Extended", "meta-externalagent", "Bytespider"])
        + "Disallow: /zine/checking-the-box.pdf\n\n"
        f"Sitemap: {SITE}/sitemap.xml\n")
    # Cloudflare Pages headers: hardening + keep the PDF out of search results (noindex, not robots-blocked,
    # so search engines can actually see the instruction).
    (OUT / "_headers").write_text("""/*
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'self'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'; object-src 'none'; upgrade-insecure-requests
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  X-Frame-Options: DENY

/zine/checking-the-box.pdf
  X-Robots-Tag: noindex

/assets/*
  Cache-Control: public, max-age=604800
""")
    print("built")
