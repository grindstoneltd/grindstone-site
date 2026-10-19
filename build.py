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
CONTACT = "colin@grindstone.ltd"
TODAY = datetime.date.today().isoformat()

CSS = (ROOT / "src/styles.css").read_text(encoding="utf-8")
EMS_SYMBOL = (ROOT / "src/ems-mark.svg.html").read_text(encoding="utf-8")
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900'
         '&family=Instrument+Sans:wght@400;500;600&family=Inter:wght@700;800&family=Unbounded:wght@900&display=swap">')

EMS_WM = ('<span class="wm-ems"><svg class="ems-logo" aria-hidden="true" focusable="false"><use href="#ems-mark"/></svg>'
          '<span>EMS <b>Directory</b></span></span>')
DRUM_WM = '<span class="wm-drum">drum<span class="b">beat</span><span class="p">+</span></span>'
TM = '<span class="tm">&trade;</span>'
CONSULT_WM = ('<span class="wm-consult"><span class="cm-name">Grind<span>stone</span></span>'
              '<span class="cm-sub">Consultancy</span></span>')

ORG = {"@type": "Organization", "name": "Grindstone Ltd", "url": SITE + "/"}

# ---------------------------------------------------------------- pages
# Links inside page bodies use {home} {ems_page} {drum_page} {gemba_page}, filled in per output.

