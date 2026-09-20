# -*- coding: utf-8 -*-
"""Genera gli asset SVG del profilo GitHub neural-rob.

Quattro pannelli scuri autoportanti (header, layers, stack, footer): stesso fondo,
stessa barra verde a sinistra, nessuna variante chiaro/scuro da mantenere.

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

W = 900          # larghezza logica di tutti i pannelli
BAR = 5          # barra verde a sinistra

# --------------------------------------------------------------- palette ---
INK = "#17232B"          # fondo pannello
EDGE = "#2A3A44"         # filetti interni
BRAND = "#8DC642"        # verde corporate — solo riempimento, mai testo su chiaro
TITLE = "#FFFFFF"
BODY = "#C3CFD5"
MUTED = "#7D8C94"
CHIP_BG = "#1C2A33"
CHIP_EDGE = "#33454F"
CHIP_TX = "#DCE4E8"

# -------------------------------------------------------------- metriche ---
_M = {
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


def w_sans(s, size, weight=400, tracking=0.0):
    f = 1.045 if weight >= 600 else 1.0
    return sum(_M.get(c, .55) for c in s) * size * f + tracking * size * max(len(s) - 1, 0)


def w_mono(s, size, tracking=0.0):
    return len(s) * 0.6 * size + tracking * size * max(len(s) - 1, 0)


def _text(family, width_fn, x, y, s, size, weight, fill, tracking, anchor):
    tl = round(width_fn(s, size, tracking) if family is MONO
               else width_fn(s, size, weight, tracking), 1)
    a = f' text-anchor="{anchor}"' if anchor else ""
    return (f'<text x="{x}" y="{y}"{a} font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" textLength="{tl}" '
            f'lengthAdjust="spacingAndGlyphs">{s.replace("&", "&amp;")}</text>')


def t_sans(x, y, s, size, weight, fill, tracking=0.0, anchor=None):
    return _text(SANS, w_sans, x, y, s, size, weight, fill, tracking, anchor)


def t_mono(x, y, s, size, weight, fill, tracking=0.0, anchor=None):
    return _text(MONO, w_mono, x, y, s, size, weight, fill, tracking, anchor)


def panel(h, body, label):
    """Cornice comune: fondo scuro a piena larghezza e barra verde a sinistra."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" '
            f'height="{h}" role="img" aria-label="{label}">\n'
            f'  <rect x="0" y="0" width="{W}" height="{h}" fill="{INK}"/>\n'
            f'  <rect x="0" y="0" width="{BAR}" height="{h}" fill="{BRAND}"/>\n'
            + body + "\n</svg>\n")


def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    md.parse(path)
    print("OK", name, os.path.getsize(path), "bytes")


# ---------------------------------------------------------------- header ---
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
    body = "\n".join([
        "  " + t_sans(38, 92, "ROB O", 52, 700, TITLE, tracking=0.01),
        "  " + t_sans(40, 126, "INFRASTRUCTURE & SECURITY ARCHITECT", 13, 600, BRAND, tracking=0.19),
        "  " + t_sans(40, 156, "Designing, securing and operating production-grade IT infrastructure.",
                      13.5, 400, "#95A3A9"),
        f'  <line x1="562" y1="56" x2="562" y2="140" stroke="{EDGE}" stroke-width="1"/>',
        f'  <line x1="678" y1="56" x2="678" y2="140" stroke="{EDGE}" stroke-width="1"/>',
    ] + rows)
    return panel(200, body,
                 "Rob O - Infrastructure and Security Architect, Neuralnetwork Srl, Firenze Italy")


# ------------------------------------------------ defense in depth (layers) ---
LAYERS = [
    ("PERIMETER",    "Next-gen firewalling, egress control and inbound exposure management"),
    ("SEGMENTATION", "Zoning, VLAN design and east-west policy to contain lateral movement"),
    ("IDENTITY",     "Directory hardening, MFA and conditional access as the real perimeter"),
    ("ACCESS",       "Remote access and privileged paths scoped to least privilege"),
    ("VISIBILITY",   "Monitoring, log retention and alerting that someone actually reads"),
    ("RECOVERY",     "Backup and disaster recovery, with restores tested before they matter"),
]
ROW = 40
TOP = 62


