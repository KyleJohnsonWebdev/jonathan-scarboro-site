#!/usr/bin/env python3
"""Builds the stopgap site (maletherapistinportland.com) into ./site. Plain static HTML output."""
import json
from datetime import date
from pathlib import Path

OUT = Path(__file__).parent / "docs"   # the published folder; build files stay outside it
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
            "knowsAbout": ["Gestalt therapy", "Mentalization-Based Narrative Exposure Therapy (MBNET)", "Trauma therapy", "Men's issues", "Creative blocks"],
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
            "founder": {"@id": PERSON_ID},
        },
    ],
}

# FAQ on /fees/ (Jon's copy, Oct 2026). One source of truth: the page renders the HTML answers and the
# FAQPage markup uses the same text with tags stripped, so the two can't drift apart (markup must match the page).
# Google stopped showing FAQ rich results in 2026; kept because it's valid and other engines and AI tools read it.
import re as _re, html as _html
PT_LINK = f'<a href="{PT}">Psychology Today</a>'
MAIL_LINK = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
FAQ = [
    ("When are you available?",
     "I see clients Tuesday through Thursday, with session start times between 9:00 am and 6:30 pm, and Friday between 9:00 am and noon."),
    ("How often do we meet?",
     "We usually start with weekly sessions. As things progress, we might shift to every other week, monthly, or meet as needed, depending on what makes sense for you and the work we're doing."),
    ("How long does therapy take?",
     "It depends on what brings you to therapy and what you're looking for. Most of my working relationships last somewhere around a year to a year and a half. Sometimes we focus on a specific issue over three or four months; other times, people find value in continuing to work together for years. There's no preset timeline. We'll keep checking in about what you're getting out of therapy and what makes sense going forward."),
    ("Do you offer a consultation?",
     f"Yep. I offer a free 20–30-minute consultation so we can get a feel for each other and see if working together makes sense. You can reach me through {PT_LINK} or email me at {MAIL_LINK}."),
    ("Do you work only with men?",
     "I specialize in working with men because I've seen a real need for therapists who understand the particular ways men can struggle with relationships, emotions, and the expectations placed on them. I also enjoy working with women, femme, trans, and nonbinary folks. You don't need to fit neatly into any particular box for us to work well together."),
    ("Do you take insurance?",
     "I'm an out-of-network provider, so I don't bill insurance directly. I can provide a superbill for you to submit to your insurance company. Whether they'll reimburse you, and how much, depends on your plan, so it's worth checking with them first."),
    ("How can I get ahold of you?",
     f"You can reach me through {PT_LINK} or email me at {MAIL_LINK}. I typically respond within one to two business days."),
]
_plain = lambda s: _html.unescape(_re.sub(r"<[^>]+>", "", s))
FAQ_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}}
        for q, a in FAQ
    ],
}
_dl = lambda items: "".join(f"      <div><dt>{q}</dt>\n      <dd>{a}</dd></div>\n" for q, a in items)
FAQ_HTML = _dl(FAQ)

# Availability: one switch. Set to False when Jon is full; every "accepting new clients" line disappears.
ACCEPTING_NEW_CLIENTS = True
def accepting(cls=""):
    if not ACCEPTING_NEW_CLIENTS:
        return ""
    return f'<p class="accepting {cls}"><span class="accepting-dot" aria-hidden="true"></span>Currently accepting new clients</p>'

EMAIL_NOTE = (
    '<p class="small">Heads up: email isn\'t a secure way to send private information. '
    "Keep it to scheduling and logistics, and save the details for when we talk.</p>"
)


def mail(text=None):
    return f'<a href="mailto:{EMAIL}">{text or EMAIL}</a>'


def fig(p, src, alt, caption=None, cls="", color="green", photo=False, lazy=False):
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
            f'<img src="{p}assets/img/{src}" alt="{alt}" width="{w}" height="{h}" decoding="async"{' loading="lazy"' if lazy else ''}>'
            f'</picture>{cap}</figure>')


