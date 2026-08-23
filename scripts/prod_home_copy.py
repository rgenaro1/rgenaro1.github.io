#!/usr/bin/env python3
from pathlib import Path

p = Path("dantix-vision/index.html")
t = p.read_text(encoding="utf-8")

repls = [
    (
        "Para instalarla tenés que servirla por HTTPS (o localhost), no abrir el HTML como archivo.",
        "Para instalarla hay que abrirla por HTTPS (o localhost), no como archivo HTML.",
    ),
    (
        "Instalá Dantix como app. El motor y los datos siguen en este dispositivo.",
        "Instala Dantix como app. El motor y los datos siguen en este dispositivo.",
    ),
    (
        "Si no aparece el diálogo, usá el menú del navegador → Instalar app / Agregar a pantalla de inicio.",
        "Si no aparece el diálogo, usa el menú del navegador → Instalar app / Agregar a pantalla de inicio.",
    ),
]

changed = 0
for old, new in repls:
    if old in t:
        t = t.replace(old, new, 1)
        changed += 1
        print("ok", old[:70])
    else:
        print("MISSING", old[:80])

if changed == 0:
    raise SystemExit("no se aplico ningun cambio")

p.write_text(t, encoding="utf-8")
print("wrote", p.stat().st_size, "changes", changed)