def layers():
    parts = [
        "  " + t_mono(38, 40, "DEFENSE IN DEPTH", 10.5, 600, BRAND, tracking=0.14),
        "  " + t_mono(862, 40, f"{len(LAYERS):02d} LAYERS", 10.5, 400, MUTED,
                      tracking=0.1, anchor="end"),
        f'  <line x1="38" y1="54" x2="862" y2="54" stroke="{EDGE}" stroke-width="1"/>',
    ]
    for i, (name, desc) in enumerate(LAYERS):
        cy = TOP + i * ROW + ROW / 2
        parts += [
            f'  <rect x="38" y="{cy - 6:.0f}" width="3" height="12" fill="{BRAND}"/>',
            "  " + t_mono(56, cy + 4, f"{i + 1:02d}", 11, 400, MUTED),
            "  " + t_mono(96, cy + 4.5, name, 12.5, 600, BRAND, tracking=0.07),
            "  " + t_sans(262, cy + 4.5, desc, 13.5, 400, BODY),
        ]
        if i < len(LAYERS) - 1:
            y = TOP + (i + 1) * ROW
            parts.append(f'  <line x1="56" y1="{y}" x2="862" y2="{y}" '
                         f'stroke="{EDGE}" stroke-width="1"/>')
    h = TOP + len(LAYERS) * ROW + 24
    return panel(h, "\n".join(parts),
                 "Defense in depth: " + "; ".join(f"{n}: {d}" for n, d in LAYERS))


# ------------------------------------------------------------ stack panel ---
STACK = [
    ("NETWORK & SECURITY", ["Fortinet", "Cisco", "Cloudflare", "Ubiquiti", "Cambium"]),
    ("PLATFORM & CLOUD",   ["Debian/Ubuntu", "Windows Server", "Microsoft 365", "Azure", "AWS"]),
    ("AUTOMATION & VOICE", ["Ansible", "Python", "Git", "LibreNMS", "3CX"]),
]
CFS, CPAD, CGAP, CH = 12.5, 16, 10, 30
COL = 240      # dove iniziano i chip
LBL = 216      # dove finisce la colonna etichette (allineata a destra)


def stack():
    flat_n = sum(len(i) for _, i in STACK)
    parts = [
        "  " + t_mono(38, 40, "TECHNOLOGY", 10.5, 600, BRAND, tracking=0.14),
        "  " + t_mono(862, 40, "IN PRODUCTION", 10.5, 400, MUTED, tracking=0.1, anchor="end"),
        f'  <line x1="38" y1="54" x2="862" y2="54" stroke="{EDGE}" stroke-width="1"/>',
    ]
    for r, (group, items) in enumerate(STACK):
        y = 72 + r * 42
        parts.append("  " + t_mono(LBL, y + 20, group, 10.5, 600, BRAND,
                                   tracking=0.1, anchor="end"))
        x = COL
        for s in items:
            w = round(w_mono(s, CFS)) + 2 * CPAD
            parts += [
                f'  <rect x="{x}" y="{y}" width="{w}" height="{CH}" rx="3" '
                f'fill="{CHIP_BG}" stroke="{CHIP_EDGE}" stroke-width="1"/>',
                f'  <rect x="{x}" y="{y}" width="3" height="{CH}" fill="{BRAND}"/>',
                "  " + t_mono(x + w / 2, y + 20, s, CFS, 500, CHIP_TX, anchor="middle"),
            ]
            x += w + CGAP
    h = 72 + len(STACK) * 42 + 12
    flat = [s for _, items in STACK for s in items]
    return panel(h, "\n".join(parts), "Technology: " + ", ".join(flat))


# ---------------------------------------------------------------- footer ---
def footer():
    body = "\n".join([
        "  " + t_sans(38, 54, "NEURALNETWORK SRL", 17, 700, TITLE, tracking=0.1),
        "  " + t_mono(40, 80, "IT & SECURITY SYSTEM INTEGRATOR", 10.5, 400, BRAND, tracking=0.1),
        "  " + t_sans(862, 54, "Infrastructure · Security · Cloud · Engineering",
                      13, 400, "#95A3A9", anchor="end"),
        "  " + t_mono(862, 80, "neuralnetwork.eu", 11, 400, "#E6EDF3", anchor="end"),
    ])
    return panel(110, body,
                 "Neuralnetwork Srl - IT and Security System Integrator, Firenze Italy")


if __name__ == "__main__":
    write("header.svg", header())
    write("layers.svg", layers())
    write("stack.svg", stack())
    write("footer.svg", footer())
