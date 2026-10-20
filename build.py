"""Build the Grindstone Ltd site.

  python3 build.py

Writes:
  docs/             the real site, served by GitHub Pages on grindstone.ltd (one page per product, sitemap, robots)
  index.html        a single-file preview with the same content (published as the Claude artifact)

Edit the page content below, then run the script; never edit docs/ or index.html by hand.
"""
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://grindstone.ltd"
EMS = "https://www.emsdirectory.co.uk/"          # canonical address of EMS Directory (apex 301s here)
DRUM = "https://drumbeat.plus/"
CONTACT = "enquiries@grindstone.ltd"
LINKEDIN = "https://www.linkedin.com/company/grindstoneltd/"
from urllib.parse import quote
DEMO_BODY = "Hi,\r\n\r\nI'd like a demo of drumbeat+.\r\n\r\nName:\r\nCompany:\r\nPhone:\r\nBest time to call:\r\n"
DEMO = "mailto:" + CONTACT + "?subject=" + quote("drumbeat+ demo request") + "&amp;body=" + quote(DEMO_BODY)
LI_EMS = "https://www.linkedin.com/company/emsdirectory/"
LI_DRUM = "https://www.linkedin.com/company/drumbeatplus/"
# LinkedIn "in" logo (Simple Icons 9.0.0, CC0)
LI_ICON = ('<svg class="li-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>')
TODAY = datetime.date.today().isoformat()

CSS = (ROOT / "src/styles.css").read_text(encoding="utf-8")
EMS_SYMBOL = (ROOT / "src/ems-mark.svg.html").read_text(encoding="utf-8")
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,600..900'
         '&family=Michroma&family=Instrument+Sans:wght@400;500;600&family=Inter:wght@700;800&family=Unbounded:wght@900&display=swap">')

EMS_WM = ('<span class="wm-ems"><svg class="ems-logo" aria-hidden="true" focusable="false"><use href="#ems-mark"/></svg>'
          '<span>EMS <b>Directory</b></span></span>')
DRUM_WM = '<span class="wm-drum">drum<span class="b">beat</span><span class="p">+</span></span>'
TM = '<span class="tm">&trade;</span>'
# 'stone' with the O drawn as the grindstone wheel (a hidden 'o' keeps the word readable to screen readers and search)
STONE = ('st<span class="o-wheel"><svg viewBox="0 0 100 100" aria-hidden="true" focusable="false"><circle cx="50" cy="50" r="44.5" fill="none" stroke="currentColor" stroke-width="11"/><circle cx="50" cy="50" r="28" fill="none" stroke="currentColor" stroke-width="8"/><circle cx="50" cy="50" r="12" fill="none" stroke="currentColor" stroke-width="7"/></svg><span class="sr">o</span></span>ne')
CONSULT_WM = ('<span class="wm-consult"><span class="cm-name">Grind<span>' + STONE + '</span></span>'
              '<span class="cm-sub">Consultancy</span></span>')

ORG = {"@type": "Organization", "name": "Grindstone Ltd", "url": SITE + "/", "sameAs": [LINKEDIN]}

# ---------------------------------------------------------------- pages
# Links inside page bodies use {home} {ems_page} {drum_page} {gemba_page}, filled in per output.

