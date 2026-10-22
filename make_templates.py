"""Free problem-solving templates as branded, fillable A4 PDFs.

Each template is laid out in HTML (site fonts and colours), printed to PDF by headless Chrome, then every
write-in box gets a fillable form field: each box carries a tiny marker word, PyMuPDF finds the marker,
takes the box drawn around it as the field's size, and removes the marker.

Run:  python3 make_templates.py      ->  src/downloads/*.pdf  (build.py copies them to docs/downloads/)
"""
import pathlib
import subprocess
import tempfile

import fitz  # PyMuPDF

import build as b

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = b.ROOT / "src/downloads"
MARK = f'<span class="gs">Grind<span>{b.STONE}</span></span>'

CSS = """
@page { size: A4; margin: 13mm 13mm 15mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: "Instrument Sans", "Helvetica Neue", Arial, sans-serif; font-size: 8.6pt; line-height: 1.38; color: #1b2125; }
.gs { font-family: "Michroma", sans-serif; text-transform: uppercase; letter-spacing: .03em; font-size: 13pt; color: #1b2125; white-space: nowrap; }
.gs > span { color: #d9661a; }
.o-wheel { display: inline-block; width: .782em; height: .782em; margin: 0 .092em 0 -.01em; vertical-align: -.016em; color: #3d464c; }
.o-wheel svg { display: block; width: 100%; height: 100%; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
.top { display: flex; justify-content: space-between; align-items: center; padding-bottom: 3mm; border-bottom: 2.5px solid #d9661a; }
.top .tag { font-size: 7.5pt; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: #59646b; }
h1 { font-family: "Archivo", sans-serif; font-weight: 800; font-size: 22pt; line-height: 1.05; letter-spacing: -.01em; margin: 5mm 0 1.5mm; }
.lead { color: #59646b; font-size: 9.5pt; margin: 0 0 4mm; max-width: 165mm; }
.meta { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2mm 3mm; margin-bottom: 4mm; }
.meta label, .cell label { display: block; font-size: 6.8pt; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: #59646b; margin-bottom: .8mm; }
.box { border: .9px solid #b9c0c3; border-radius: 1.5mm; background: #fbfbfb; position: relative; }
.line { height: 7.5mm; }
.how { border-left: 3px solid #d9661a; background: #f6efe9; padding: 3mm 4mm; margin-bottom: 4mm; border-radius: 0 1.5mm 1.5mm 0; }
.how strong { font-family: "Archivo", sans-serif; font-size: 9.5pt; }
.how ol { margin: 1.5mm 0 0; padding-left: 4.5mm; display: grid; gap: .8mm; }
.step { break-inside: avoid; display: grid; grid-template-columns: 62mm 1fr; gap: 4mm; padding: 3.2mm 0; border-top: .8px solid #d2d7d9; }
.step h2 { grid-column: 1 / -1; margin: 0; font-family: "Archivo", sans-serif; font-weight: 800; font-size: 12pt; display: flex; gap: 2.5mm; align-items: baseline; }
.step h2 b { color: #d9661a; font-size: 13pt; min-width: 8mm; }
.step h2 span { font-family: "Instrument Sans", sans-serif; font-weight: 500; font-size: 8pt; color: #59646b; }
.guide { color: #3b454b; }
.guide p { margin: 0 0 1.2mm; }
.guide ul { margin: 0; padding-left: 3.6mm; display: grid; gap: .7mm; }
.guide .tip { margin-top: 1.6mm; color: #59646b; font-style: italic; }
.write { display: grid; gap: 2mm; align-content: start; }
.tbl { display: grid; gap: 1.2mm; }
.tbl .hd { display: grid; gap: 1.2mm; font-size: 6.8pt; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: #59646b; }
.tbl .row { display: grid; gap: 1.2mm; }
.tbl .row .box { height: 6.5mm; }
.fm { font-size: 1pt; color: #fbfbfb; position: absolute; left: 1mm; top: 1mm; line-height: 1; }
.step.one { display: block; }
.step.one .guide { margin: 2mm 0 3mm; }
.m4 { display: grid; grid-template-columns: 17mm repeat(4, 1fr); gap: 1.2mm 2mm; align-items: center; }
.m4 b { font-family: "Archivo", sans-serif; font-size: 10pt; display: grid; }
.m4 b em { font-style: normal; font-family: "Instrument Sans", sans-serif; font-weight: 500; font-size: 6.8pt; color: #59646b; }
.m4 .wl { font-size: 7pt; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: #59646b; }
.m4 .wl:nth-last-of-type(1) { color: #d9661a; }
.help { break-inside: avoid; margin-top: 4mm; background: #1b2125; color: #eceeee; border-radius: 1.5mm; padding: 4mm 5mm; display: grid; gap: 1mm; }
.help strong { font-family: "Archivo", sans-serif; font-size: 11pt; color: #fff; }
.help b { color: #f08a3a; font-weight: 600; }
"""