def portrait(p, name, alt):
    """Art-directed photo: the large cutout from 992px up; below that a 240px circle crop (shown at ~104px),
    so phones and tablets download a small file and the text starts near the top of the screen."""
    from PIL import Image
    w, h = Image.open(OUT / "assets/img" / f"{name}.jpg").size
    small = '(max-width: 991.98px)'
    return (f'<figure class="portrait"><picture>'
            f'<source media="{small}" srcset="{p}assets/img/{name}-avatar.webp" type="image/webp" width="240" height="240">'
            f'<source media="{small}" srcset="{p}assets/img/{name}-avatar.jpg" width="240" height="240">'
            f'<source srcset="{p}assets/img/{name}.webp" type="image/webp">'
            f'<img src="{p}assets/img/{name}.jpg" alt="{alt}" width="{w}" height="{h}" decoding="async">'
            f'</picture></figure>')


def link(p, target):
    """Link to a page folder, relative to the current page: 'help/' -> '../help/index.html'.
    On a server that serves / for index.html (Cloudflare) these redirect to the clean URL."""
    if p == "/":                                   # 404 page: served at any depth, so root-absolute clean URLs
        return "/" if target in ("./", "") else "/" + target
    base = "" if target in ("./", "") else target
    return f"{p}{base}index.html"


def page(path, title, desc, body, current=None, noindex=False, schema=None, root=None, theme=None):
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
<link rel="preload" href="{p}assets/fonts/familjen-grotesk-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/bootstrap.purged.css">
<link rel="stylesheet" href="{p}assets/css/site.css">
{ld}
</head>
<body{f' class="theme-{theme}"' if theme else ""}>
<a class="skip-link" href="#main">Skip to main content</a>
<section class="crisis-bar" aria-label="Crisis support">
  <div class="container"><span class="cb-long">In crisis? Call or text <a href="tel:988">988</a>, or call 911. This site isn't crisis care. <a href="{link(p, "crisis/")}">More on getting help now</a></span><span class="cb-short">Not crisis care · Call or text <a href="tel:988">988</a> · <a href="{link(p, "crisis/")}">Get help</a></span></div>
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
<script src="{p}assets/js/site.js" defer></script>
</body>
</html>
"""
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html)


# ---------------------------------------------------------------- About (home)
def about():
    p = ""
    # Jon's copy (Oct 2026), laid out as stacked sections so nothing interleaves on phones:
    # 1 Who I am (text + photo) · 2 Why do therapy? with the At a glance card beside it on desktop (sticky) and
    # just before it on phones; the card ends in the consultation call to action · 3 his closing line + button.
    body = f"""