PAGES = [
    {
        "id": "home", "path": "/", "nav": "Home",
        "title": "Grindstone | Cutting-edge services for contract manufacturing",
        "description": "Grindstone runs EMS Directory, builds drumbeat+ sales and operations software, and offers hands-on consultancy for contract electronics manufacturers.",
        "jsonld": {"@context": "https://schema.org", **ORG,
                   "legalName": "Grindstone Ltd",
                   "identifier": {"@type": "PropertyValue", "propertyID": "Companies House company number", "value": "17440074"},
                   "address": {"@type": "PostalAddress", "streetAddress": "8 Aldermans Hill", "addressLocality": "Hockley",
                               "addressRegion": "Essex", "postalCode": "SS5 4RW", "addressCountry": "GB"},
                   "brand": [{"@type": "Brand", "name": "EMS Directory", "url": EMS, "sameAs": [LI_EMS]},
                             {"@type": "Brand", "name": "drumbeat+", "url": SITE + "/drumbeat/", "sameAs": [LI_DRUM]}]},
        "body": """
    <div class="home">
    <div class="wheel" aria-hidden="true"></div>
    <div class="hero">
      <div class="wrap">
        <h1><span class="nowrap">Cutting-edge</span> services for <em>contract manufacturing.</em></h1>
        <p class="lead lead-big">Sourcing, software and support for contract manufacturing, built on thirty years in sales and operations across OEMs, Tier 1s and EMS companies.</p>
      </div>
    </div>
    <div class="wrap products">
      <h2 class="sr">What Grindstone does</h2>
      <div class="cards">
        <article class="card">
          <span class="kind">Find a supplier</span>
          <h3><a href="{ems_page}">""" + EMS_WM + """</a></h3>
          <p>370+ <a href="{EMS}">UK contract electronics manufacturers</a> in one place. Compare them on capability and certification, then send one RFQ to your whole shortlist.</p>
          <div class="card-foot"><a class="more" href="{ems_page}">More about EMS Directory</a><a class="ext" href="{EMS}">emsdirectory.co.uk</a></div>
        </article>
        <article class="card">
          <span class="kind">Sales and operations</span>
          <h3><a href="{drum_page}">""" + DRUM_WM + TM + """</a></h3>
          <p><a href="{drum_page}">Sales and operations software for EMS companies</a>. It takes every job from lead to delivery, keeps it moving between departments, and runs beside the ERP you already have.</p>
          <div class="card-foot"><a class="more" href="{drum_page}">More about drumbeat+</a></div>
        </article>
        <article class="card">
          <span class="kind">Gemba support</span>
          <h3><a href="{gemba_page}" aria-label="Grindstone Consultancy">""" + CONSULT_WM + """</a></h3>
          <p>Hands-on consultancy across sales, operations and practical AI: winning the right work, new product introduction, customer approvals, and quality or supplier problems that need fixing.</p>
          <div class="card-foot"><a class="more" href="{gemba_page}">More about Grindstone Consultancy</a></div>
        </article>
      </div>
    </div>
    </div>""",
    },
    {
        "id": "ems-directory", "path": "/ems-directory/", "nav": "EMS Directory",
        "title": "EMS Directory: compare UK contract manufacturers | Grindstone",
        "description": "Compare 370+ UK contract electronics manufacturers on certification, process, test capability and "
                       "industry, then send one RFQ to your shortlist.",
        "jsonld": {"@context": "https://schema.org", "@type": "WebSite", "name": "EMS Directory", "url": EMS,
                   "description": "Directory of UK contract electronics manufacturers (EMS providers).",
                   "publisher": ORG},
        "body": """
    <div class="wrap page">
      <a class="back" href="{home}">Home</a>
      <header class="big">
        <span class="kind">Find a supplier &middot; emsdirectory.co.uk</span>
        <h1>""" + EMS_WM + """</h1>
        <p class="intro">Find the UK EMS partner that fits the job.</p>
        <p class="body"><a href="{EMS}">EMS Directory</a> lists 370+ UK contract electronics manufacturers, from prototype
          specialists to high-volume box build. Every listing uses the same layout, so you can compare suppliers like for like
          on the things that decide a project.</p>
      </header>
      <ul class="points">
        <li><strong>370+ UK EMS providers</strong><span>From PCB assembly to full box build, all in one place.</span></li>
        <li><strong>Compare like for like</strong><span>Filter by certification, process, test capability and industry.</span></li>
        <li><strong>One RFQ, your whole shortlist</strong><span>Pick the suppliers that fit and send them the same request in one go.</span></li>
        <li><strong>Checked, not just collected</strong><span>Listings are checked against company websites and Companies House. See <a href="https://www.emsdirectory.co.uk/pages/what-verified-means/">what &ldquo;verified&rdquo; means</a>.</span></li>
      </ul>
      <p class="crosslink">First time? Read <a href="https://www.emsdirectory.co.uk/pages/how-to-use-ems-directory/">how to use EMS Directory</a>.</p>
      <div class="cta-row">
        <a class="cta" href="{EMS}">Find a supplier on EMS Directory</a>
        <a class="li li-page" href="{LI_EMS}">""" + LI_ICON + """<span>Follow EMS Directory on LinkedIn</span></a>
      </div>
    </div>""",
    },
    {
        "id": "drumbeat", "path": "/drumbeat/", "nav": "drumbeat+",
        "title": "drumbeat+ sales and operations software for EMS | Grindstone",
        "description": "drumbeat+ takes every job in a contract electronics manufacturer from lead to delivery, "
                       "beside the ERP you already have.",
        "jsonld": {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "drumbeat+", "url": SITE + "/drumbeat/", "sameAs": [LI_DRUM],
                   "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
                   "description": "Sales and operations software for contract electronics manufacturers, from lead to delivery.",
                   "publisher": ORG},
        "body": """
    <div class="wrap page page-top">
      <a class="back" href="{home}">Home</a>
      <header class="big">
        <span class="kind">Sales and operations</span>
        <h1>""" + DRUM_WM + TM + """</h1>
        <p class="intro">Your ERP keeps the books. drumbeat+ keeps the beat.</p>
        <p class="body">drumbeat+&trade; is sales and operations software for contract electronics manufacturers.
          It takes each job from first enquiry through quoting, orders, materials, production, quality and despatch,
          and gives every team the right task at the right time.</p>
      </header>
    </div>
    <section class="beatband" aria-label="From enquiry to delivery">
      <div class="wrap">
        <p class="bb-eyebrow">From enquiry to delivery</p>
        <h2 class="bb-h">Every stage, on one beat.</h2>
        <div class="track">
          <div class="seg crm"><span class="seglab">crm</span><ol><li style="--i:0">Enquiry</li><li style="--i:1">RFQ and reviews</li><li style="--i:2">Quote</li></ol></div>
          <div class="seg ops"><span class="seglab">ops</span><ol><li style="--i:3">Order</li><li style="--i:4">Materials</li><li style="--i:5">Production</li><li style="--i:6">Quality</li><li style="--i:7">Delivery</li></ol></div>
        </div>
      </div>
    </section>
    <div class="wrap page page-cont">
      <ul class="points">
        <li><strong>Built for EMS</strong><span>Follows a job the way an electronics manufacturer actually runs one.</span></li>
        <li><strong>Beside your ERP</strong><span>Works alongside the ERP you already have, rather than replacing it.</span></li>
        <li><strong>Right task, right time</strong><span>Everyone sees what needs doing today, so jobs keep moving without chasing.</span></li>
        <li><strong>Your customers can see it</strong><span>A live link shows each customer where their orders are.</span></li>
      </ul>
      <h2 class="sub-h">Four plans, one platform</h2>
      <ul class="plans">
        <li><span class="wm-drum">drum<span class="b">beat</span><span class="p">+</span><span class="pl">crm</span></span><span>Win the work.</span></li>
        <li><span class="wm-drum">drum<span class="b">beat</span><span class="p">+</span><span class="pl">ops</span></span><span>Deliver on time.</span></li>
        <li><span class="wm-drum">drum<span class="b">beat</span><span class="p">+</span><span class="pl">opx</span></span><span>Operational excellence.</span></li>
        <li><span class="wm-drum">drum<span class="b">beat</span><span class="p">+</span><span class="pl">max</span></span><span>Built for AS9100, ISO 13485 and IATF 16949.</span></li>
      </ul>
      <div class="cta-row">
        <a class="cta" href="{DEMO}">Request a demo</a>
        <a class="li li-page" href="{LI_DRUM}">""" + LI_ICON + """<span>Follow drumbeat+ on LinkedIn</span></a>
      </div>
    </div>""",
    },
    {
        "id": "consultancy", "path": "/consultancy/", "nav": "Consultancy",
        "title": "Electronics manufacturing consultancy | Grindstone",
        "description": "Hands-on consultancy for OEMs and contract electronics manufacturers: sales and marketing, NPI, quality approvals, supplier selection and practical AI.",
        "jsonld": {"@context": "https://schema.org", "@type": "Service", "name": "Grindstone Consultancy",
                   "serviceType": "Sales, marketing, operations, quality, engineering and practical AI consultancy for electronics manufacturing",
                   "provider": ORG, "areaServed": {"@type": "Country", "name": "United Kingdom"}},
        "body": """
    <div class="wrap page">
      <a class="back" href="{home}">Home</a>
      <header class="big">
        <span class="kind">Consultancy</span>
        <h1 aria-label="Grindstone Consultancy">""" + CONSULT_WM + """</h1>
        <p class="intro">Hands-on consultancy for electronics manufacturing.</p>
        <p class="body">We work with OEMs and contract manufacturers to get new products into production,
          win customer approval, and get to the root of quality and supplier problems. For contract manufacturers, we also
          help win more of the right work, and we help both put AI to practical use. You get thirty years of sales and operations experience, working alongside your team.</p>
      </header>

      <h2 class="sub-h">Who we work with</h2>
      <ul class="points">
        <li><strong>Contract manufacturers</strong><span>Extra experience for winning new customers, a busy NPI, a demanding customer approval, or a quality problem that keeps coming back.</span></li>
        <li><strong>OEMs and buyers</strong><span>Someone independent on site with your supplier, whether they're down the road or you're overseas.</span></li>
      </ul>

      <h2 class="sub-h">What we can help with</h2>
      <div class="stages">
        <div class="stage stage-wide">
          <span class="kind">Sales and marketing</span>
          <ul>
            <li>Sales strategy<span>Pick the right markets and build a pipeline of customers who fit.</span></li>
            <li>RFQ and quoting<span>Faster, more consistent quotes that win more of the right work.</span></li>
            <li>Key account management<span>Grow and keep your most important customers.</span></li>
            <li>Pricing and margin<span>Quoting models that protect your margin.</span></li>
            <li>Sales process and CRM<span>Track every lead and quote, so none go cold.</span></li>
            <li>Positioning and messaging<span>Know what makes you different, and say it clearly.</span></li>
            <li>Website and sales collateral<span>Capability decks, case studies and website copy.</span></li>
            <li>Trade shows and outreach<span>Plan events, follow up properly and run campaigns.</span></li>
          </ul>
        </div>
        <div class="stage">
          <span class="kind">Into production</span>
          <ul>
            <li>New product introduction<span>From design release to stable production.</span></li>
            <li>DFM / DFA reviews<span>Catch build problems before the first build.</span></li>
            <li>Process validation<span>Show the process is capable and repeatable.</span></li>
            <li>ECN / ECO implementation<span>Engineering changes cut in cleanly.</span></li>
          </ul>
        </div>
        <div class="stage">
          <span class="kind">Quality and approval</span>
          <ul>
            <li>APQP and PPAP<span>Plan for quality and get the customer's sign-off.</span></li>
            <li>PFMEA<span>Find where the process can fail, before it does.</span></li>
            <li>First article inspection<span>Check the first build against every requirement.</span></li>
            <li>8D root cause and corrective action<span>Find the real cause and stop it coming back.</span></li>
          </ul>
        </div>
        <div class="stage">
          <span class="kind">Suppliers and capacity</span>
          <ul>
            <li>Supplier selection<span>Find and qualify the right manufacturing partner.</span></li>
            <li>Run at rate<span>Prove the line can build at the volume quoted.</span></li>
            <li>Project delivery<span>From kick-off to steady production.</span></li>
          </ul>
        </div>
        <div class="stage stage-wide">
          <span class="kind">Practical AI</span>
          <ul>
            <li>RFQ and BOM handling<span>Read customer BOMs and drawings, clean up part data and quote faster.</span></li>
            <li>Sales and admin automation<span>Draft RFQ replies, chasers, meeting notes and CRM updates.</span></li>
            <li>Documents and quality<span>Draft work instructions, 8D reports, procedures and audit prep in less time.</span></li>
            <li>Data and reporting<span>Get answers out of your ERP exports, without new software.</span></li>
            <li>Getting started safely<span>Which tools to use, what's safe to share, and guidance for your team.</span></li>
          </ul>
        </div>
      </div>

      <div class="experience">
        <p class="big-figure">30 <span>years</span></p>
        <p>Sales and operations across OEMs, Tier 1 suppliers and contract manufacturers, including senior roles at global
          companies. Low-volume, high-mix through to high-volume, in regulated and safety-critical industries.</p>
      </div>

      <h2 class="sub-h">How we work</h2>
      <p class="cycle-intro">We follow DMAIC, the Six Sigma method used across manufacturing.</p>
      <ol class="dmaic">
        <li style="--i:0"><span class="node">D</span><strong>Define</strong><span class="txt">The problem, the scope and a fixed price.</span></li>
        <li style="--i:1"><span class="node">M</span><strong>Measure</strong><span class="txt">How things run today, from your data and the shop floor.</span></li>
        <li style="--i:2"><span class="node">A</span><strong>Analyse</strong><span class="txt">Find the real cause.</span></li>
        <li style="--i:3"><span class="node">I</span><strong>Improve</strong><span class="txt">Put the fix in, with your team.</span></li>
        <li style="--i:4"><span class="node">C</span><strong>Control</strong><span class="txt">Make sure it stays fixed, with a written report your team keeps.</span></li>
      </ol>

      <div class="contact">
        <strong>Tell us what you need</strong>
        <span class="addr">""" + CONTACT + """</span>
      </div>
      <a class="li li-page" href="{LINKEDIN}">""" + LI_ICON + """<span>Follow Grindstone on LinkedIn</span></a>
      <p class="crosslink">Still looking for a supplier? Compare 370+ <a href="{EMS}">UK contract electronics manufacturers</a> on EMS Directory.</p>
    </div>""",
    },
]