def box(name, height_mm=None, multiline=True, cls=""):
    style = f' style="height:{height_mm}mm"' if height_mm else ""
    return f'<div class="box {cls}"{style}><span class="fm">F{"M" if multiline else "S"}_{name}</span></div>'


def table(name, cols, widths, rows):
    tpl = f'grid-template-columns:{" ".join(widths)}'
    head = f'<div class="hd" style="{tpl}">' + "".join(f"<span>{c}</span>" for c in cols) + "</div>"
    body = "".join(
        f'<div class="row" style="{tpl}">' + "".join(box(f"{name}_r{r}c{c}", multiline=False) for c in range(len(cols))) + "</div>"
        for r in range(1, rows + 1))
    return f'<div class="tbl">{head}{body}</div>'


def step(num, title, sub, guide, write):
    return f"""<section class="step"><h2><b>{num}</b>{title}<span>{sub}</span></h2>
<div class="guide">{guide}</div><div class="write">{write}</div></section>"""


def page(title, lead, meta, how, steps, file_title, help_title, help_text, extra_css=""):
    meta_html = "".join(f'<div><label>{m}</label>{box("meta_" + str(i), multiline=False, cls="line")}</div>'
                        for i, m in enumerate(meta))
    how_html = "".join(f"<li>{h}</li>" for h in how)
    return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{file_title}</title>
{b.FONTS.replace('display=swap', 'display=block')}<style>{CSS}{extra_css}</style></head><body>
<div class="top">{MARK}<span class="tag">Free problem-solving template</span></div>
<h1>{title}</h1><p class="lead">{lead}</p>
<div class="meta">{meta_html}</div>
<div class="how"><strong>How to use this template</strong><ol>{how_html}</ol></div>
{''.join(steps)}
<div class="help"><strong>{help_title}</strong><span>{help_text}</span><span><b>enquiries@grindstone.ltd</b> &middot; grindstone.ltd/consultancy</span></div>
</body></html>"""


# ---------------------------------------------------------------- 8D

def eight_d():
    S = []
    S.append(step("D0", "Prepare and plan", "Is this an 8D problem, and is the customer protected now?", """
<p>Decide whether the problem needs a full 8D. Use it when the problem is new or repeating, the cause is unknown, or the customer has asked for one.</p>
<ul><li>Record the first report: who found it, where and when.</li><li>Take emergency action straight away if the customer or the line is at risk.</li></ul>
<p class="tip">An emergency action protects the customer today. It is not the fix.</p>""",
        box("d0", 22)))
    S.append(step("D1", "Form the team", "The people with the knowledge and authority to fix it", """
<ul><li>Pick a team leader and a champion (the manager who removes blockers).</li><li>Include the people closest to the process: operator, engineer, quality, and buying if parts are involved.</li><li>Keep it to 4 to 6 people.</li></ul>""",
        table("d1", ["Name", "Role on team", "Department"], ["1fr", "1fr", "1fr"], 5)))
    S.append(step("D2", "Describe the problem", "In facts and numbers, not opinions", """
<p>Answer each question in the box:</p>
<ul><li><b>What</b> is wrong, on which part number and revision?</li><li><b>Where</b> was it found, and where on the assembly?</li><li><b>When</b> did it start? Date code, lot or serial range.</li><li><b>How many</b> are affected, and what proportion?</li><li><b>How</b> was it found? Test, inspection or customer.</li></ul>
<p class="tip">Add what the problem is NOT, for example "only line 2" or "only lot 4417". It narrows the search later.</p>""",
        box("d2", 46)))
    S.append(step("D3", "Contain the problem", "Stop more bad parts reaching the customer while you find the cause", """
