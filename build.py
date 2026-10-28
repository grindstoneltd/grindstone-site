"""Build the Grindstone Ltd site.

  python3 build.py

Writes:
  docs/             the real site, served by GitHub Pages on grindstone.ltd (one page per product, sitemap, robots)
  index.html        a single-file preview with the same content (published as the Claude artifact)

Edit the page content below, then run the script; never edit docs/ or index.html by hand.
"""
import datetime
import json
import shutil
import os
import re
from html import escape as html_escape
import pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://grindstone.ltd"
EMS = "https://www.emsdirectory.co.uk/"          # canonical address of EMS Directory (apex 301s here)
DRUM = "https://drumbeat.plus/"
CONTACT = "enquiries@grindstone.ltd"
MAIL = '<a href="mailto:' + CONTACT + '">' + CONTACT + '</a>'
LINKEDIN = "https://www.linkedin.com/company/grindstoneltd/"
from urllib.parse import quote
DEMO_BODY = "Hi,\r\n\r\nI'd like a demo of drumbeat+.\r\n\r\nName:\r\nCompany:\r\nPhone:\r\nBest time to call:\r\n"
DEMO = "mailto:" + CONTACT + "?subject=" + quote("drumbeat+ demo request") + "&amp;body=" + quote(DEMO_BODY)
LI_EMS = "https://www.linkedin.com/company/emsdirectory/"
LI_DRUM = "https://www.linkedin.com/company/drumbeatplus/"
LI_COLIN = "https://www.linkedin.com/in/colinastbury/"
# Cloudflare Web Analytics (cookie-free, so no consent banner). Paste the site token from the Cloudflare dashboard;
# empty = no tracking script. Live site only, never the Claude preview.
CF_BEACON_TOKEN = "a5c66aa1f32649e99122b57591ff7131"
# Answers go to a Google Sheet through an Apps Script web app (Grindstone/marketing/readiness-checklist/).
# Empty READINESS_URL = the form still works and shows the result, but nothing is stored.
READINESS_URL = "https://script.google.com/macros/s/AKfycbx5I1WfB0XPxjau-cv0nwY1bLvCflY-6dSighM5RbXp7ci5wateCmbeYwR23qIQAf3Qzg/exec"
# Pages stay off the site until the Sheet URL is set and Colin approves; PREVIEW_READINESS=1 builds them locally.
SHOW_READINESS = bool(READINESS_URL) or os.environ.get("PREVIEW_READINESS") == "1"
# Home page band promoting the checklist (wording approved by Colin 26 Oct 2026)
SHOW_HOME_TOOL = SHOW_READINESS

# Escalation matrix, training matrix and critical spares templates: cards go live with the escalation matrix post
# (Wed 4 Nov 2026). The PDFs wait in Grindstone/marketing/escalation-matrix/ until the publish run copies them into src/downloads/.
SHOW_OPS_TEMPLATES = datetime.date.today().isoformat() >= "2026-11-04"
OPS_TEMPLATES = """
        <li><strong>Escalation matrix</strong><span>Who hears about a problem, and how fast: three tiers, measurable thresholds, the team's own decisions and a call list.</span><a class="dl" href="/downloads/grindstone-escalation-matrix-template.pdf" download>Download PDF<small>4 pages, 470 KB</small></a></li>
        <li><strong>Training matrix</strong><span>Who can do what, to what level, and where one absence would leave a machine or test without cover.</span><a class="dl" href="/downloads/grindstone-training-matrix-template.pdf" download>Download PDF<small>3 pages, 26 people, 660 KB</small></a></li>
        <li><strong>Critical spares</strong><span>The parts that would stop a line, how many to keep, where they are and who reorders them.</span><a class="dl" href="/downloads/grindstone-critical-spares-template.pdf" download>Download PDF<small>3 pages, 490 KB</small></a></li>"""
# LinkedIn "in" logo (Simple Icons 9.0.0, CC0)
LI_ICON = ('<svg class="li-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>')
TODAY = datetime.date.today().isoformat()

CSS = (ROOT / "src/styles.css").read_text(encoding="utf-8")
EMS_SYMBOL = (ROOT / "src/ems-mark.svg.html").read_text(encoding="utf-8") + (ROOT / "src/cnc-mark.svg.html").read_text(encoding="utf-8") + (ROOT / "src/emc-mark.svg.html").read_text(encoding="utf-8")
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,600..900'
         '&family=Michroma&family=Instrument+Sans:wght@400;500;600&family=Inter:wght@700;800&family=Unbounded:wght@900&display=swap">')

EMS_WM = ('<span class="wm-ems"><svg class="ems-logo" aria-hidden="true" focusable="false"><use href="#ems-mark"/></svg>'
          '<span>EMS <b>Directory</b></span></span>')
DRUM_WM = '<span class="wm-drum">drum<span class="b">beat</span><span class="p">+</span></span>'
# CNC Directory wordmark: its cube mark (Other directories/CNC/brand/cnc_cube_only_black.svg) and CNC blue
CNC_WM = ('<span class="wm-cnc"><svg class="cnc-logo" aria-hidden="true" focusable="false"><use href="#cnc-mark"/></svg>'
          '<span>CNC <b>Directory</b></span></span>')
CNC = "https://www.cncdirectory.co.uk/"
# CNC Directory is switched off until launch (by Thu 5 Nov 2026): no link until then. Set True on launch day.
CNC_LIVE = False
# The /cnc-directory/ page is live from 27 Oct (Colin: "make it live"); until CNC_LIVE it shows "Coming soon"
# instead of links to cncdirectory.co.uk
SHOW_CNC_PAGE = True
# EMC Directory wordmark: its cube mark (src/emc-mark.svg.html) and EMC signal red. Switch-on planned Thu 12 Nov 2026
EMC_WM = ('<span class="wm-cnc wm-emc"><svg class="cnc-logo" aria-hidden="true" focusable="false"><use href="#emc-mark"/></svg>'
          '<span>EMC <b>Directory</b></span></span>')
EMC = "https://www.emcdirectory.co.uk/"
EMC_LIVE = False
SHOW_EMC_PAGE = True
TM = '<span class="tm">&trade;</span>'
# 'stone' with the O drawn as the grindstone wheel (a hidden 'o' keeps the word readable to screen readers and search)
STONE = ('st<span class="o-wheel"><svg viewBox="0 0 100 100" aria-hidden="true" focusable="false"><circle cx="50" cy="50" r="44.5" fill="none" stroke="currentColor" stroke-width="11"/><circle cx="50" cy="50" r="28" fill="none" stroke="currentColor" stroke-width="8"/><circle cx="50" cy="50" r="12" fill="none" stroke="currentColor" stroke-width="7"/></svg><span class="sr">o</span></span>ne')
# The company wordmark, used where a product mark would go (Grindstone Ltd is the brand; consultancy is a service, not a brand)
GS_WM = '<span class="mark gs-wm">Grind<span>' + STONE + '</span></span>'

ORG = {"@type": "Organization", "name": "Grindstone Ltd", "url": SITE + "/", "sameAs": [LINKEDIN],
       "founder": {"@type": "Person", "name": "Colin Astbury", "sameAs": [LI_COLIN]}}