# Large faint brand watermark behind each sub page (the home page has its own wheel in the hero)
MARKS = {
    "ems-directory": '<div class="wm-bg mark-ems" aria-hidden="true"><svg><use href="#ems-mark"/></svg></div>',
    "drumbeat": '<div class="wm-bg mark-drum" aria-hidden="true">+</div>',
    "consultancy": '<div class="wm-bg wheel" aria-hidden="true"></div>',
}


def page_body(p, links):
    body = fill(p["body"], links)
    mark = MARKS.get(p["id"])
    return f'<div class="pagewrap">{mark}{body}\n</div>' if mark else body


FOOTER = """
<footer>
  <div class="wrap">
    <nav aria-label="Our sites">
      <a href="{EMS}">EMS Directory</a>
      <a href="{drum_page}">drumbeat+</a>
      <a href="{gemba_page}">Grindstone Consultancy</a>
      <span class="foot-mail">""" + CONTACT + """</span>
      <a class="li" href="{LINKEDIN}">""" + LI_ICON + """<span>LinkedIn</span></a>
    </nav>
    <p class="legal">Grindstone Ltd &middot; Registered in England and Wales, company no. 17440074 &middot; Registered office: 8 Aldermans Hill, Hockley, Essex SS5 4RW</p>
  </div>
</footer>"""


