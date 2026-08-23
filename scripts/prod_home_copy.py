#!/usr/bin/env python3
from pathlib import Path

p = Path("dantix-vision/index.html")
t = p.read_text(encoding="utf-8")

repls = [
    (
        "Mide solo con 4 marcadores ArUco. No hace falta ingresar ancho ni largo.",
        "Mide solo con 4 tarjetas Dantix. No hace falta ingresar ancho ni largo.",
    ),
    (
        "Beta · Solo ArUco · Sin medidas manuales",
        "Beta · Tarjetas Dantix · Sin medidas manuales",
    ),
]

changed = 0
for old, new in repls:
    if old in t:
        t = t.replace(old, new, 1)
        changed += 1
        print("ok", old)
    else:
        print("MISSING", old)

t = t.replace(
    "<title>Dantix Leather Vision v208</title>",
    "<title>Dantix Leather Vision v209</title>",
    1,
)

if changed == 0:
    raise SystemExit("no se aplico ningun cambio")

p.write_text(t, encoding="utf-8")
print("wrote html", p.stat().st_size, "changes", changed)

sw = Path("dantix-vision/sw.js")
s = sw.read_text(encoding="utf-8")
s = s.replace("service worker v208", "service worker v209")
s = s.replace("dantix-lv-v208-copy-1", "dantix-lv-v209-card-1")
sw.write_text(s, encoding="utf-8")
print("wrote sw")