PAGES = [
    {
        "id": "home", "path": "/", "nav": "Home",
        "title": "Grindstone Ltd | Sharper tools for contract manufacturing",
        "description": "Grindstone builds tools for contract electronics manufacturing: EMS Directory for finding a UK supplier, "
                       "drumbeat+ sales and operations software, and Grindstone Consultancy on the shop floor.",
        "jsonld": {"@context": "https://schema.org", **ORG,
                   "legalName": "Grindstone Ltd",
                   "identifier": {"@type": "PropertyValue", "propertyID": "Companies House company number", "value": "17440074"},
                   "address": {"@type": "PostalAddress", "streetAddress": "8 Aldermans Hill", "addressLocality": "Hockley",
                               "addressRegion": "Essex", "postalCode": "SS5 4RW", "addressCountry": "GB"},
                   "brand": [{"@type": "Brand", "name": "EMS Directory", "url": EMS},
                             {"@type": "Brand", "name": "drumbeat+", "url": DRUM}]},
        "body": """
    <div class="hero">
      <div class="wheel" aria-hidden="true"></div>
      <div class="wrap">
        <p class="eyebrow">Grindstone Ltd</p>
        <h1>Grindstone</h1>
        <p class="strap">Sharper tools for <em>contract manufacturing.</em></p>
        <p class="lead lead-big"><strong>Thirty years across OEM, Tier 1 and contract manufacturing.</strong> Three tools we wish we'd had.</p>
      </div>
    </div>
    <div class="wrap products">
      <h2>What we do</h2>
      <div class="cards">
        <article class="card">
          <span class="kind">Find a supplier</span>
          <h3><a href="{ems_page}">""" + EMS_WM + """</a></h3>
          <p>370+ <a href="{EMS}">UK contract electronics manufacturers</a> in one place. Compare them on capability and certification, then send one RFQ to your whole shortlist.</p>
          <div class="card-foot"><a class="more" href="{ems_page}">More about EMS Directory</a><a class="ext" href="{EMS}">emsdirectory.co.uk</a></div>
        </article>
        <article class="card">
          <span class="kind">Run the work &middot; <span class="soon">Coming soon</span></span>
          <h3><a href="{drum_page}">""" + DRUM_WM + TM + """</a></h3>
          <p><a href="{DRUM}">Sales and operations software for EMS companies</a>. It takes every job from lead to delivery, so nothing slips between departments, and runs beside the ERP you already have.</p>
          <div class="card-foot"><a class="more" href="{drum_page}">More about drumbeat+</a><a class="ext" href="{DRUM}">drumbeat.plus</a></div>
        </article>
        <article class="card">
          <span class="kind">Get it right</span>
          <h3><a href="{gemba_page}" aria-label="Grindstone Consultancy">""" + CONSULT_WM + """</a></h3>
          <p>An experienced engineer on the shop floor for NPI, first article, PPAP and root cause, at your site or your supplier's.</p>
          <div class="card-foot"><a class="more" href="{gemba_page}">More about Grindstone Consultancy</a></div>
        </article>
      </div>
    </div>""",
    },
    {
        "id": "ems-directory", "path": "/ems-directory/", "nav": "EMS Directory",
        "title": "EMS Directory: compare UK contract electronics manufacturers | Grindstone Ltd",
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
        <p class="intro">Find the right UK EMS partner, faster.</p>
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
      <a class="cta" href="{EMS}">Find a supplier on EMS Directory</a>
    </div>""",
    },
    {
        "id": "drumbeat", "path": "/drumbeat/", "nav": "drumbeat+",
        "title": "drumbeat+ sales and operations software for EMS companies | Grindstone Ltd",
        "description": "drumbeat+ takes every job in a contract electronics manufacturer from lead to delivery, "
                       "beside the ERP you already have. Coming soon.",
        "jsonld": {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "drumbeat+", "url": DRUM,
                   "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
                   "description": "Sales and operations software for contract electronics manufacturers, from lead to delivery.",
                   "publisher": ORG},
        "body": """
    <div class="wrap page">
      <a class="back" href="{home}">Home</a>
      <header class="big">
        <span class="kind">Run the work &middot; drumbeat.plus &middot; <span class="soon">Coming soon</span></span>
        <h1>""" + DRUM_WM + TM + """</h1>
        <p class="intro">Every job, from lead to delivery.</p>
        <p class="body"><a href="{DRUM}">drumbeat+&trade;</a> is sales and operations software for contract electronics manufacturers.
          It takes each job from first enquiry through quoting, orders, materials, production, quality and despatch,
          and gives every team the right task at the right time.</p>
      </header>
      <ul class="points">
        <li><strong>Built for EMS</strong><span>Follows a job the way an electronics manufacturer actually runs one.</span></li>
        <li><strong>Beside your ERP</strong><span>Your ERP keeps the books. drumbeat+ keeps the beat.</span></li>
        <li><strong>Right task, right time</strong><span>Everyone sees what needs doing today, so jobs keep moving without chasing.</span></li>
        <li><strong>Your customers can see it</strong><span>A live link shows each customer where their orders are.</span></li>
      </ul>
      <h2 class="sub-h">Four plans, one platform</h2>
      <ul class="plans">
        <li><span class="wm-drum">drum<span class="b">beat</span><span class="p">+</span><span class="pl">crm</span></span><span>Win the work.</span></li>
        <li><span class="wm-drum">drum<span class="b">beat</span><span class="p">+</span><span class="pl">ops</span></span><span>Run the work.</span></li>
        <li><span class="wm-drum">drum<span class="b">beat</span><span class="p">+</span><span class="pl">opx</span></span><span>Improve how it runs.</span></li>
        <li><span class="wm-drum">drum<span class="b">beat</span><span class="p">+</span><span class="pl">max</span></span><span>Everything, including regulated work.<span class="later">Later</span></span></li>
      </ul>
      <a class="cta muted" href="{DRUM}">drumbeat.plus &middot; coming soon</a>
    </div>""",
    },
    {
        "id": "consultancy", "path": "/consultancy/", "nav": "Consultancy",
        "title": "Grindstone Consultancy: on-site NPI and quality engineering for EMS | Grindstone Ltd",
        "description": "Hands-on engineering support at your site or your supplier's: NPI, DFM/DFA, APQP and PPAP, "
                       "first article inspection, PFMEA, run at rate and 8D root cause.",
        "jsonld": {"@context": "https://schema.org", "@type": "Service", "name": "Grindstone Consultancy",
                   "serviceType": "On-site operations, quality and engineering support for electronics manufacturing",
                   "provider": ORG, "areaServed": {"@type": "Country", "name": "United Kingdom"}},
        "body": """
    <div class="wrap page">
      <a class="back" href="{home}">Home</a>
      <header class="big">
        <span class="kind">Get it right</span>
        <h1 aria-label="Grindstone Consultancy">""" + CONSULT_WM + """</h1>
        <p class="intro">An experienced pair of hands on your shop floor.</p>
        <p class="body"><i>Gemba</i> is the lean word for the place where the work actually happens. That's where we work:
          at your site or your supplier's, alongside your team, until the problem is fixed and the fix holds.</p>
      </header>

      <ul class="points">
        <li><strong>For EMS providers</strong><span>Extra engineering muscle for a busy NPI, a demanding customer approval or a quality problem that won't go away.</span></li>
        <li><strong>For OEMs and buyers</strong><span>Independent eyes on your supplier, whether you're down the road or overseas.</span></li>
      </ul>

      <h2 class="sub-h">What we do</h2>
      <div class="stages">
        <div class="stage">
          <span class="kind">Into production</span>
          <ul>
            <li>New product introduction<span>From design release to stable production.</span></li>
            <li>DFM / DFA reviews<span>Catch build problems before the first build.</span></li>
            <li>Process validation<span>Prove the process makes good product, every time.</span></li>
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
            <li>Supplier selection<span>Find and qualify the right EMS partner.</span></li>
            <li>Run at rate<span>Prove the line can build at the volume quoted.</span></li>
            <li>Project delivery<span>From kick-off to steady production.</span></li>
          </ul>
        </div>
      </div>

      <div class="experience">
        <p class="big-figure">30 <span>years</span></p>
        <p>Running operations, quality and engineering in electronics manufacturing, including senior roles at global OEMs
          and Tier 1 suppliers. Low-volume, high-mix through to high-volume, in regulated and safety-critical industries.</p>
      </div>

      <h2 class="sub-h">How we work</h2>
      <ol class="cycle">
        <li><strong>Plan</strong><span>Agree the problem and how we'll measure success.</span></li>
        <li><strong>Do</strong><span>Fix it on the shop floor, with your team.</span></li>
        <li><strong>Check</strong><span>Measure the result against the plan.</span></li>
        <li><strong>Act</strong><span>Make the fix the standard, then agree what's next.</span></li>
      </ol>
      <p class="body note">Every job is scoped and priced with you, from a single first article inspection to support from NPI right through to production.</p>

      <div class="contact">
        <strong>Tell us what you need</strong>
        <span class="addr">""" + CONTACT + """</span>
      </div>
      <p class="crosslink">Still looking for a supplier? Compare 370+ <a href="{EMS}">UK contract electronics manufacturers</a> on EMS Directory.</p>
    </div>""",
    },
]

FOOTER = """
<footer>
  <div class="wrap">
    <p class="legal">Grindstone Ltd. Registered in England and Wales, company number 17440074.
      Registered office: 8 Aldermans Hill, Hockley, Essex, SS5 4RW.</p>
    <nav aria-label="Our sites">
      <a href="{EMS}">EMS Directory</a>
      <a href="{DRUM}">drumbeat+</a>
      <a href="{gemba_page}">Grindstone Consultancy</a>
    </nav>
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
    <a class="mark" href="{links['home']}">Grind<span>stone</span></a>
    <nav aria-label="Main">
{items}
    </nav>
  </div>
</div>"""


def fill(text, links):
    return (text.replace("{home}", links["home"]).replace("{ems_page}", links["ems-directory"])
            .replace("{drum_page}", links["drumbeat"]).replace("{gemba_page}", links["consultancy"])
            .replace("{EMS}", EMS).replace("{DRUM}", DRUM))


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
{fill(p['body'], links)}
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
    (out / "CNAME").write_text("grindstone.ltd\n", encoding="utf-8")   # GitHub Pages custom domain
    (out / ".nojekyll").write_text("", encoding="utf-8")                   # serve files as they are
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


# ---------------------------------------------------------------- single-file preview (Claude artifact)

def build_preview():
    links = {p["id"]: "#" + p["id"] for p in PAGES}
    sections = "\n".join(
        f'  <section data-page="{p["id"]}"' + ("" if p["id"] == "home" else " hidden") + f'>{fill(p["body"], links)}\n  </section>'
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
