# -*- coding: utf-8 -*-
"""Genera gli asset SVG del profilo GitHub neural-rob.
   Nessuna dipendenza esterna: il testo usa textLength calcolato su metriche
   Helvetica-like, cosi' il layout regge qualunque font trovi il browser del visitatore."""
import os, xml.dom.minidom as md

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)
FONT = "Inter,&apos;Segoe UI&apos;,system-ui,-apple-system,Helvetica,Arial,sans-serif"

W = {**{c: w for c, w in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
      [.667,.667,.722,.722,.667,.611,.778,.722,.278,.5,.667,.556,.833,.722,
       .778,.667,.778,.722,.667,.611,.722,.667,.944,.667,.667,.611])},
     **{c: w for c, w in zip("abcdefghijklmnopqrstuvwxyz",
      [.556,.556,.5,.556,.556,.278,.556,.556,.222,.222,.5,.222,.833,.556,
       .556,.556,.556,.333,.5,.278,.556,.5,.722,.5,.5,.5])},
     **{" ": .278, "&": .667, "·": .333, ",": .278, ".": .278, "-": .333, "/": .278}}

def measure(text, size, weight=400, tracking=0.0):
    """Larghezza stimata in px, tracking in em."""
    f = 1.045 if weight >= 600 else 1.0
    return sum(W.get(c, .55) for c in text) * size * f + tracking * size * max(len(text) - 1, 0)

THEMES = {
    "light": dict(title="#17232B", accent="#4D7320", bar="#8DC642", body="#6E6E6E",
                  rule="#E3E7DE", stroke="#D8DDD3", fill="#FFFFFF",
                  text="#3E3E3E", label="#6E6E6E"),
    "dark":  dict(title="#E6EDF3", accent="#8DC642", bar="#8DC642", body="#8B949E",
                  rule="#21262D", stroke="#30363D", fill="#0D1117",
                  text="#C9D1D9", label="#8B949E"),
}

def txt(x, y, s, size, weight, fill, tracking=0.0, anchor=None):
    tl = round(measure(s, size, weight, tracking), 1)
    a = f' text-anchor="{anchor}"' if anchor else ""
    esc = s.replace("&", "&amp;")
    return (f'<text x="{x}" y="{y}"{a} font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" textLength="{tl}" '
            f'lengthAdjust="spacingAndGlyphs">{esc}</text>')

TITLE = "ROB O"
ROLE = "INFRASTRUCTURE & SECURITY ARCHITECT"
TAG = "Designing, securing and operating production-grade IT infrastructure."
FOOT = "NEURALNETWORK SRL · FIRENZE, IT"

def header(t):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 180" width="900" height="180" role="img" aria-label="Rob O - Infrastructure and Security Architect">
  <rect x="0" y="26" width="5" height="106" fill="{t['bar']}"/>
  {txt(28, 80, TITLE, 48, 700, t['title'], tracking=0.01)}
  {txt(30, 111, ROLE, 13.5, 600, t['accent'], tracking=0.155)}
  {txt(30, 140, TAG, 13.5, 400, t['body'])}
  <g stroke-width="2" stroke-linecap="square">
    <line x1="590" y1="66" x2="620" y2="66" stroke="{t['bar']}"/>
    <line x1="630" y1="66" x2="880" y2="66" stroke="{t['rule']}"/>
    <line x1="590" y1="88" x2="610" y2="88" stroke="{t['bar']}"/>
    <line x1="620" y1="88" x2="820" y2="88" stroke="{t['rule']}"/>
    <line x1="590" y1="110" x2="630" y2="110" stroke="{t['bar']}"/>
    <line x1="640" y1="110" x2="762" y2="110" stroke="{t['rule']}"/>
  </g>
  {txt(880, 142, FOOT, 10.5, 600, t['label'], tracking=0.08, anchor="end")}
</svg>
"""

ITEMS = ["Fortinet", "Cisco", "Linux", "Microsoft", "Azure", "AWS", "Cloudflare", "Ansible"]
FS, PAD, GAP, H, CW = 14.0, 15, 10, 32, 900

def stack(t):
    widths = [round(measure(s, FS, 500)) + 2 * PAD for s in ITEMS]
    x = (CW - (sum(widths) + GAP * (len(ITEMS) - 1))) / 2
    rows = []
    for s, w in zip(ITEMS, widths):
        rows.append(
            f'  <rect x="{x:.1f}" y="7" width="{w}" height="{H}" rx="4" fill="{t["fill"]}" '
            f'stroke="{t["stroke"]}" stroke-width="1"/>\n'
            f'  <rect x="{x:.1f}" y="7" width="3" height="{H}" rx="1.5" fill="{t["bar"]}"/>\n'
            f'  ' + txt(round(x + w / 2, 1), 28, s, FS, 500, t["text"], anchor="middle"))
        x += w + GAP
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} 46" width="{CW}" '
            f'height="46" role="img" aria-label="{", ".join(ITEMS)}">\n'
            + "\n".join(rows) + "\n</svg>\n")

for name, t in THEMES.items():
    open(f"{OUT}/header-{name}.svg", "w", encoding="utf-8").write(header(t))
    open(f"{OUT}/stack-{name}.svg", "w", encoding="utf-8").write(stack(t))

for fn in sorted(os.listdir(OUT)):
    md.parse(f"{OUT}/{fn}")
    print("OK", fn, os.path.getsize(f"{OUT}/{fn}"), "bytes")
