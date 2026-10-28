---
title: From DFMEA to PFMEA to Control Plan: Turning Design Risks into Process Controls
seo_title: DFMEA to PFMEA to Control Plan, Explained
date: 2026-10-30
kind: Article
description: How DFMEA, PFMEA, the control plan and SPC connect, what each one hands to the next, and how to keep the chain working in electronics manufacturing.
---

DFMEA, PFMEA, control plan and SPC are often written by different people at different times, and filed separately. They work best as one chain. Each document answers its own question and hands something to the next, so a risk found in design ends up as a check on the shop floor.

![From design risk to process control: DFMEA, PFMEA, control plan and SPC, and what passes between them](/blog-images/dfmea-pfmea-control-plan.png)

## 1. DFMEA: how could the design fail?

The design team works through how the product could fail to do its job, how serious each failure would be, and what causes it. The output that matters most downstream is the list of special characteristics: the dimensions, materials and features where variation would affect safety, compliance or function.

For an electronics assembly, that might be the retention force of a high-current connector, the creepage distance on a mains-side board, or the coating thickness on a board that has to survive condensation.

## 2. PFMEA: how could the process fail to build it right?

Process engineering takes each step of the process flow and asks how it could fail to deliver what the design needs. The special characteristics from the DFMEA get extra attention: for each one, the PFMEA should show how the process prevents the failure and how it would detect it if it happened anyway.

Using the connector example: the PFMEA covers the press-fit or soldering step, the causes of a weak joint (wrong tooling, worn tooling, insufficient solder) and the controls in place today.

## 3. Control plan: what do we check, how and how often?

The control plan turns the PFMEA's controls into a working list: each characteristic, how it's measured, the sample size and frequency, who checks it, and the reaction plan if it's out. If a control is in the PFMEA but not in the control plan, nobody is actually doing it.

For the connector, that could be a first-off and periodic pull test, a tooling check at each set-up, and AOI on every joint, with a clear instruction on what to do with suspect stock.

## 4. SPC and reaction: is the process staying in control?

For the characteristics that matter most, statistical process control shows whether the process is stable and capable, and warns of drift before parts go out of tolerance. Solder paste volume, reflow profiles and press-fit forces are common candidates in electronics assembly. When a chart signals, the reaction plan from the control plan says what happens next.

## Closing the loop

The chain only works if it runs both ways. Field returns, 8D findings and SPC trends should go back into the PFMEA, and lessons about what's hard to build should go back to the design team for the next product. A PFMEA that hasn't changed since launch is usually a sign this isn't happening.

## Keeping the chain intact

- **Use the same numbering for steps and characteristics** in all four documents, so each line can be traced.
- **Review them together** whenever the design or the process changes.
- **Score honestly.** A low occurrence score needs a real prevention control behind it.
- **Check the floor matches the paperwork** during layered or internal audits.

Our free [PFMEA template](/downloads/grindstone-pfmea-template.pdf) includes scoring guides and 75 rows of worksheet. If you'd like help building or reviewing PFMEAs and control plans for APQP or PPAP, see our [Consultancy page]({gemba_page}).