<div class="spread sections">
  <section class="sec sec-intro" aria-labelledby="page-title">
    <h1 id="page-title" class="sec-h1">Who I am as a person and therapist</h1>
    <div class="sec-photo">{portrait(p, "jon-portrait", "Jonathan Scarboro sitting on a blue velvet couch in his office, leaning forward with his hands clasped.")}</div>
    <div class="sec-text">
      <p class="lede">When I'm looking at therapist websites and profiles myself, I find it very hard to know which ones I'll vibe with, which ones are skilled, and which ones are poor fits and/or kooks. So I'll try to say who I am and what I do in plain language.</p>
      <p><span class="lead-in">I came of age in punk and skateboard culture in the '90s, got an art degree, and had a first career as a bicycle mechanic and shop owner.</span> I love drawing and making things. I'm squarely middle-aged, queer, and a later-in-life parent. Although I don't talk much about myself in session, my life outside therapy influences my values and how I'll show up with you.</p>
      <p>If you come to see me, I won't try to "fix" you or correct you, and I'm not going to hand you a stack of worksheets or tell you how to live your life. I will help you stop organizing your life around fear, shame, and habits. And if your old tools are dull, I'll help you build sharp new ones. We'll probably work well together if you value humor, honesty, and a straightforward, <span class="nowrap">no-BS</span> approach to growth.</p>
    </div>
  </section>

  <div class="sec sec-story-wrap">
    <section class="glance-card" aria-labelledby="glance-title">
      <h2 id="glance-title" class="visually-hidden">At a glance</h2>
      <dl class="glance-list">
        <div><dt>Who</dt><dd>Specializing in men; I also enjoy working with women, femme, trans, and nonbinary folks</dd></div>
        <div><dt>Approach</dt><dd>Gestalt therapy and MBNET for trauma</dd></div>
        <div><dt>Where</dt><dd>In person at {STREET} in inner Southeast Portland, or online for clients in Oregon</dd></div>
        <div><dt>When</dt><dd>Tuesday through Thursday, plus Friday mornings</dd></div>
        <div><dt>Fee</dt><dd>$140 per 55-minute session, limited sliding scale</dd></div>
        <div><dt>Credentials</dt><dd>Licensed Professional Counselor (Oregon {LICENSE}), MS in Clinical Mental Health Counseling (Portland State), NCC</dd></div>
      </dl>
      <div class="glance-cta">
        <h3 class="glance-cta-heading">First step</h3>
        <p class="glance-cta-text">A free 20–30-minute consultation so we can get a feel for each other.</p>
        <a class="btn btn-ink btn-block" href="{link(p, 'contact/')}">Book a free consultation</a>
        {accepting("accepting--center")}
      </div>
    </section>

    <section class="sec-story" aria-labelledby="why-therapy">
      <h2 id="why-therapy">Why do therapy?</h2>
      <p>Fair question. As I practice it, therapy is slow, expensive, and often painful. And, of course, there's no guarantee it'll help. So why bother? Why not just keep doing what you're doing?</p>
      <p>What I have to say in reply is more of a story than an answer.</p>
      <p>I was in my early thirties, running a small but successful bicycle shop with a friend. I'd just gotten married and was living on a beautiful half-acre in the city, with a small halfpipe in the barn out back. I had dogs. From the outside, things were going well. More than that, I'd built a life that was uniquely mine. I hadn't followed anyone else's script; I'd made it myself.</p>
      <p>But things were getting weird. I didn't know how to talk to my then-wife or business partner when something wasn't working for me. I felt increasingly off and trapped by the circumstances of the life I'd built. Instead of dealing with the problems I was having with them, I found ways to ignore them: working harder, keeping to myself, drinking, and so on.</p>
      <p>I finally went to therapy after my marriage and business took a crash landing. My therapist helped me talk about things I'd rather have forgotten and get to know parts of myself it would have been convenient not to know about. I had to confront who I actually was, rather than the person I'd constructed out of other people's ideas for me and about me.</p>
      <p>It's been more than a decade since I finally decided to talk to someone about what was going on inside. It remains one of the most important decisions I've made for myself.</p>
    </section>
  </div>

  <div class="spread-close close-wide">
    <p class="close-line">I can't promise it'll be worth it for you. But if you're curious about what might change when you stop trying to figure everything out on your own, that's a good place to start.</p>
    <p class="mt-4 mb-0"><a class="btn btn-ink" href="{link(p, 'contact/')}">Book a free consultation</a></p>
  </div>

  <section class="sec zine-card" aria-labelledby="zine-card-title">
    {fig(p, "checklist.jpg", "", cls="zine-card-art", lazy=True)}
    <div class="zine-card-text">
      <p class="zine-card-label">From my zine</p>
      <h2 id="zine-card-title" class="zine-card-title"><a href="{link(p, 'zine/')}">Checking the Box</a></h2>
      <p class="mb-0">A not-too woo-woo guide to unblocking your creativity using a simple checklist.</p>
    </div>
  </section>
</div>
"""
    page("index.html",
         "Male Therapist in Portland, OR | Jonathan Scarboro, LPC",
         "Gestalt therapist in Portland, OR working mostly with men: burnout, relationships, habits, and trauma. In person in SE Portland or online in Oregon.",
         body, current="./", schema=HOME_SCHEMA, theme="coral")


# ---------------------------------------------------------------- What I help with
def help_page():
    p = "../"
    # Jon's copy (Oct 2026): "What I help with" + "How I do therapy", as stacked sections. His last paragraph is split
    # (no words changed): its last sentence is the page's closing line, matching Home (pending Jon's OK).
    body = f"""