# ---------------------------------------------------------------- pages
# Links inside page bodies use {home} {ems_page} {drum_page} {gemba_page}, filled in per output.

PAGES = [
    {
        "id": "home", "path": "/", "nav": "Home",
        "title": "Grindstone | Cutting-edge solutions for contract manufacturing",
        "description": "Grindstone runs EMS Directory and CNC Directory, builds drumbeat+ sales and operations software, and offers hands-on consultancy for contract manufacturers.",
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
        <h1><span class="nowrap">Cutting-edge</span> solutions for <em>contract manufacturing.</em></h1>
        <p class="lead lead-big">Sourcing, software and support for contract manufacturing, built on 30+ years in engineering, sales and operations across OEMs, Tier 1s and EMS companies.</p>
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
          <span class="kind">Find a machining supplier</span>
          <h3>""" + ('<a href="{link:cnc-directory}">' + CNC_WM + '</a>' if SHOW_CNC_PAGE else CNC_WM) + """</h3>
          <p>UK CNC machining companies in one place. Compare them on the machining they do, the materials they work with and their certification.</p>
          <div class="card-foot">""" + ('<a class="more" href="{link:cnc-directory}">More about CNC Directory</a>' + (f'<a class="ext" href="{CNC}">cncdirectory.co.uk</a>' if CNC_LIVE else '<span class="soon">Coming soon</span>')) + """</div>
        </article>""" + ("""
        <article class="card">
          <span class="kind">Find an EMC test lab</span>
          <h3><a href="{link:emc-directory}">""" + EMC_WM + """</a></h3>
          <p>UK EMC testing and compliance companies in one place. Compare them on the standards they test to, the tests they run and their accreditations.</p>
          <div class="card-foot"><a class="more" href="{link:emc-directory}">More about EMC Directory</a>""" + (f'<a class="ext" href="{EMC}">emcdirectory.co.uk</a>' if EMC_LIVE else '<span class="soon">Launching November</span>') + """</div>
        </article>""" if SHOW_EMC_PAGE else "") + """
        <article class="card">
          <span class="kind">Sales and operations</span>
          <h3><a href="{drum_page}">""" + DRUM_WM + TM + """</a></h3>
          <p><a href="{drum_page}">Sales and operations software for EMS companies</a>: quotes, orders and production in one place, beside the ERP you already have.</p>
          <div class="card-foot"><a class="more" href="{drum_page}">More about drumbeat+</a></div>
        </article>
        <article class="card">
          <span class="kind">Consultancy</span>
          <h3><a href="{gemba_page}" aria-label="Grindstone">""" + GS_WM + """</a></h3>
          <p>Hands-on consultancy across sales, operations and practical AI: winning the right work, new product introduction, customer approvals, and quality or supplier problems that need fixing.</p>
          <div class="card-foot"><a class="more" href="{gemba_page}">More about our consultancy</a></div>
        </article>
      </div>
    </div>""" + ("""
    <section class="wrap tool-band" aria-labelledby="tool-band-h">
      <div class="tool-band-in">
        <div>
          <span class="kind">Free tool &middot; 3 minutes</span>
          <h2 id="tool-band-h">Could AI take the admin off your team's plate?</h2>
          <p>Find out in three minutes, with your score and an action plan.</p>
        </div>
        <a class="cta" href="{link:ai-readiness}">Get my score</a>
      </div>
    </section>""" if SHOW_HOME_TOOL else "") + """
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
        <div class="brandmark" role="img" aria-label="EMS Directory">""" + EMS_WM + """</div>
        <h1 class="intro">Find the UK EMS partner that fits the job.</h1>
        <p class="body"><a href="{EMS}">EMS Directory</a> lists 370+ UK contract electronics manufacturers, from prototype
          specialists to high-volume box build. Every listing uses the same layout, so you can compare suppliers like for like
          on the things that decide a project.</p>
      </header>
      <h2 class="sub-h">Why use EMS Directory</h2>
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
    *([{
        "id": "cnc-directory", "path": "/cnc-directory/", "nav": None,
        "title": "CNC Directory: compare UK CNC machining companies | Grindstone",
        "description": "Compare UK CNC machining companies on the machining they do, the materials they work with and their certification.",
        "jsonld": {"@context": "https://schema.org", "@type": "WebSite", "name": "CNC Directory", "url": CNC if CNC_LIVE else SITE + "/cnc-directory/",
                   "description": "Directory of UK CNC machining companies.", "publisher": ORG},
        "body": """
    <div class="wrap page">
      <a class="back" href="{home}">Home</a>
      <header class="big">
        <span class="kind">Find a machining supplier &middot; cncdirectory.co.uk</span>
        <div class="brandmark" role="img" aria-label="CNC Directory">""" + CNC_WM + """</div>
        <h1 class="intro">Find the UK machine shop that fits the job.</h1>
        <p class="body">""" + ('<a href="{CNC}">CNC Directory</a>' if CNC_LIVE else 'CNC Directory') + """ lists UK CNC machining companies, from one-off prototypes to production
          runs. Every listing uses the same layout, so you can compare suppliers like for like on the things that decide a job.</p>
      </header>
      <h2 class="sub-h">Why use CNC Directory</h2>
      <ul class="points">
        <li><strong>UK machine shops in one place</strong><span>Milling, turning and more, without searching company by company.</span></li>
        <li><strong>Compare like for like</strong><span>See the machining each company does, the materials they work with and their certification.</span></li>
        <li><strong>From the team behind EMS Directory</strong><span>Built the same way as <a href="{EMS}">EMS Directory</a>, our directory of UK contract electronics manufacturers.</span></li>
      </ul>
      <div class="cta-row">
        """ + ('<a class="cta" href="{CNC}">Find a supplier on CNC Directory</a>' if CNC_LIVE else '<span class="soon">Coming soon</span>') + """
      </div>
    </div>""",
    }] if SHOW_CNC_PAGE else []),
    *([{
        "id": "emc-directory", "path": "/emc-directory/", "nav": None,
        "title": "EMC Directory: compare UK EMC test labs | Grindstone",
        "description": "Compare UK EMC testing and compliance companies on the standards they test to, the tests they run and their accreditations.",
        "jsonld": {"@context": "https://schema.org", "@type": "WebSite", "name": "EMC Directory", "url": EMC if EMC_LIVE else SITE + "/emc-directory/",
                   "description": "Directory of UK EMC testing and compliance companies.", "publisher": ORG},
        "body": """
    <div class="wrap page">
      <a class="back" href="{home}">Home</a>
      <header class="big">
        <span class="kind">Find an EMC test lab &middot; emcdirectory.co.uk</span>
        <div class="brandmark" role="img" aria-label="EMC Directory">""" + EMC_WM + """</div>
        <h1 class="intro">Find the UK EMC test lab that fits the product.</h1>
        <p class="body">""" + ('<a href="{EMC}">EMC Directory</a>' if EMC_LIVE else 'EMC Directory') + """ lists UK EMC testing and compliance companies, from pre-compliance checks
          to formal testing. Every listing uses the same layout, so you can compare labs like for like on the things that decide a test.</p>
      </header>
      <h2 class="sub-h">Why use EMC Directory</h2>
      <ul class="points">
        <li><strong>UK EMC labs in one place</strong><span>Testing and compliance support, without searching company by company.</span></li>
        <li><strong>Compare like for like</strong><span>See the standards each company tests to, the tests and chambers they have, and their accreditations.</span></li>
        <li><strong>From the team behind EMS Directory</strong><span>Built the same way as <a href="{EMS}">EMS Directory</a>, our directory of UK contract electronics manufacturers.</span></li>
      </ul>
      <div class="cta-row">
        """ + ('<a class="cta" href="{EMC}">Find a lab on EMC Directory</a>' if EMC_LIVE else '<span class="soon">Launching November</span>') + """
      </div>
    </div>""",
    }] if SHOW_EMC_PAGE else []),
    {
        "id": "drumbeat", "path": "/drumbeat/", "nav": "drumbeat+",
        "title": "drumbeat+ sales and operations software for EMS | Grindstone",
        "description": "drumbeat+ is sales and operations software for EMS companies: quotes, orders and production in one place, "
                       "beside the ERP you already have.",
        "jsonld": {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "drumbeat+", "url": SITE + "/drumbeat/", "sameAs": [LI_DRUM],
                   "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
                   "description": "Sales and operations software for EMS companies: quotes, orders and production in one place, beside the ERP you already have.",
                   "publisher": ORG},
        "body": """
    <div class="wrap page page-top">
      <a class="back" href="{home}">Home</a>
      <header class="big">
        <span class="kind">Sales and operations</span>
        <div class="brandmark" role="img" aria-label="drumbeat+">""" + DRUM_WM + TM + """</div>
        <h1 class="intro">Your ERP keeps the books. """ + DRUM_WM + """ keeps the beat.</h1>
        <p class="body">drumbeat+&trade; is sales and operations software for contract electronics manufacturers.
          Every job in one place, from first enquiry to despatch, so every team knows what to do next.</p>
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
        "title": "Contract manufacturing consultancy, UK | Grindstone",
        "description": "UK contract manufacturing consultancy: winning work, NPI, PPAP and quality approvals, supplier selection and practical AI. Fixed price, remote or on site.",
        "jsonld": {"@context": "https://schema.org", "@type": "Service", "name": "Contract manufacturing consultancy",
                   "serviceType": "Sales, marketing, operations, quality, engineering and practical AI consultancy for electronics manufacturing",
                   "provider": ORG, "areaServed": {"@type": "Country", "name": "United Kingdom"}},
        "body": """
    <div class="wrap page">
      <a class="back" href="{home}">Home</a>
      <header class="big">
        <span class="kind">Consultancy</span>
        <div class="brandmark" role="img" aria-label="Grindstone">""" + GS_WM + """</div>
        <h1 class="intro">Contract manufacturing consultancy, remotely or on your shop floor.</h1>
        <p class="body">30+ years in engineering and manufacturing: building and leading teams, running production and quality, and
          representing companies to OEMs around the world. We help contract manufacturers win the right work, get new products
          through customer approval and fix quality problems for good. We help OEMs get the best from their suppliers. And we help
          both put AI to practical use. Every job has a fixed price, agreed before we start.</p>
      </header>

      <h2 class="sub-h">Who we work with</h2>
      <ul class="points">
        <li><strong>Contract manufacturers</strong><span>Extra experience for winning new customers, a busy NPI, a demanding customer approval, or a quality problem that keeps coming back.</span></li>
        <li><strong>OEMs and buyers</strong><span>An independent engineer on site with your supplier, whether they're down the road or you're overseas.</span></li>
      </ul>

      <h2 class="sub-h">What we can help with</h2>
      <div class="stages">
        <div class="stage stage-wide">
          <span class="kind">Sales and marketing</span>
          <ul>
            <li>Sales strategy<span>Choose the markets and customers that suit your factory, then build the pipeline.</span></li>
            <li>RFQ and quoting<span>Quote faster and more consistently, and win more of the work you want.</span></li>
            <li>Key account management<span>Grow and keep your most important customers.</span></li>
            <li>Pricing and margin<span>Costing and quoting models that protect your margin.</span></li>
            <li>Sales process and CRM<span>Track every lead and quote, so none go cold.</span></li>
            <li>Positioning and messaging<span>Know what makes you different, and say it clearly.</span></li>
            <li>Web design<span>A clear, modern website that turns visitors into enquiries.</span></li>
            <li>Sales collateral<span>Capability decks, case studies and website copy.</span></li>
            <li>Trade shows and outreach<span>Plan events, follow up properly and run campaigns.</span></li>
          </ul>
        </div>
        <div class="stage">
          <span class="kind">Into production</span>
          <ul>
            <li>New product introduction<span>From design release to stable production.</span></li>
            <li>DFM / DFA reviews<span>Catch build problems before the first build.</span></li>
            <li>Process validation<span>Show the process is capable and repeatable.</span></li>
            <li>ECN / ECO implementation<span>Cut engineering changes in cleanly, with no mixed builds.</span></li>
          </ul>
        </div>
        <div class="stage">
          <span class="kind">Quality and approval</span>
          <ul>
            <li>APQP and PPAP<span>Plan for quality and get the customer's sign-off.</span></li>
            <li>PFMEA<span>Find where the process can fail, before it does.</span></li>
            <li>First article inspection<span>Check the first build against every requirement.</span></li>
            <li>8D root cause and corrective action<span>Find the real cause, fix it and prove it's fixed.</span></li>
          </ul>
        </div>
        <div class="stage">
          <span class="kind">Suppliers and capacity</span>
          <ul>
            <li>Supplier selection<span>Find and qualify the right manufacturing partner.</span></li>
            <li>Run at rate<span>Prove the line can build at the quoted volume before the orders arrive.</span></li>
            <li>Project delivery<span>Run the project from kick-off to steady production.</span></li>
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
        <p class="big-figure">30+ <span>years</span></p>
        <div class="bio">
          <h2 class="bio-name">Colin Astbury</h2>
          <p>Colin began his career in 1992 as an aircraft engineer in the Royal Navy's Fleet Air Arm, working on Sea Harriers, and
            served as a weapons engineer in the Gulf and the former Yugoslavia. He then spent 18 years at TT Electronics plc, progressing through test
            engineering, quality, production and project management to lead sales for the UK, Ireland and Northern Europe.</p>
          <p>He went on to manage EMEA accounts for Joyson Safety Systems, a global Tier 1 automotive supplier, before returning to
            operations as operations manager at DVR Ltd (now Note Basildon) and Leonardo.</p>
          <p>His experience covers quality, NPI, production and commercial leadership, on both sides of the customer and supplier
            relationship, across automotive, industrial, aerospace and defence, medical and rail.</p>
          <a class="li li-page" href="{LI_COLIN}">""" + LI_ICON + """<span>Connect with Colin on LinkedIn</span></a>
        </div>
      </div>

      <h2 class="sub-h">How we work</h2>
      <p class="cycle-intro">Every job follows DMAIC, the Six Sigma improvement method.</p>
      <ol class="dmaic">
        <li style="--i:0"><span class="node">D</span><strong>Define</strong><span class="txt">The problem, the scope and a fixed price.</span></li>
        <li style="--i:1"><span class="node">M</span><strong>Measure</strong><span class="txt">How things run today, from your data and the shop floor.</span></li>
        <li style="--i:2"><span class="node">A</span><strong>Analyse</strong><span class="txt">Find the real cause.</span></li>
        <li style="--i:3"><span class="node">I</span><strong>Improve</strong><span class="txt">Put the fix in, with your team.</span></li>
        <li style="--i:4"><span class="node">C</span><strong>Control</strong><span class="txt">Make sure it stays fixed, with a written report your team keeps.</span></li>
      </ol>

      <div class="contact">
        <strong>Tell us the problem. We'll say straight away if we can help.</strong>
        <a class="addr" href="mailto:""" + CONTACT + """">""" + CONTACT + """</a>
      </div>
      <a class="li li-page" href="{LINKEDIN}">""" + LI_ICON + """<span>Follow Grindstone on LinkedIn</span></a>
      <p class="crosslink">Still looking for a supplier? Compare 370+ <a href="{EMS}">UK contract electronics manufacturers</a> on EMS Directory.</p>

      <h2 class="sub-h">""" + ("Free tools and templates" if SHOW_READINESS else "Free problem-solving templates") + """</h2>
      <p class="cycle-intro">Fillable PDFs with step-by-step instructions built in. Type into them on screen or print them out. Free to use and share.""" + (" The AI readiness checklist works online and shows your score as soon as you finish." if SHOW_READINESS else "") + """</p>
      <ul class="templates">
        <li><strong>8D Problem Solving Report</strong><span>Find the root cause, fix it and stop it coming back, from D0 to D8.</span><a class="dl" href="/downloads/grindstone-8d-problem-solving-template.pdf" download>Download PDF<small>3 pages, 310 KB</small></a></li>
        <li><strong>5 Whys</strong><span>Ask why across Man, Machine, Method and Material to reach the root cause.</span><a class="dl" href="/downloads/grindstone-5-whys-template.pdf" download>Download PDF<small>2 pages, 270 KB</small></a></li>
        <li><strong>Fishbone (Ishikawa) diagram</strong><span>List every possible cause in six groups before you start testing.</span><a class="dl" href="/downloads/grindstone-fishbone-diagram-template.pdf" download>Download PDF<small>2 pages, 220 KB</small></a></li>
        <li><strong>Process FMEA</strong><span>Find where each process step could fail, and what stops it.</span><a class="dl" href="/downloads/grindstone-pfmea-template.pdf" download>Download PDF<small>6 pages, 75 rows, 1.1 MB</small></a></li>
        <li><strong>Kaizen improvement sheet</strong><span>See the waste, try a fix, measure the result and make it the new standard.</span><a class="dl" href="/downloads/grindstone-kaizen-template.pdf" download>Download PDF<small>2 pages, 270 KB</small></a></li>""" + (OPS_TEMPLATES if SHOW_OPS_TEMPLATES else "") + ("""
        <li><strong>AI readiness checklist</strong><span>Twelve quick statements to see whether one job is ready to hand to AI, with your score and an action plan.</span><a class="dl" href="/ai-readiness/">Get my score<small>Online, about three minutes</small></a></li>""" if SHOW_READINESS else "") + """
      </ul>
    </div>""",
    },
]

# ---------------------------------------------------------------- blog
# Posts are markdown files in src/blog/ with a small front matter block (title, date, kind, order, description,
# original). kind "Summary" = a short Grindstone take on an EMS Directory article, linking to the full piece there,
# so the two sites never carry duplicate copies. Unpublished pieces wait in src/blog-drafts/ and are not built.

def md_inline(t):
    t = html_escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    # drumbeat+ in running text: its wordmark, linked to its page (left unlinked when it is already inside a link)
    parts = re.split(r"(\[[^\]]+\]\([^)\s]+\))", t)
    t = "".join(p.replace("drumbeat+", DRUM_WM) if p.startswith("[")
                else p.replace("drumbeat+", f'<a class="wm-link" href="{{drum_page}}">{DRUM_WM}</a>') for p in parts)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)


