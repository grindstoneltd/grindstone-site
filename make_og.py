"""Social share images (og:image), one per page, 1200 x 630.

Each card reuses the site's own CSS and wordmarks, so product names always appear in their brand style.
Run after changing a page headline or adding a blog post:  python3 make_og.py && python3 build.py
Images land in src/og/<page id>.png; build.py copies them to docs/og/ and points og:image at them.
"""
import pathlib
import subprocess
import tempfile

import build as b

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = b.ROOT / "src/og"

MARK = f'<span class="mark">Grind<span>{b.STONE}</span></span>'

CARD_CSS = """
  html, body { margin: 0; width: 1200px; height: 630px; overflow: hidden; background: var(--bg); }
  .card { position: relative; width: 1200px; height: 630px; overflow: hidden; }
  .card .wheel { position: absolute; width: 980px; right: -430px; top: -175px; opacity: .55; animation: none; }
  .card .in { position: absolute; left: 80px; top: 76px; right: 330px; bottom: 76px; display: grid; align-content: start; gap: 34px; }
  .card .brand { line-height: 1; }
  .card .brand .mark { font-size: 40px; color: var(--fg); }
  .card .brand .wm-ems { font-size: 54px; }
  .card .brand .wm-drum { font-size: 66px; }
  .card .eyebrow { font-size: 22px; letter-spacing: .14em; margin-left: 1.2em; vertical-align: .3em; }
  .card h1 { font-family: var(--font-display); font-weight: 800; font-size: 70px; line-height: 1.04; letter-spacing: -.02em; color: var(--fg); margin: 0; text-wrap: balance; }
  .card h1.long { font-size: 56px; }
  .card h1 em { font-style: normal; color: var(--spark); }
  .card .url { position: absolute; left: 80px; bottom: 60px; font-size: 24px; font-weight: 600; color: var(--muted); }
"""


def card(brand, headline, path, long=False):
    return f"""<!doctype html><html lang="en-GB" data-theme="light"><head><meta charset="utf-8">
{b.FONTS.replace('display=swap', 'display=block')}
<style>{b.CSS}{CARD_CSS}</style></head><body>{b.EMS_SYMBOL}
<div class="card"><div class="wheel"></div>
  <div class="in"><div class="brand">{brand}</div><h1{' class="long"' if long else ''}>{headline}</h1></div>
  <div class="url">grindstone.ltd{path if path != '/' else ''}</div>
</div></body></html>"""


def cards():
    yield "home", card(MARK, '<span class="nowrap">Cutting-edge</span> solutions for <em>contract manufacturing.</em>', "/")
    yield "ems-directory", card(b.EMS_WM, "Find the UK EMS partner that fits the job.", "/ems-directory/")
    yield "cnc-directory", card(b.CNC_WM, "Find the UK machine shop that fits the job.", "/cnc-directory/")
    yield "emc-directory", card(b.EMC_WM, "Find the UK EMC test lab that fits the product.", "/emc-directory/")
    yield "drumbeat", card(b.DRUM_WM + b.TM, "Your ERP keeps the books. " + b.DRUM_WM + " keeps the beat.", "/drumbeat/")
    yield "consultancy", card(MARK + '<span class="eyebrow">Consultancy</span>', "Contract manufacturing consultancy, remotely or on your shop floor.", "/consultancy/")
    yield "ai-readiness", card(MARK + '<span class="eyebrow">Free checklist</span>',
                               "Could AI take the admin off your team&rsquo;s <em>plate?</em>", "/ai-readiness/")
    yield "blog", card(MARK + '<span class="eyebrow">Blog</span>',
                       f'Nose to the <span class="wm-inline">Grind<span>{b.STONE}</span></span>.', "/blog/")
    for p in b.POSTS:
        yield "post-" + p["slug"], card(MARK + '<span class="eyebrow">Blog</span>', b.brand_heading(b.html_escape(p["title"])),
                                        f"/blog/{p['slug']}/", long=len(p["title"]) > 48)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for pid, html in cards():
            src = pathlib.Path(tmp) / f"{pid}.html"
            src.write_text(html, encoding="utf-8")
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                            "--window-size=1200,630", "--virtual-time-budget=8000",
                            f"--screenshot={OUT / (pid + '.png')}", src.as_uri()],
                           check=True, capture_output=True)
            print("og", pid)