<div class="spread sections">
  <section class="sec sec-intro" aria-labelledby="page-title">
    <h1 id="page-title" class="sec-h1">What I help with</h1>
    <div class="sec-photo">{portrait(p, "jon-seated", "Jonathan Scarboro sitting on a step in his office, one boot up, next to a stack of books.")}</div>
    <div class="sec-text">
      <p class="lede">Many of the folks I work with are pretty good at keeping their shit together. They show up for work, take care of their responsibilities, and generally manage to get by. But underneath, something isn't working.</p>
      <p>Maybe you're burned out, unhappy in a relationship, or unsure what you actually want. Maybe you've built a life that looks fine on paper but doesn't feel much like yours. You might spend more time than you'd like distracting yourself or thinking about making changes than actually making them.</p>
      <p><span class="lead-in">I help people get unstuck when the way they're living isn't working anymore.</span> That might mean learning to deal with conflict instead of avoiding it, figuring out what you feel and want instead of defaulting to what other people expect, or understanding why you keep reaching for the same habits even when they're making you miserable or numbing you out.</p>
      <p>I also work with trauma, especially when past experiences continue to shape how you see yourself and relate to other people. Often, the ways we learned to get by made sense at the time. The trouble is when we keep relying on them long after they've stopped working.</p>
      <p>You don't need to be falling apart to come to therapy. You might just be tired of going through the motions and ready to do something about it. You don't have to know exactly what needs to change, either. Wherever you are and whatever you're dealing with, we can start right there.</p>
    </div>
  </section>

  <section class="sec spread-row" aria-labelledby="how-i-do-therapy">
    <div class="spread-row-main">
      <h2 id="how-i-do-therapy">How I do therapy</h2>
      <p><span class="lead-in">I draw most on Gestalt therapy, which, unless you geek out on therapy theory like I do, may not mean much to you.</span> In Gestalt, we pay attention to what's happening right here, right now: what you feel in your body, how you’re making sense of your experience, and how you relate to other people, including me. We slow things way down and get closer to what your attention is actually with from moment to moment. Sometimes we run an experiment to see what happens when you do something differently or pay attention to something you'd usually gloss over. This helps us spot patterns you might not see on your own and figure out how some of the ways you've learned to cope might be keeping you stuck.</p>
      <p>I also use Mentalization-Based Narrative Exposure Therapy (MBNET), a trauma-focused approach that helps you make sense of painful experiences and how they continue to shape your life. We revisit what happened, pay attention to the feelings and beliefs you developed around it, and get curious about how you came to understand yourself and other people in the process. The aim is to put the past in context, so you have more freedom in how you respond to what's happening now.</p>
      <p>I'll be direct with you, challenge you when it seems useful, and take your experience seriously. We'll work together to see you more clearly, face what you've been avoiding, and have more say in how you live.</p>
    </div>
    <div class="spread-row-side">
      {fig(p, "books.jpg", "Pen drawing of a stack of books: The Courage to Create, The Power of Fun, Free Play, The Denial of Death, Make Your Art No Matter What, The Creative Act, Atomic Habits, The Artist's Way, and Gestalt Therapy on the bottom.", "Books that were on my mind or on my desk while I made my zine.", lazy=True)}
    </div>
  </section>

  <div class="spread-close close-wide">
    <p class="close-line">Rather than just talking about your problems or trying to think your way through them, the aim is to help you encounter yourself and your life in a way that feels fresh.</p>
    <p class="mt-4 mb-0"><a class="btn btn-ink" href="{link(p, 'contact/')}">Book a free consultation</a></p>
  </div>
</div>
"""
    page("help/index.html",
         "What I Help With: Gestalt & Trauma Therapy, Portland OR",
         "Therapy in Portland, OR for burnout, relationship trouble, stuck habits, and trauma, using Gestalt therapy and MBNET. In person or online in Oregon.",
         body, current="help/", theme="turquoise")


# ---------------------------------------------------------------- Fees + FAQ
def fees():
    p = "../"
    # Jon's copy (Oct 2026): "When, Where & the Rest", as stacked sections: intro with Fees beside the photo, his seven
    # questions (two columns on desktop), then the Good Faith Estimate notice (required, not his copy) at the bottom.
    # The Fees box links down to it so it stays easy to find ("prominently displayed": 45 CFR 149.610).
    body = f"""
