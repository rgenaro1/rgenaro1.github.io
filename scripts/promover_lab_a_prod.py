#!/usr/bin/env python3
from pathlib import Path

src = Path("dantix-vision-lab/index.html")
dst = Path("dantix-vision/index.html")
t = src.read_text(encoding="utf-8")
t = t.replace(
    '<div id="labBanner">VERSION DE PRUEBA · no modifica produccion</div>\n',
    "",
)
t = t.replace("Dantix Leather Vision LAB v222", "Dantix Leather Vision v222")
t = t.replace("LAB v222", "v222")
if 'id="labBanner"' in t:
    raise SystemExit("lab banner still present")
if "VERSION DE PRUEBA" in t:
    raise SystemExit("prueba text still present")
dst.write_text(t, encoding="utf-8")
print("prod html", dst.stat().st_size)

sw = Path("dantix-vision-lab/sw.js").read_text(encoding="utf-8")
sw = (
    sw.replace("service worker LAB v222", "service worker v222")
    .replace("LAB v222", "v222")
    .replace("dantix-lv-lab-v222-studio", "dantix-lv-v222")
)
Path("dantix-vision/sw.js").write_text(sw, encoding="utf-8")
print("prod sw", Path("dantix-vision/sw.js").read_text(encoding="utf-8").split("\n")[:2])
print("ok promote")