def brand_heading(h):
    """Company name in a heading goes in the Grindstone wordmark style."""
    return h.replace("Grindstone", f'<span class="wm-inline">Grind<span>{STONE}</span></span>')


def md_to_html(md):
    out, para, items, kind = [], [], [], ["ul"]
    def flush():
        if para: out.append("<p>" + md_inline(" ".join(para)) + "</p>"); para.clear()
        if items: out.append(f"<{kind[0]}>" + "".join(f"<li>{md_inline(i)}</li>" for i in items) + f"</{kind[0]}>"); items.clear()
    for line in md.splitlines():
        line = line.rstrip()
        if not line: flush(); continue
        if line.startswith("## "): flush(); out.append(f"<h2>{brand_heading(md_inline(line[3:]))}</h2>"); continue
        im = re.match(r"!\[([^\]]*)\]\(([^)\s]+)\)$", line)
        if im: flush(); out.append(f'<figure class="post-img"><img src="{im.group(2)}" alt="{html_escape(im.group(1))}" loading="lazy" width="1080" height="1350"></figure>'); continue
        m = re.match(r"(- |\d+\. )(.*)", line)
        if m:
            k = "ul" if m.group(1) == "- " else "ol"
            if para or (items and kind[0] != k): flush()
            kind[0] = k; items.append(m.group(2)); continue
        para.append(line)
    flush()
    return "\n".join(out)