<div class="spread sections">
  <section class="sec sec-intro" aria-labelledby="page-title">
    <h1 id="page-title" class="sec-h1">When, Where &amp; the Rest</h1>
    <div class="sec-photo">{portrait(p, "jon-smiling", "Jonathan Scarboro laughing, sitting on the blue couch in his office.")}</div>
    <div class="sec-text">
      <p class="lede">I have a limited number of openings and am currently accepting new clients. I see people in person at my office in inner Southeast Portland and online throughout Oregon. I generally prefer working in person when possible, but online sessions are available if that works better for you.</p>
      <section class="fees-block" aria-labelledby="fees">
        <div class="at-a-glance">
          <h2 id="fees" class="side-heading">Fees</h2>
          <ul class="side-list">
            <li><strong>55-minute session: $140</strong></li>
            <li>Sliding scale: I have a limited number of reduced-fee spots available.</li>
          </ul>
          <p class="fees-gfe-link"><a href="#gfe" data-open-details="gfe-details">Your right to a Good Faith Estimate</a></p>
        </div>
      </section>
    </div>
  </section>

  <section class="sec sec-faq" aria-labelledby="faq">
    <h2 id="faq" class="visually-hidden">Questions</h2>
    <dl class="faq faq-grid">
{FAQ_HTML}    </dl>
    {EMAIL_NOTE}
  </section>

  <section class="sec sec-gfe" id="gfe" aria-labelledby="gfe-title">
    <!-- Good Faith Estimate notice (45 CFR 149.610: "prominently displayed" on the website). The right itself stays
         visible; the details expand. <details> is native HTML: keyboard accessible, no JavaScript, and the collapsed
         text is still in the page for search engines. Structure and timing follow the CMS standard notice. -->
    <div class="fine-print" role="note" aria-labelledby="gfe-title">
      <h2 id="gfe-title">Your right to a Good Faith Estimate</h2>
      <p>If you don't have insurance or aren't using it, you have the right to a Good Faith Estimate explaining how much your care will cost (federal No Surprises Act).</p>
      <details class="expand" id="gfe-details">
        <summary>How it works</summary>
        <ul>
          <li>You can ask for an estimate at any time. If you ask before scheduling, you'll get it in writing within 3 business days.</li>
          <li>If you schedule at least 3 business days ahead, you'll get it within 1 business day of scheduling.</li>
          <li>If you schedule at least 10 business days ahead, you'll get it within 3 business days of scheduling.</li>
          <li>If your bill is at least $400 more than your estimate, you can dispute the bill.</li>
          <li>Keep a copy or photo of your estimate.</li>
        </ul>
        <p class="mb-0">Questions? Visit <a href="https://www.cms.gov/nosurprises/consumers">cms.gov/nosurprises/consumers</a> or call 1-800-985-3059.</p>
      </details>
    </div>
  </section>

  <div class="spread-close">
    <p class="mb-0"><a class="btn btn-ink" href="{link(p, 'contact/')}">Book a free consultation</a></p>
  </div>
</div>
"""
    page("fees/index.html",
         "Hours, Fees & FAQ | Jonathan Scarboro, Portland, OR",
         "Hours, $140 sessions, a limited sliding scale, superbills for out-of-network reimbursement, and common questions about therapy with Jonathan Scarboro.",
         body, current="fees/", schema=FAQ_SCHEMA, theme="lime")


# ---------------------------------------------------------------- Contact
def contact():
    p = "../"
    # Section pattern (Oct 2026): intro beside the office photo, then the ways to reach him as separate items.
    # Hours reuse Jon's FAQ answer word for word; response time uses his wording.
    body = f"""