<ul><li>Quarantine suspect stock everywhere: work in progress, finished goods, in transit, and at the customer.</li><li>Sort, screen or add an extra inspection.</li><li>Check the containment is working, and record the results.</li></ul>""",
        table("d3", ["Containment action", "Owner", "Date", "Result"], ["2.2fr", "1fr", ".8fr", "1fr"], 4)))
    S.append(step("D4", "Find the root cause", "Why it happened, and why it wasn't caught", """
<p>Find two causes:</p>
<ul><li><b>Occurrence:</b> why the defect was made.</li><li><b>Escape:</b> why your checks didn't catch it.</li></ul>
<p>Use 5 Whys or a fishbone diagram. Then prove the cause: switch it on and off and see the problem follow.</p>
<p class="tip">"Operator error" is rarely the root cause. Ask why the process allowed it.</p>""",
        '<div><label style="font-size:6.8pt;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#59646b">Occurrence root cause</label>' + box("d4a", 24) + "</div>"
        + '<div><label style="font-size:6.8pt;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#59646b">Escape root cause</label>' + box("d4b", 18) + "</div>"
        + '<div><label style="font-size:6.8pt;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#59646b">How the cause was proven</label>' + box("d4c", 14) + "</div>"))
    S.append(step("D5", "Choose permanent corrective actions", "One action for each root cause", """
<ul><li>Choose an action that removes each cause, both occurrence and escape.</li><li>Prove it works before rolling it out, with a trial build or test.</li><li>Check it doesn't create a new problem somewhere else.</li></ul>""",
        table("d5", ["Corrective action", "Root cause it fixes", "Owner", "Due"], ["2fr", "1.4fr", ".9fr", ".7fr"], 4)))
    S.append(step("D6", "Put the actions in and confirm", "Then remove the containment", """
<ul><li>Implement the actions and record the date and the first lot or serial number built after the change.</li><li>Show the results: defect rate before and after, and audit results.</li><li>Only remove the D3 containment once the data shows the fix works.</li></ul>""",
        box("d6", 32)))
    S.append(step("D7", "Prevent it happening again", "Here and on similar products and processes", """
<ul><li>Update the PFMEA, control plan, work instructions and training records.</li><li>Read across: apply the fix to similar parts, lines and sites.</li><li>Record the lesson so the next team starts from it.</li></ul>""",
        table("d7", ["Document or process updated", "Reference / revision", "Done"], ["2fr", "1.3fr", ".7fr"], 4)))
    S.append(step("D8", "Recognise the team and close", "Agree the problem is solved", """
<ul><li>Confirm with the customer that they accept the closure.</li><li>Thank the team and say what they achieved.</li><li>Sign off and file the report.</li></ul>""",
        table("d8", ["Closed by", "Customer acceptance", "Date closed"], ["1fr", "1.2fr", ".8fr"], 1)))
    return page(
        "8D Problem Solving Report",
        "A structured way to find the real cause of a problem, fix it, and stop it coming back. Work through D0 to D8 in order and don't skip ahead to a fix.",
        ["8D report number", "Customer", "Part number and revision", "Date opened", "Team leader", "Customer reference"],
        ["Type straight into the boxes on screen, or print it and write by hand. Long text shrinks to fit its box.",
         "Read the guidance on the left of each step before filling in the box on the right.",
         "Save a copy with your report number in the file name, and send it to your customer at D3 (containment) and again at D8 (closure).",
         "Keep evidence (photos, data, test results) with the report. Most customers will ask for it."],
        S, "8D Problem Solving Report | Grindstone",
        "Stuck on a root cause, or need an 8D your customer will accept?",
        "Grindstone runs 8D investigations alongside your team, on site or remotely, at a fixed price agreed before we start.")


LABEL = '<label style="display:block;font-size:6.8pt;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#59646b;margin-bottom:.8mm">{}</label>'


def labelled(text, name, h):
    return "<div>" + LABEL.format(text) + box(name, h) + "</div>"


# ---------------------------------------------------------------- 5 Whys