def header(links, current):
    items = "\n".join(
        f'      <a href="{links[p["id"]]}" data-nav="{p["id"]}"'
        + (' aria-current="page"' if p["id"] == current else "") + f'>{p["nav"]}</a>'
        for p in PAGES)
    return f"""
<div class="top">
  <div class="wrap">
    <a class="mark" href="{links['home']}">Grind<span>{STONE}</span></a>
    <nav aria-label="Main">
{items}
    </nav>
  </div>
</div>"""


def fill(text, links):
    return (text.replace("{home}", links["home"]).replace("{ems_page}", links["ems-directory"])
            .replace("{drum_page}", links["drumbeat"]).replace("{gemba_page}", links["consultancy"])
            .replace("{EMS}", EMS).replace("{DRUM}", DRUM).replace("{LINKEDIN}", LINKEDIN).replace("{LI_EMS}", LI_EMS).replace("{LI_DRUM}", LI_DRUM).replace("{DEMO}", DEMO))


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=True) + "</script>"


# ---------------------------------------------------------------- real site (dist/)

def build_dist():
    links = {p["id"]: p["path"] for p in PAGES}
    out = ROOT / "docs"
    for p in PAGES:
        url = SITE + p["path"]
        html = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['title']}</title>
<meta name="description" content="{p['description']}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Grindstone Ltd">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['description']}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_GB">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Grindstone: cutting-edge services for contract manufacturing">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{p['title']}">
<meta name="twitter:description" content="{p['description']}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{FONTS}
<style>
{CSS}
</style>
{jsonld(p['jsonld'])}
</head>
<body>
{EMS_SYMBOL}
{header(links, p['id'])}
<main>
{page_body(p, links)}
</main>
{fill(FOOTER, links)}
</body>
</html>
"""
        target = out / p["path"].strip("/") / "index.html" if p["path"] != "/" else out / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
    urls = "\n".join(f"  <url><loc>{SITE}{p['path']}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES)
    (out / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8")
    # favicon: the grindstone wheel from the logo
    import shutil
    for icon in (ROOT / "src/icons").iterdir():
        shutil.copy(icon, out / icon.name)
    (out / "CNAME").write_text("grindstone.ltd\n", encoding="utf-8")   # GitHub Pages custom domain
    (out / ".nojekyll").write_text("", encoding="utf-8")                   # serve files as they are
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


# ---------------------------------------------------------------- single-file preview (Claude artifact)

def build_preview():
    links = {p["id"]: "#" + p["id"] for p in PAGES}
    sections = "\n".join(
        f'  <section data-page="{p["id"]}"' + ("" if p["id"] == "home" else " hidden") + f'>{page_body(p, links)}\n  </section>'
        for p in PAGES)
    ids = json.dumps([p["id"] for p in PAGES])
    html = f"""<title>Grindstone Ltd</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{PAGES[0]['description']}">
{FONTS}
<style>
{CSS}
</style>

{EMS_SYMBOL}
{header(links, 'home')}
<main>
{sections}
</main>
{fill(FOOTER, links)}

<script>
  (function () {{
    var pages = {ids};
    function show() {{
      var id = (location.hash || '#home').slice(1);
      if (pages.indexOf(id) < 0) id = 'home';
      document.querySelectorAll('[data-page]').forEach(function (s) {{ s.hidden = s.getAttribute('data-page') !== id; }});
      document.querySelectorAll('[data-nav]').forEach(function (a) {{
        if (a.getAttribute('data-nav') === id) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
      }});
      window.scrollTo(0, 0);
    }}
    window.addEventListener('hashchange', show);
    show();
  }})();
</script>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build_dist()
    build_preview()
    print("Built docs/ (" + ", ".join(p["path"] for p in PAGES) + ") and index.html preview")