<div class="spread sections">
  <section class="sec sec-intro sec-intro--wide-photo" aria-labelledby="page-title">
    <h1 id="page-title" class="sec-h1">Book a free consultation</h1>
    <div class="sec-photo">{fig(p, "office.jpg", "Jonathan's office: a blue velvet loveseat under a window with green striped curtains, a lamp on a green filing cabinet, plants, and framed art on white walls.", "My office in inner Southeast Portland.", photo=True)}</div>
    <div class="sec-text">
      <p class="lede">I offer a free 20–30-minute consultation so we can get a feel for each other and see if working together makes sense.</p>
      <p class="mt-4 mb-2"><a class="btn btn-ink" href="mailto:{EMAIL}?subject=Free%20consultation">Email to book a consultation</a></p>
      {accepting()}
    </div>
  </section>

  <!-- DRAFT copy (Claude, Oct 2026), in Jon's register; pending his OK. Steps 2-3 reuse his own wording. -->
  <section class="sec steps" aria-labelledby="steps-title">
    <h2 id="steps-title" class="steps-title">How the consultation works</h2>
    <ol class="steps-list">
      <li><span class="step-head">You reach out.</span> Email me or send a message through Psychology Today. A line or two is plenty.</li>
      <li><span class="step-head">We find a time.</span> I typically respond within one to two business days.</li>
      <li><span class="step-head">We talk for 20–30 minutes.</span> Free, so we can get a feel for each other and see if working together makes sense.</li>
    </ol>
  </section>

  <section class="sec contact-options" aria-label="Ways to reach me">
    <div class="contact-option">
      <h2 class="option-heading">Email</h2>
      <p>Email me at {mail()} and we'll find a time. I typically respond within one to two business days.</p>
      {EMAIL_NOTE}
    </div>
    <div class="contact-option">
      <h2 class="option-heading">Psychology Today</h2>
      <p class="mb-0">You can also reach me through <a href="{PT}">Psychology Today</a>.</p>
    </div>
    <div class="contact-option">
      <h2 class="option-heading">Office</h2>
      <p class="mb-0">{STREET}, Portland, OR 97214 (inner Southeast), or online for clients located in Oregon. <a href="{MAPS}">Get directions on Google Maps</a>.</p>
    </div>
    <div class="contact-option">
      <h2 class="option-heading">Hours</h2>
      <p class="mb-0">{FAQ[0][1]}</p>
    </div>
  </section>

  <div class="sec notice" role="note">
    <strong>If you're in crisis right now,</strong> please don't wait on email. Call or text <a href="tel:988">988</a>, or call 911. <a href="{link(p, 'crisis/')}">More crisis resources</a>.
  </div>
</div>
"""
    page("contact/index.html",
         "Free Consultation | Therapist for Men, Portland OR",
         "Book a free 20–30-minute consultation with Jonathan Scarboro, a therapist in Portland, OR. In person in inner Southeast Portland or online in Oregon.",
         body, current="contact/")


# ---------------------------------------------------------------- Zine
def zine():
    p = "../"
    body = f"""
<div class="spread">
  <div class="spread-open">
    <h1 class="spread-h1">Checking the Box</h1>
    <p class="lede spread-lede">A not-too woo-woo guide to unblocking your creativity using a simple checklist.</p>
    <div class="spread-aside">
      <div class="spread-photo">{fig(p, "checklist.jpg", "Pen drawing of Jonathan's handwritten daily checklist, pinned up with a pen clipped to the top. Items include write in journal, draw or paint something, dance or sing, contact a friend, and leave one or more items unchecked.", "My actual list, as it was while I made the zine.")}</div>
    </div>
    <div class="spread-main">
      <p>As I mentioned, I love to draw and make things. But for about ten years, I felt pretty stuck and struggled to do much of either. I eventually found my way out of that block with a simple daily habit tracker, which became less about checking off boxes and more about reorganizing my life around doing what I loved, a little at a time. I wrote a longform zine about the whole experience. You can <a href="{ZINE_PDF}">download it here</a>.</p>
      <p class="mt-4"><a class="btn btn-ink" href="{ZINE_PDF}">Download the zine (PDF, about 4 MB)</a></p>
      <p class="small">An easier-to-read web version is on the way. <em>Checking the Box</em> © 2024 Jonathan E Scarboro, licensed <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>. It's not psychotherapy or medical advice.</p>
    </div>
  </div>

  <section class="sec meet-card" aria-labelledby="meet-title">
    <img class="meet-avatar" src="{p}assets/img/jon-portrait-avatar.jpg" alt="" width="240" height="240" decoding="async" loading="lazy">
    <div class="meet-text">
      <p class="meet-label">About the author</p>
      <h2 id="meet-title" class="meet-title"><a href="{link(p, './')}">Who I am as a person and therapist</a></h2>
    </div>
    <p class="meet-cta mb-0"><a class="btn btn-ink" href="{link(p, 'contact/')}">Book a free consultation</a></p>
  </section>
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
  <div class="crisis-actions">
    <a class="btn btn-crisis" href="tel:988">Call&nbsp;988</a>
    <a class="btn btn-crisis" href="sms:988">Text&nbsp;988</a>
    <a class="btn btn-crisis" href="tel:911">Call&nbsp;911</a>
  </div>
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
    legacy = {"/about": "/", "/main": "/", "/approach": "/help/", "/dudes": "/help/",
              "/blocks": "/zine/", "/business": "/fees/"}
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