def five_whys():
    ms = [("Man", "people, skills, training"), ("Machine", "equipment, tooling, software"),
          ("Method", "procedures, instructions"), ("Material", "components, PCBs, consumables")]
    grid = ('<div class="m4"><span></span>' + "".join(f"<b>{m}<em>{h}</em></b>" for m, h in ms)
            + "".join(f'<span class="wl">Why {i}</span>' + "".join(box(f"why{i}_{m[0].lower()}{m[1:3]}", 10.5) for m, _ in ms)
                      for i in range(1, 6))
            + '<span class="wl">Root cause?</span>' + "".join(box(f"root_{m[0].lower()}{m[1:3]}", 9) for m, _ in ms) + "</div>")
    S = [
        step("1", "State the problem", "One sentence, in facts", """
<p>Write what is wrong, where and how often, as a fact you could check.</p>
<ul><li>Good: "12 of 400 assemblies failed functional test on lot 4417, all at connector J3."</li><li>Weak: "Quality is poor on the new product."</li></ul>""",
             box("problem", 18)),
        """<section class="step one" style="break-inside:auto"><h2><b>2</b>Ask why, five times, across the 4Ms<span>Man, Machine, Method, Material</span></h2>
<div class="guide"><ul><li>Look at the problem through each of the four Ms in turn. In each column, ask why it happened, and write the answer as a fact.</li><li>Ask why again about that answer, and keep going down the column until you reach a cause you can act on, usually by the fifth why. Leave a column empty if that M plays no part.</li><li>Stay with the process. If an answer becomes a person ("the operator forgot"), ask why the process allowed it.</li><li>Mark the root cause in the bottom row. Often only one or two Ms lead to it.</li></ul></div>
<div class="write">""" + grid + """</div></section>""",
        step("3", "Check the chain backwards", "Read it from the bottom up", """
<p>Read from the last why back to the problem, saying "and therefore" between each line. If any link doesn't follow, the chain is broken: go back and check that step.</p>
<p>Then prove the root cause with data or a trial, where you can.</p>""",
             labelled("How the root cause was checked", "check", 18)),
        step("4", "Fix it", "One action for the root cause, one for why it wasn't caught", """
<ul><li>Choose an action that removes the root cause, not one that only deals with the symptom.</li><li>Ask one more question: why didn't our checks catch it? Add an action for that too.</li><li>Give every action an owner and a date.</li></ul>""",
             table("act", ["Action", "Owner", "Due", "Done"], ["2.4fr", "1fr", ".8fr", ".6fr"], 4)),
    ]
    return page(
        "5 Whys Root Cause Analysis",
        "A quick way to get from a problem to its root cause: ask why, through each of the 4Ms, until you reach something you can fix.",
        ["Reference", "Part number or process", "Date", "Led by", "Customer (if any)", "Linked 8D or NCR"],
        ["Type straight into the boxes on screen, or print it and write by hand.",
         "Do it with the people who know the process, at the place where the problem happened if you can.",
         "Write facts, not opinions or blame. Every answer should be something you could check.",
         "For problems with many possible causes, start with a fishbone diagram, then use 5 Whys on the likeliest causes."],
        S, "5 Whys Root Cause Analysis | Grindstone",
        "Going round in circles on a recurring problem?",
        "Grindstone leads root cause investigations alongside your team, on site or remotely, at a fixed price agreed before we start.")


# ---------------------------------------------------------------- Fishbone

FISH_CSS = """
@page { size: A4 landscape; margin: 10mm 12mm 14mm; }
h1 { margin-top: 3.5mm; }
.lead { margin-bottom: 3mm; }
.meta { grid-template-columns: repeat(6, 1fr); margin-bottom: 3mm; }
.how { padding: 2.2mm 4mm; margin-bottom: 3mm; }
.fish { position: relative; height: 106mm; margin: 0 0 3mm; break-inside: avoid; }
.fish svg.bones { position: absolute; inset: 0; width: 100%; height: 100%; }
.fish .cat { position: absolute; width: 62mm; display: grid; gap: 1mm; }
.fish .cat b { font-family: "Archivo", sans-serif; font-size: 10pt; }
.fish .cat b span { font-family: "Instrument Sans", sans-serif; font-weight: 500; font-size: 7pt; color: #59646b; margin-left: 1.5mm; }
.fish .cat .box { height: 27mm; }
.fish .head { position: absolute; right: 0; top: 38mm; width: 52mm; display: grid; gap: 1mm; }
.fish .head b { font-family: "Archivo", sans-serif; font-size: 10pt; color: #d9661a; }
.fish .head .box { height: 28mm; border: 1.6px solid #d9661a; }
"""


