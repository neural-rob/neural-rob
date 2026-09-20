# -*- coding: utf-8 -*-
"""Genera gli asset SVG del profilo GitHub neural-rob.

Nessuna dipendenza esterna e nessun servizio di terze parti: ogni testo porta un
textLength calcolato su metriche Helvetica-like (sans) e su avanzamento fisso
0.6em (mono), cosi' il layout regge qualunque font trovi il browser del visitatore.

    python3 tools/gen-assets.py
"""
import os
import xml.dom.minidom as md

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

SANS = "Inter,&apos;Segoe UI&apos;,system-ui,-apple-system,Helvetica,Arial,sans-serif"
MONO = "&apos;IBM Plex Mono&apos;,ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

# ---------------------------------------------------------------- metriche ---
_W = {
    **{c: w for c, w in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
       [.667, .667, .722, .722, .667, .611, .778, .722, .278, .5, .667, .556, .833,
        .722, .778, .667, .778, .722, .667, .611, .722, .667, .944, .667, .667, .611])},
    **{c: w for c, w in zip("abcdefghijklmnopqrstuvwxyz",
       [.556, .556, .5, .556, .556, .278, .556, .556, .222, .222, .5, .222, .833,
        .556, .556, .556, .556, .333, .5, .278, .556, .5, .722, .5, .5, .5])},
    **{c: w for c, w in zip("0123456789", [.556] * 10)},
    " ": .278, "&": .667, "·": .333, ",": .278, ".": .278, "-": .333,
    "/": .278, "(": .333, ")": .333, "+": .584, ":": .278,
}


def w_sans(text, size, weight=400, tracking=0.0):
    f = 1.045 if weight >= 600 else 1.0
    return sum(_W.get(c, .55) for c in text) * size * f + tracking * size * max(len(text) - 1, 0)


def w_mono(text, size, tracking=0.0):
    return len(text) * 0.6 * size + tracking * size * max(len(text) - 1, 0)


def t_sans(x, y, s, size, weight, fill, tracking=0.0, anchor=None):
    tl = round(w_sans(s, size, weight, tracking), 1)
    a = f' text-anchor="{anchor}"' if anchor else ""
    return (f'<text x="{x}" y="{y}"{a} font-family="{SANS}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" textLength="{tl}" '
            f'lengthAdjust="spacingAndGlyphs">{s.replace("&", "&amp;")}</text>')


def t_mono(x, y, s, size, weight, fill, tracking=0.0, anchor=None):
    tl = round(w_mono(s, size, tracking), 1)
    a = f' text-anchor="{anchor}"' if anchor else ""
    return (f'<text x="{x}" y="{y}"{a} font-family="{MONO}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" textLength="{tl}" '
            f'lengthAdjust="spacingAndGlyphs">{s.replace("&", "&amp;")}</text>')


def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    md.parse(path)
    print("OK", name, os.path.getsize(path), "bytes")


# ------------------------------------------------------------------ palette ---
INK = "#17232B"        # slab
INK_EDGE = "#2A3A44"   # filetti dentro lo slab
BRAND = "#8DC642"      # verde corporate, solo riempimento
LIGHT = {
    "accent": "#4D7320", "text": "#3E3E3E", "muted": "#8A938D",
    "rule": "#E3E7DE", "chip_bg": "#FFFFFF", "chip_edge": "#D8DDD3", "chip_tx": "#3E3E3E",
}
DARK = {
    "accent": "#8DC642", "text": "#C9D1D9", "muted": "#6E7681",
    "rule": "#21262D", "chip_bg": "#0D1117", "chip_edge": "#30363D", "chip_tx": "#C9D1D9",
}

# ------------------------------------------------------------------- header ---
META = [
    ("LOCATION", "Firenze, Italy"),
    ("COMPANY",  "Neuralnetwork Srl"),
    ("FOCUS",    "Infrastructure & Security"),
]