def shown_date(p):
    """Summaries carry the date their EMS Directory article first appeared; our own articles their own date."""
    return p.get("original_date") or p.get("event_date") or p["date"]


# Line a post can carry as {readiness}; dropped until the checklist page is live
READINESS_MD = "Not sure where you stand? [Score your business on our AI readiness checklist](/ai-readiness/). It takes three minutes, and you get an action plan straight away.\n"


def load_posts():
    posts = []
    # PREVIEW_DRAFT=<slug> builds one draft from src/blog-drafts/ for a local look; never use it for a build that gets pushed
    preview = os.environ.get("PREVIEW_DRAFT")
    files = sorted((ROOT / "src/blog").glob("*.md")) + ([ROOT / "src/blog-drafts" / f"{preview}.md"] if preview else [])
    for f in files:
        head, body = f.read_text(encoding="utf-8").split("---\n", 2)[1:]
        body = body.replace("{readiness}\n", READINESS_MD if SHOW_READINESS else "")
        meta = dict(l.split(": ", 1) for l in head.strip().splitlines())
        meta["slug"], meta["html"] = f.stem, md_to_html(body)
        if meta["date"] == "DRAFT":
            meta["date"] = TODAY
        elif meta["date"] > TODAY:      # scheduled: a future-dated post stays off the site until a build on or after its date
            continue
        posts.append(meta)
    return sorted(posts, key=lambda p: (shown_date(p), p["title"]), reverse=True)