def fishbone():
    cats = [("Man", "people, skills, training"), ("Machine", "equipment, tooling, software"), ("Method", "procedures, work instructions"),
            ("Material", "components, PCBs, consumables"), ("Measurement", "test, inspection, calibration"), ("Environment", "temperature, humidity, ESD")]
    pos = [(0, 0), (66, 0), (132, 0), (0, 74), (66, 74), (132, 74)]   # mm: left, top
    cat_html = "".join(
        f'<div class="cat" style="left:{x}mm;top:{y}mm"><b>{n}<span>{hint}</span></b>{box("cat" + str(i), 27)}</div>'
        for i, ((n, hint), (x, y)) in enumerate(zip(cats, pos)))
    bones = ('<svg class="bones" viewBox="0 0 273 106" preserveAspectRatio="none" aria-hidden="true">'
             '<line x1="4" y1="53" x2="218" y2="53" stroke="#1b2125" stroke-width="1.4"/>'
             + "".join(f'<line x1="{x + 31}" y1="{33 if y == 0 else 72}" x2="{x + 52}" y2="53" stroke="#59646b" stroke-width=".8"/>' for x, y in pos)
             + '<polygon points="214,49 221,53 214,57" fill="#1b2125"/></svg>')
    diagram = f'<div class="fish">{bones}{cat_html}<div class="head"><b>Problem (the effect)</b>{box("effect", 28)}</div></div>'
    likely = """<section class="step" style="grid-template-columns:62mm 1fr;break-before:page"><h2><b>Next</b>Pick the likeliest causes and test them<span>Don't fix anything until a cause is proven</span></h2>
<div class="guide"><ul><li>Circle the causes the team thinks most likely, using data where you have it.</li><li>Test each one: change it and see if the problem follows.</li><li>Take proven causes into 5 Whys or your 8D.</li></ul></div><div class="write">""" + \
        table("test", ["Likely cause", "How we'll test it", "Owner", "Result"], ["1.6fr", "1.8fr", ".8fr", "1.2fr"], 4) + "</div></section>"
    return page(
        "Fishbone (Ishikawa) Diagram",
        "Brainstorm every possible cause of a problem in six groups, so nothing is missed before you start testing.",
        ["Reference", "Part number or process", "Date", "Led by", "Team", "Linked 8D or NCR"],
        ["Write the problem in the orange box on the right, as a fact (what, where, how many).",
         "With the team, list possible causes in each of the six boxes. Every idea goes down at this stage: no arguing yet.",
         "Then pick the likeliest causes and test them, using the table on page 2."],
        [diagram, likely], "Fishbone (Ishikawa) Diagram | Grindstone",
        "Too many possible causes and no clear answer?",
        "Grindstone runs root cause workshops with your team, on site or remotely, at a fixed price agreed before we start.",
        FISH_CSS)


# ---------------------------------------------------------------- PFMEA

PFMEA_CSS = """
@page { size: A4 landscape; margin: 11mm 11mm 14mm; }
.scales { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; margin-bottom: 4mm; break-inside: avoid; }
.scales div { border: .8px solid #d2d7d9; border-radius: 1.5mm; padding: 2mm 3mm; }
.scales b { font-family: "Archivo", sans-serif; font-size: 9.5pt; display: block; margin-bottom: .8mm; }
.scales b em { font-style: normal; color: #d9661a; }
.fmea .hd span { font-size: 6pt; letter-spacing: .04em; }
.fmea .row .box { height: 9mm; }
"""