def header():
    rows = []
    for i, (k, v) in enumerate(META):
        y = 80 + i * 26
        rows.append("  " + t_mono(586, y, k, 10.5, 600, BRAND, tracking=0.12))
        rows.append("  " + t_mono(694, y, v, 11, 400, "#E6EDF3"))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 200" width="900" height="200" role="img" aria-label="Rob O - Infrastructure and Security Architect, Neuralnetwork Srl, Firenze Italy">
  <rect x="0" y="0" width="900" height="200" fill="{INK}"/>
  <rect x="0" y="0" width="5" height="200" fill="{BRAND}"/>
  {t_sans(38, 92, "ROB O", 52, 700, "#FFFFFF", tracking=0.01)}
  {t_sans(40, 126, "INFRASTRUCTURE & SECURITY ARCHITECT", 13, 600, BRAND, tracking=0.19)}
  {t_sans(40, 156, "Designing, securing and operating production-grade IT infrastructure.", 13.5, 400, "#95A3A9")}
  <line x1="562" y1="56" x2="562" y2="140" stroke="{INK_EDGE}" stroke-width="1"/>
  <line x1="678" y1="56" x2="678" y2="140" stroke="{INK_EDGE}" stroke-width="1"/>
{chr(10).join(rows)}
</svg>
"""


# ------------------------------------------------- defense in depth (layers) ---
LAYERS = [
    ("PERIMETER",    "Next-gen firewalling, egress control and inbound exposure management"),
    ("SEGMENTATION", "Zoning, VLAN design and east-west policy to contain lateral movement"),
    ("IDENTITY",     "Directory hardening, MFA and conditional access as the real perimeter"),
    ("ACCESS",       "Remote access and privileged paths scoped to least privilege"),
    ("VISIBILITY",   "Monitoring, log retention and alerting that someone actually reads"),
    ("RECOVERY",     "Backup and disaster recovery, with restores tested before they matter"),
]
ROW_H = 40


def layers(t):
    h = ROW_H * len(LAYERS) + 8
    parts = [f'  <line x1="8" y1="6" x2="8" y2="{h - 10}" stroke="{t["rule"]}" stroke-width="2"/>']
    for i, (name, desc) in enumerate(LAYERS):
        y = 6 + i * ROW_H
        cy = y + ROW_H / 2
        parts += [
            f'  <rect x="4" y="{cy - 7:.0f}" width="9" height="14" fill="{t["accent"]}"/>',
            "  " + t_mono(34, cy + 4, f"{i + 1:02d}", 11, 400, t["muted"]),
            "  " + t_mono(72, cy + 4.5, name, 12.5, 600, t["accent"], tracking=0.07),
            "  " + t_sans(236, cy + 4.5, desc, 13.5, 400, t["text"]),
        ]
        if i < len(LAYERS) - 1:
            parts.append(f'  <line x1="34" y1="{y + ROW_H}" x2="892" y2="{y + ROW_H}" '
                         f'stroke="{t["rule"]}" stroke-width="1"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {h}" width="900" '
            f'height="{h}" role="img" aria-label="'
            + "; ".join(f"{n}: {d}" for n, d in LAYERS) + '">\n'
            + "\n".join(parts) + "\n</svg>\n")


# -------------------------------------------------------------- stack strip ---
STACK = [
    ["Fortinet", "Cisco", "Cloudflare", "Ubiquiti", "Cambium", "3CX"],
    ["Debian/Ubuntu", "Windows Server", "Microsoft 365", "Azure", "AWS", "Ansible"],
]
CHIP_FS, CHIP_PAD, CHIP_GAP, CHIP_H, CW = 12.5, 16, 10, 30, 900


def stack(t):
    h = len(STACK) * (CHIP_H + 10) + 4
    parts = []
    for r, row in enumerate(STACK):
        widths = [round(w_mono(s, CHIP_FS)) + 2 * CHIP_PAD for s in row]
        x = (CW - (sum(widths) + CHIP_GAP * (len(row) - 1))) / 2
        y = 4 + r * (CHIP_H + 10)
        for s, w in zip(row, widths):
            parts += [
                f'  <rect x="{x:.1f}" y="{y}" width="{w}" height="{CHIP_H}" rx="3" '
                f'fill="{t["chip_bg"]}" stroke="{t["chip_edge"]}" stroke-width="1"/>',
                f'  <rect x="{x:.1f}" y="{y}" width="3" height="{CHIP_H}" fill="{t["accent"]}"/>',
                "  " + t_mono(round(x + w / 2, 1), y + 20, s, CHIP_FS, 500,
                              t["chip_tx"], anchor="middle"),
            ]
            x += w + CHIP_GAP
    flat = [s for row in STACK for s in row]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {h}" width="{CW}" '
            f'height="{h}" role="img" aria-label="{", ".join(flat)}">\n'
            + "\n".join(parts) + "\n</svg>\n")


# ------------------------------------------------------------------- footer ---
def footer():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 110" width="900" height="110" role="img" aria-label="Neuralnetwork Srl - IT and Security System Integrator, Firenze Italy">
  <rect x="0" y="0" width="900" height="110" fill="{INK}"/>
  <rect x="0" y="0" width="900" height="3" fill="{BRAND}"/>
  {t_sans(38, 54, "NEURALNETWORK SRL", 17, 700, "#FFFFFF", tracking=0.1)}
  {t_mono(40, 80, "IT & SECURITY SYSTEM INTEGRATOR", 10.5, 400, BRAND, tracking=0.1)}
  {t_sans(862, 54, "Infrastructure · Security · Cloud · Engineering", 13, 400, "#95A3A9", anchor="end")}
  {t_mono(862, 80, "neuralnetwork.eu", 11, 400, "#E6EDF3", anchor="end")}
</svg>
"""


if __name__ == "__main__":
    write("header.svg", header())
    write("footer.svg", footer())
    for name, theme in (("light", LIGHT), ("dark", DARK)):
        write(f"layers-{name}.svg", layers(theme))
        write(f"stack-{name}.svg", stack(theme))