def nice_date(iso):
    return datetime.date.fromisoformat(iso).strftime("%-d %b %Y")


POSTS = load_posts()
BLOG_DESC = "Articles for contract manufacturers and the OEMs who buy from them: choosing suppliers, NPI, quality and sourcing."
blog_items = "\n".join(
    f"""        <li><a href="{{link:post-{p['slug']}}}"><span class="post-meta">{nice_date(shown_date(p))}"""
    + (" &middot; EMS Directory article, summarised" if p.get("kind") == "Summary" else " &middot; Company news" if p.get("kind") == "News" else "")
    + f"""</span><strong>{brand_heading(html_escape(p['title']))}</strong><span>{html_escape(p['description'])}</span></a></li>"""
    for p in POSTS)
PAGES.append({
    "id": "blog", "path": "/blog/", "nav": "Blog",
    "title": "Nose to the Grindstone: a contract manufacturing blog", "description": BLOG_DESC,
    "jsonld": {"@context": "https://schema.org", "@type": "Blog", "name": "Grindstone blog", "url": SITE + "/blog/", "publisher": ORG},
    "body": f"""
    <div class="wrap page">
      <a class="back" href="{{home}}">Home</a>
      <header class="big">
        <span class="kind">Blog</span>
        <h1 class="intro">Nose to the <span class="wm-inline">Grind<span>{STONE}</span></span>.</h1>
        <p class="body">{BLOG_DESC}</p>
      </header>
      <ul class="post-list">
{blog_items}
      </ul>
    </div>""",
})
for p in POSTS:
    src = ""
    if p.get("original"):
        src = f"""
        <p class="post-source"><a class="cta" href="{p['original']}">Read the full article on EMS Directory</a></p>"""
    PAGES.append({
        "id": "post-" + p["slug"], "path": f"/blog/{p['slug']}/", "nav": None, "og_type": "article",
        "title": (lambda t: t + " | Grindstone" if len(t) <= 47 else t)(p.get("seo_title", p["title"])), "description": p["description"],
        "published": p["date"],
        "jsonld": {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
                   "description": p["description"], "datePublished": p["date"], "url": f"{SITE}/blog/{p['slug']}/",
                   "author": ORG, "publisher": ORG, **({"isBasedOn": p["original"]} if p.get("original") else {})},
        "body": f"""
    <div class="wrap page">
      <a class="back" href="{{link:blog}}">Blog</a>
      <article class="post">
        <header class="big">
          <span class="kind">{('Summary of an EMS Directory article first published ' + nice_date(p['original_date'])) if p.get('original_date') else ('Company news &middot; ' + nice_date(p['event_date'])) if p.get('event_date') else nice_date(p['date'])}</span>
          <h1 class="intro">{brand_heading(html_escape(p['title']))}</h1>
        </header>
        <div class="prose">
{p['html']}
        </div>{src}
      </article>
    </div>""",
    })


# ---------------------------------------------------------------- AI readiness checklist (lead capture)

# Each statement scores 0/1/2. Partly or True opens its follow-ups; their names become Sheet column headings.
#   ("checks", name, prompt, options)  tick all that apply
#   ("choice", name, prompt, options)  pick one
#   ("text", name, prompt)
RC_GROUPS = [
    ("Problem", [
        ("We can name one specific, repetitive task that costs us real time every week.", [
            ("checks", "Q1 tasks", "Which tasks take the time? Tick all that apply.",
             ["Chasing leads and enquiries", "Quoting RFQs", "Checking and costing BOMs", "Chasing supplier delivery dates",
              "Raising purchase orders", "Entering customer orders", "Customer progress updates", "Shortage and stock checks",
              "Engineering changes", "Quality paperwork (NCRs, 8Ds, CoCs)", "Planning and scheduling", "Invoicing and credit control"]),
            ("text", "Q1 other", "Anything else?")]),
        ("We know roughly how long that task takes today, and how often it goes wrong.", [
            ("choice", "Q2 hours a week", "Roughly how many hours a week does it take?",
             ["Under 2", "2 to 5", "5 to 10", "10 to 20", "Over 20"]),
            ("choice", "Q2 how often it goes wrong", "How often does it go wrong?",
             ["Rarely", "Monthly", "Weekly", "Daily"]),
            ("checks", "Q2 what goes wrong", "What goes wrong? Tick all that apply.",
             ["Late or missed dates", "Wrong prices or costs", "Keying errors", "Emails missed",
              "Customer complaints", "Rework or scrap"])]),
        ("Our senior team is engaged in the process and will make time for the pilot each week.", [
            ("checks", "Q3 who is engaged", "Who is engaged? Tick all that apply.",
             ["Owner or MD", "Operations", "Sales", "Purchasing", "Quality", "Engineering", "Finance"])]),
    ]),
    ("Data", [
        ("The information the task needs lives somewhere we can get at: the ERP, a shared drive or a mailbox.", [
            ("checks", "Q4 where it lives", "Where does it live? Tick all that apply.",
             ["ERP or MRP system", "Spreadsheets", "Shared drive", "Email inboxes", "Paper", "Supplier or customer portals"]),
            ("text", "Q4 which ERP", "Which ERP or MRP system, if any?")]),
        ("That information is mostly up to date (lead times, prices, stock, open orders).", [
            ("text", "Q5 detail", "Which information is up to date, and which isn't?")]),
        ("We know which data belongs to customers and is covered by an NDA or export control.", [
            ("text", "Q6 detail", "How do you keep track of it? For example: a register, or flags in the ERP.")]),
    ]),
    ("People", [
        ("The people who do the task today are involved and willing to try it.", [
            ("text", "Q7 detail", "Who is involved? Job titles are enough.")]),
        ("We have named one owner for the pilot and one person who checks the outputs.", [
            ("text", "Q8 detail", "Who are the owner and the checker? Job titles are enough.")]),
        ("Staff know which AI tools are approved, and which are not.", [
            ("checks", "Q9 tools approved", "Which tools are approved? Tick all that apply.",
             ["ChatGPT", "Microsoft Copilot", "Google Gemini", "Claude"]),
            ("text", "Q9 other tools", "Any others?")]),
    ]),
    ("Guardrails", [
        ("We have a written rule on what the agent may and may not do (for example: draft, never send).", [
            ("text", "Q10 may do", "What may the agent do? For example: read RFQs and draft quotes."),
            ("text", "Q10 must never do", "What must it never do? For example: send anything to a customer.")]),
        ("We've made sure no agent can commit spend, change master data or make a promise to a customer.", [
            ("text", "Q11 detail", "How is that stopped? For example: read-only access, or sign-off before anything leaves the building.")]),
        ("We've decided where every agent output will be logged, so the work stays traceable for audit.", [
            ("text", "Q12 detail", "Where will outputs be logged? For example: against the job in the ERP.")]),
    ]),
]
# Unscored questions about the business, always shown, all optional
RC_ABOUT = [
    ("choice", "Staff", "How many people work in the business?", ["1 to 10", "11 to 50", "51 to 200", "Over 200"]),
    ("checks", "What you make", "What do you make? Tick all that apply.",
     ["PCB assembly", "Cable and harness", "Box build", "Mechanical or machined parts", "Other"]),
    ("checks", "Sectors", "Which sectors do you supply? Tick all that apply.",
     ["Defence", "Aerospace", "Medical", "Industrial", "Automotive", "Rail", "Telecoms", "Consumer"]),
    ("choice", "When to start", "When would you like to start?", ["Just exploring", "Within 3 months", "Within 6 months", "Within a year"]),
]