def pfmea():
    scales = """<div class="scales">
<div><b><em>S</em> Severity, 1 to 10</b>How bad is the effect if it happens? 10 = safety or legal risk without warning. 7–8 = product doesn't work, customer very unhappy. 4–6 = works but degraded. 1 = no noticeable effect.</div>
<div><b><em>O</em> Occurrence, 1 to 10</b>How likely is the cause, with today's prevention controls? 10 = almost certain. 5–6 = occasional. 1 = prevented by design, for example mistake-proofing.</div>
<div><b><em>D</em> Detection, 1 to 10</b>How likely are today's checks to catch it before it leaves? 10 = no check at all. 5–6 = manual inspection. 1 = automatic check that can't miss.</div>
</div>"""
    cols = ["Process step", "Function / requirement", "Failure mode", "Effect", "S", "Cause", "Prevention controls", "O",
            "Detection controls", "D", "RPN or AP", "Recommended action", "Owner / due"]
    widths = ["1.1fr", "1.2fr", "1.2fr", "1.2fr", ".35fr", "1.2fr", "1.2fr", ".35fr", "1.2fr", ".35fr", ".55fr", "1.3fr", ".9fr"]
    tbl = '<div class="fmea">' + table("pf", cols, widths, 10) + "</div>"
    guide = """<section class="step" style="grid-template-columns:1fr"><h2><b>Fill</b>One row per failure mode<span>Work through the process in order, step by step</span></h2>
<div class="write">""" + tbl + "</div></section>"
    return page(
        "Process FMEA (PFMEA)",
        "Find where each process step could fail, how bad that would be, and what stops it, before it happens on the line.",
        ["FMEA number", "Process or line", "Part number and revision", "Prepared by", "Team", "Date / revision"],
        ["Take the steps from your process flow, in order. For each step, ask how it could fail to meet its requirement.",
         "For each failure mode, write the effect on the customer, the cause, and the controls you have today. Then score S, O and D using the scales below.",
         "Prioritise by RPN (S × O × D), or by Action Priority if your customer follows the AIAG & VDA FMEA Handbook. Always act on high severity first, whatever the total.",
         "Re-score after each action, and keep the PFMEA in step with your control plan and work instructions. Add rows or pages as needed."],
        [scales, guide], "Process FMEA | Grindstone",
        "Need a PFMEA your customer will sign off?",
        "Grindstone builds and reviews PFMEAs and control plans with your team, for APQP and PPAP, at a fixed price agreed before we start.",
        PFMEA_CSS)


TEMPLATES = {"grindstone-8d-problem-solving-template": eight_d,
             "grindstone-5-whys-template": five_whys,
             "grindstone-fishbone-diagram-template": fishbone,
             "grindstone-pfmea-template": pfmea}


def make_fillable(pdf_in, pdf_out):
    doc = fitz.open(pdf_in)
    count = 0
    for page in doc:
        rects = [d["rect"] for d in page.get_drawings() if d.get("rect") and d["rect"].width > 15 and d["rect"].height > 8]
        for w in page.get_text("words"):
            word = w[4]
            if not word.startswith(("FM_", "FS_")):
                continue
            pt = fitz.Point(w[0], w[1])
            inside = [r for r in rects if r.contains(pt)]
            if not inside:
                continue
            r = min(inside, key=lambda r: r.width * r.height)
            page.add_redact_annot(fitz.Rect(w[:4]), fill=False)
            widget = fitz.Widget()
            widget.field_name = word[3:]
            widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            widget.rect = fitz.Rect(r.x0 + 1, r.y0 + 1, r.x1 - 1, r.y1 - 1)
            widget.text_font = "Helv"
            widget.text_fontsize = 0 if word.startswith("FM_") else 8   # 0 = shrink to fit for long text
            if word.startswith("FM_"):
                widget.field_flags = fitz.PDF_TX_FIELD_IS_MULTILINE
            widget.border_width = 0
            page.add_widget(widget)
            count += 1
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    n = len(doc)
    for i, page in enumerate(doc):
        y = page.rect.height - 22
        page.insert_text((37, y), "Free template from Grindstone Ltd  ·  grindstone.ltd/consultancy  ·  enquiries@grindstone.ltd",
                         fontsize=6.8, fontname="helv", color=(0.35, 0.39, 0.42))
        right = f"© Grindstone Ltd. Free to use and share.   Page {i + 1} of {n}"
        page.insert_text((page.rect.width - 37 - fitz.get_text_length(right, "helv", 6.8), y), right,
                         fontsize=6.8, fontname="helv", color=(0.35, 0.39, 0.42))
    doc.set_metadata({"title": doc.metadata.get("title") or "", "author": "Grindstone Ltd", "subject": "Free problem-solving template",
                      "creator": "Grindstone Ltd, grindstone.ltd"})
    doc.save(pdf_out, garbage=3, deflate=True)
    return count


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for slug, fn in TEMPLATES.items():
            src = pathlib.Path(tmp) / f"{slug}.html"
            raw = pathlib.Path(tmp) / f"{slug}.raw.pdf"
            src.write_text(fn(), encoding="utf-8")
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000",
                            f"--print-to-pdf={raw}", src.as_uri()], check=True, capture_output=True)
            n = make_fillable(str(raw), str(OUT / f"{slug}.pdf"))
            print(slug, "fields:", n)