def rc_field(kind, name, prompt, opts=None):
    if kind == "text":
        return f'<label class="rc-text">{prompt}<textarea name="{name}" rows="2" maxlength="300"></textarea></label>'
    t = "checkbox" if kind == "checks" else "radio"
    chips = "".join(f'<label><input type="{t}" name="{name}" value="{html_escape(o)}"><span>{html_escape(o)}</span></label>' for o in opts)
    return f'<div class="rc-pick"><p>{prompt}</p><div class="rc-opts rc-chips">{chips}</div></div>'


def rc_form():
    out, n = [], 0
    for group, items in RC_GROUPS:
        out.append(f'      <h3 class="rc-group">{group}</h3>')
        for text, follow in items:
            n += 1
            score = "".join(f'<label><input type="radio" name="q{n}" value="{v}"><span>{lab}</span></label>'
                            for v, lab in ((0, "Not true"), (1, "Partly"), (2, "True")))
            more = "".join(rc_field(*f) for f in follow)
            out.append(f'      <fieldset class="rc-q"><legend><b>{n:02d}</b> {text}</legend><div class="rc-opts">{score}</div>'
                       f'<div class="rc-more rc-x" hidden>{more}</div></fieldset>')
    out.append('      <h3 class="rc-group">About your business <span class="rc-opt">(optional)</span></h3>')
    out.append('      <fieldset class="rc-q rc-x rc-about">' + "".join(rc_field(*f) for f in RC_ABOUT) + '</fieldset>')
    return "\n".join(out) + "\n"


if SHOW_READINESS: PAGES.append({
    "id": "ai-readiness", "path": "/ai-readiness/", "nav": None,
    "title": "AI readiness checklist for contract manufacturers | Grindstone",
    "description": "Could AI take the admin off your team's plate? Twelve quick statements for contract manufacturers, with your score and an action plan in about three minutes.",
    "jsonld": {"@context": "https://schema.org", "@type": "WebPage", "name": "AI readiness checklist", "url": SITE + "/ai-readiness/", "publisher": ORG},
    "body": """
    <div class="wrap page rc">
      <a class="back" href="{gemba_page}">Consultancy</a>
      <header class="big">
        <span class="kind">Free checklist</span>
        <h1 class="intro">Could AI take the admin off your team's plate?</h1>
        <p class="body">Start with one job that eats time every week, such as quoting, chasing suppliers or updating customers. Twelve quick statements show whether that job is ready to hand to an AI tool on a small trial, and what's in the way if it isn't.</p>
        <p class="body">About three minutes. Your score, and an action plan in order of what to fix first, appear as soon as you finish.</p>
      </header>
      <form id="rc-form" novalidate onsubmit="return false">
""" + rc_form() + """      <div class="rc-contact">
        <h3>Enter your email to see your score</h3>
        <div class="rc-fields">
          <label>Email <span class="req">(required)</span><input type="email" name="email" autocomplete="email" required></label>
          <label>Name<input type="text" name="name" autocomplete="name"></label>
          <label>Company<input type="text" name="company" autocomplete="organization"></label>
          <label>Role<input type="text" name="role" autocomplete="organization-title"></label>
        </div>
        <label class="rc-hp" aria-hidden="true">Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label>
        <label class="rc-optin"><input type="checkbox" name="call" value="yes"> I'd like a call to talk through my result.</label>
        <div class="rc-fields" id="rc-phone" hidden><label>Phone number <span class="req">(required for a call)</span><input type="tel" name="phone" autocomplete="tel" maxlength="30"></label></div>
        <label class="rc-optin"><input type="checkbox" name="news" value="yes"> Send me Grindstone's articles and free tools by email. You can unsubscribe at any time.</label>
        <p class="rc-small">We use your details to show and record your result and, if you ticked the box, to send you our articles. See our <a href="{link:privacy}">privacy notice</a>.</p>
        <p class="rc-error" id="rc-error" hidden></p>
        <button class="cta" type="submit" id="rc-submit">See my score</button>
      </div>
      </form>
      <section class="rc-result" id="rc-result" hidden aria-live="polite">
        <span class="kind">Your result</span>
        <p class="rc-score"><b id="rc-total">0</b> / 24</p>
        <h2 id="rc-band"></h2>
        <p id="rc-advice"></p>
        <div class="rc-bars" id="rc-bars"></div>
        <div class="rc-plan"><h3>Your action plan</h3><p class="rc-small">Work down the list. Anything marked Not true comes first, then the Partly items.</p><ol id="rc-plan"></ol></div>
        <p>If you'd like help choosing a first task and running the pilot, email <b>""" + MAIL + """</b>. Our <a href="{gemba_page}">free problem-solving templates</a> are on the Consultancy page.</p>
      </section>
    </div>
    <script>
    (function () {
      var URL_ = """ + '"{READINESS_URL}"' + """;
      var groups = ["Problem", "Data", "People", "Guardrails"];
      var fixes = {
        1: "Pick one specific, repetitive task that costs real time every week.",
        2: "Time the task as it's done today, and count how often it goes wrong.",
        3: "Get the senior team engaged in the process, and agree time for the pilot each week.",
        4: "Find where the task's information lives, and make sure it can be reached.",
        5: "Bring the key data up to date: lead times, prices, stock and open orders.",
        6: "List which data is customer-owned and covered by an NDA or export control.",
        7: "Involve the people who do the task today.",
        8: "Name one owner for the pilot and one person who checks the outputs.",
        9: "Tell staff which AI tools are approved, and which are not.",
        10: "Write a one-line rule on what the agent may and may not do.",
        11: "Make sure no agent can commit spend, change master data or make a promise to a customer.",
        12: "Decide where every agent output will be logged, so the work stays traceable for audit."
      };
      var form = document.getElementById("rc-form"), err = document.getElementById("rc-error");
      // Partly or True opens a short box asking for the detail
      form.addEventListener("change", function (ev) {
        if (ev.target.name === "call") { document.getElementById("rc-phone").hidden = !ev.target.checked; return; }
        if (!/^q\d+$/.test(ev.target.name)) return;
        ev.target.closest(".rc-q").querySelector(".rc-more").hidden = ev.target.value === "0";
      });
      form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        var d = new FormData(form), q = [], missing = 0;
        for (var i = 1; i <= 12; i++) { var v = d.get("q" + i); if (v === null) missing++; q.push(v === null ? null : Number(v)); }
        var email = String(d.get("email") || "").trim();
        if (missing) { err.textContent = "Please score all 12 statements (" + missing + " to go)."; err.hidden = false; return; }
        var emailBox = form.querySelector("input[name=email]");
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { err.textContent = "That doesn't look like a full email address. It needs an @ and a domain, for example name@company.co.uk."; err.hidden = false; emailBox.classList.add("rc-bad"); emailBox.focus(); return; }
        emailBox.classList.remove("rc-bad");
        var phoneBox = form.querySelector("input[name=phone]"), phone = String(d.get("phone") || "").trim();
        if (d.get("call") && (phone.match(/\d/g) || []).length < 10) { err.textContent = "Please add a phone number so we can call you, or untick the call box."; err.hidden = false; phoneBox.classList.add("rc-bad"); phoneBox.focus(); return; }
        phoneBox.classList.remove("rc-bad");
        err.hidden = true;
        var total = q.reduce(function (a, b) { return a + b; }, 0);
        var g = [0, 1, 2, 3].map(function (k) { return q[k * 3] + q[k * 3 + 1] + q[k * 3 + 2]; });
        var band, advice;
        if (total >= 18) { band = "Ready for a first pilot"; advice = "The basics are in place. Pick the task, write the pilot charter and start measuring how it runs today."; }
        else if (total >= 12) { band = "Nearly ready"; advice = "Close the gaps below first. Most can be fixed in a few weeks, without spending money."; }
        else { band = "Start with the basics"; advice = "An agent would struggle here today. Fix the lowest-scoring area first; the rest gets easier once it's done."; }
        // Action plan: every Not true in statement order, then every Partly; the final step is always the pilot itself
        var plan = [];
        [0, 1].forEach(function (score) { q.forEach(function (v, i) { if (v === score) plan.push(i + 1); }); });
        var fix = plan.length ? fixes[plan[0]] : "Nothing obvious. Choose the task and start.";
        var steps = plan.map(function (n) {
          return '<li><span class="rc-tag' + (q[n - 1] === 0 ? ' rc-tag-0' : '') + '">' + (q[n - 1] === 0 ? "Not true" : "Partly") + '</span>' +
            fixes[n] + '<small>' + groups[Math.floor((n - 1) / 3)] + ', statement ' + n + '</small></li>'; });
        steps.push('<li><span class="rc-tag rc-tag-go">Then</span>Choose the task, measure how it runs today, and start the pilot.</li>');
        document.getElementById("rc-total").textContent = total;
        document.getElementById("rc-band").textContent = band;
        document.getElementById("rc-advice").textContent = advice;
        document.getElementById("rc-plan").innerHTML = steps.join("");
        document.getElementById("rc-bars").innerHTML = groups.map(function (n, k) {
          return '<div><span>' + n + '</span><i><em style="width:' + (g[k] / 6 * 100) + '%"></em></i><b>' + g[k] + ' / 6</b></div>'; }).join("");
        var body = new URLSearchParams();
        ["email", "name", "company", "role", "website"].forEach(function (k) { body.append(k, String(d.get(k) || "").trim()); });
        body.append("news", d.get("news") ? "yes" : "no");
        body.append("call", d.get("call") ? "yes" : "no");
        if (d.get("call")) body.append("Phone", phone);
        q.forEach(function (v, i) { body.append("q" + (i + 1), v); });
        // Follow-ups that are showing, plus the business questions: ticks joined with "; "
        form.querySelectorAll(".rc-x").forEach(function (box) {
          if (box.hidden) return;
          var seen = {};
          box.querySelectorAll("[name]").forEach(function (el) {
            if (seen[el.name]) return; seen[el.name] = 1;
            body.append(el.name, d.getAll(el.name).map(function (x) { return String(x).trim(); }).filter(Boolean).join("; "));
          });
        });
        body.append("fields", Array.from(body.keys()).concat(["Action plan"]).join("|"));
        body.append("result", band); body.append("fix", fix);
        body.append("Action plan", plan.map(function (n, k) { return (k + 1) + ". " + fixes[n]; }).join("\\n")); body.append("page", location.href);
        if (URL_) { try { fetch(URL_, { method: "POST", mode: "no-cors", body: body }); } catch (e) {} }
        form.hidden = true;
        var r = document.getElementById("rc-result"); r.hidden = false; r.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    })();
    </script>""",
})

if SHOW_READINESS: PAGES.append({
    "id": "privacy", "path": "/privacy/", "nav": None,
    "title": "Privacy notice | Grindstone",
    "description": "How Grindstone Ltd collects, uses and protects personal information.",
    "jsonld": {"@context": "https://schema.org", "@type": "WebPage", "name": "Privacy notice", "url": SITE + "/privacy/", "publisher": ORG},
    "body": """
    <div class="wrap page">
      <a class="back" href="{home}">Home</a>
      <header class="big"><span class="kind">Legal</span><h1 class="intro">Privacy notice</h1></header>
      <div class="prose">
        <p><b>Who we are.</b> Grindstone Ltd (company number 17440074, registered in England and Wales, 8 Aldermans Hill, Hockley, Essex SS5 4RW) is responsible for the personal information described here. We are registered with the Information Commissioner's Office, registration number ZC285025. Contact us at """ + MAIL + """.</p>
        <h2>What we collect</h2>
        <ul><li>When you complete the AI readiness checklist: your email address, your name, company and role if you give them, your phone number if you ask us to call you, with your answers, any details you add, what you tell us about your business, whether you asked for a call, and your score.</li>
        <li>When you email us: your name, email address and anything you include in your message.</li>
        <li>When you visit the site: anonymous visit statistics through Cloudflare Web Analytics, which does not use cookies or identify you.</li></ul>
        <h2>How we use it, and why</h2>
        <ul><li>To show and record your checklist result, and to reply to you if you contact us. Our lawful basis is our legitimate interest in responding to people who ask for information about our services.</li>
        <li>To send you our articles and free tools by email, only if you ticked the box to ask for them. Our lawful basis is your consent, which you can withdraw at any time by replying to any email or writing to """ + MAIL + """.</li></ul>
        <p>We do not sell your information or share it with anyone for their own marketing.</p>
        <h2>Where it is kept</h2>
        <p>Checklist responses and emails are stored in our Google Workspace account. Google acts as our processor and may store data outside the UK under the safeguards required by UK data protection law.</p>
        <h2>How long we keep it</h2>
        <p>We keep checklist responses and enquiry emails for 24 months after your last contact with us, then delete them. If you withdraw consent to emails, we stop sending them straight away.</p>
        <h2>Your rights</h2>
        <p>You can ask to see, correct or delete the information we hold about you, object to how we use it, or withdraw consent. Email """ + MAIL + """. If you're unhappy with how we've handled your information, you can complain to the Information Commissioner's Office at ico.org.uk.</p>
        <p class="muted">Last updated 26 October 2026.</p>
      </div>
    </div>""",
})


# Large faint brand watermark behind each sub page (the home page has its own wheel in the hero)
MARKS = {
    "ems-directory": '<div class="wm-bg mark-ems" aria-hidden="true"><svg><use href="#ems-mark"/></svg></div>',
    "cnc-directory": '<div class="wm-bg mark-ems" aria-hidden="true"><svg><use href="#cnc-mark"/></svg></div>',
    "emc-directory": '<div class="wm-bg mark-ems" aria-hidden="true"><svg><use href="#emc-mark"/></svg></div>',
    "drumbeat": '<div class="wm-bg mark-drum" aria-hidden="true">+</div>',
    "consultancy": '<div class="wm-bg wheel" aria-hidden="true"></div>',
}


def page_body(p, links):
    body = fill_links(fill(p["body"], links), links)
    mark = MARKS.get(p["id"]) or (MARKS["consultancy"] if p["id"] == "blog" or p["id"].startswith("post-") else None)
    return f'<div class="pagewrap">{mark}{body}\n</div>' if mark else body


FOOTER = """
<footer>
  <div class="wrap">
    <nav aria-label="Our sites">
      <a href="{EMS}">EMS Directory</a>
      <a href="{drum_page}">drumbeat+</a>
      <a href="{gemba_page}">Consultancy</a>
      <a href="{link:blog}">Blog</a>
      <a class="li" href="{LINKEDIN}">""" + LI_ICON + """<span>LinkedIn</span></a>""" + ("""
      <a href="/privacy/">Privacy</a>""" if SHOW_READINESS else "") + """
      <a class="foot-mail" href="mailto:""" + CONTACT + """">""" + CONTACT + """</a>
    </nav>
    <p class="legal">Grindstone Ltd &middot; Registered in England and Wales, company no. 17440074 &middot; Registered office: 8 Aldermans Hill, Hockley, Essex SS5 4RW &middot; ICO registration ZC285025</p>
  </div>
</footer>"""


def header(links, current):
    items = "\n".join(
        f'      <a href="{links[p["id"]]}" data-nav="{p["id"]}"'
        + (' aria-current="page"' if p["id"] == current else "") + f'>{p["nav"]}</a>'
        for p in PAGES if p.get("nav"))
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
            .replace("{EMS}", EMS).replace("{CNC}", CNC).replace("{EMC}", EMC).replace("{DRUM}", DRUM).replace("{LINKEDIN}", LINKEDIN).replace("{LI_EMS}", LI_EMS).replace("{LI_DRUM}", LI_DRUM).replace("{LI_COLIN}", LI_COLIN).replace("{DEMO}", DEMO).replace("{READINESS_URL}", READINESS_URL))


def fill_links(text, links):
    return re.sub(r"\{link:([\w-]+)\}", lambda m: links[m.group(1)], text)


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=True) + "</script>"


# ---------------------------------------------------------------- real site (dist/)

def build_dist():
    global CF_BEACON
    CF_BEACON = ("<script type=\"module\" src=\"https://static.cloudflareinsights.com/beacon.min.js\" "
                 f"data-cf-beacon='{{\"token\": \"{CF_BEACON_TOKEN}\"}}'></script>") if CF_BEACON_TOKEN else ""
    links = {p["id"]: p["path"] for p in PAGES}
    out = ROOT / "docs"
    for p in PAGES:
        url = SITE + p["path"]
        og_img = f"{SITE}/og/{p['id']}.png" if (ROOT / "src/og" / f"{p['id']}.png").exists() else f"{SITE}/og-image.png"
        art = f'\n<meta property="article:published_time" content="{p["published"]}">' if p.get("published") else ""
        html = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['title']}</title>
<meta name="description" content="{p['description']}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{p.get('og_type', 'website')}">
<link rel="alternate" type="application/rss+xml" title="Grindstone blog" href="{SITE}/blog/feed.xml">
<meta property="og:site_name" content="Grindstone Ltd">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['description']}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_GB">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html_escape(p.get('og_alt', p['title']))}">{art}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{p['title']}">
<meta name="twitter:description" content="{p['description']}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{FONTS}
<style>
{CSS}
</style>
{jsonld(p['jsonld'])}
{CF_BEACON}
</head>
<body>
{EMS_SYMBOL}
{header(links, p['id'])}
<main>
{page_body(p, links)}
</main>
{fill_links(fill(FOOTER, links), links)}
</body>
</html>
"""
        target = out / p["path"].strip("/") / "index.html" if p["path"] != "/" else out / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
    urls = "\n".join(f"  <url><loc>{SITE}{p['path']}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES)
    # the free templates on the Consultancy page, so Google indexes the PDFs too
    urls += "".join(f"\n  <url><loc>{SITE}/downloads/{f.name}</loc><lastmod>{TODAY}</lastmod></url>"
                    for f in sorted((ROOT / "src/downloads").glob("*.pdf")))
    (out / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8")
    items = "".join(
        f"<item><title>{html_escape(p['title'])}</title><link>{SITE}/blog/{p['slug']}/</link><guid>{SITE}/blog/{p['slug']}/</guid>"
        f"<pubDate>{datetime.date.fromisoformat(p['date']).strftime('%a, %d %b %Y')} 09:00:00 +0000</pubDate>"
        f"<description>{html_escape(p['description'])}</description></item>" for p in POSTS)
    # remove pages for posts that are no longer built (drafts, future-dated, renamed), so nothing stale gets pushed
    live = {p["slug"] for p in POSTS}
    for d in (out / "blog").iterdir():
        if d.is_dir() and d.name not in live:
            shutil.rmtree(d)
    if not SHOW_CNC_PAGE:
        shutil.rmtree(out / "cnc-directory", ignore_errors=True)
    if not SHOW_EMC_PAGE:
        shutil.rmtree(out / "emc-directory", ignore_errors=True)
    if not SHOW_READINESS:
        for name in ("ai-readiness", "privacy"):
            shutil.rmtree(out / name, ignore_errors=True)
    (out / "blog" / "feed.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Grindstone blog</title><link>{SITE}/blog/</link>'
        f'<description>{html_escape(BLOG_DESC)}</description><language>en-gb</language>{items}</channel></rss>\n', encoding="utf-8")
    # favicon: the grindstone wheel from the logo
    for icon in (ROOT / "src/icons").iterdir():
        shutil.copy(icon, out / icon.name)
    (out / "downloads").mkdir(exist_ok=True)
    for pdf in (ROOT / "src/downloads").glob("*.pdf"):
        shutil.copy(pdf, out / "downloads" / pdf.name)
    (out / "blog-images").mkdir(exist_ok=True)
    for img in (ROOT / "src/blog-images").glob("*"):
        shutil.copy(img, out / "blog-images" / img.name)
    (out / "og").mkdir(exist_ok=True)
    for img in (ROOT / "src/og").glob("*.png"):
        shutil.copy(img, out / "og" / img.name)
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
{fill_links(fill(FOOTER, links), links)}

<script>
  (function () {{
    var pages = {ids};
    // The preview frame can reload with a stale hash, so remember the last page shown in this tab and reopen it
    var KEY = 'gs-preview-page', first = true;
    function show() {{
      var id = (location.hash || '#home').slice(1);
      if (first) {{
        first = false;
        try {{ var saved = sessionStorage.getItem(KEY); if (saved && pages.indexOf(saved) >= 0) id = saved; }} catch (e) {{}}
      }}
      if (pages.indexOf(id) < 0) id = 'home';
      try {{ sessionStorage.setItem(KEY, id); }} catch (e) {{}}
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
