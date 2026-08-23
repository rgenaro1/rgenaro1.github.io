#!/usr/bin/env python3
from pathlib import Path

p = Path("dantix-vision/index.html")
t = p.read_text(encoding="utf-8")

repls = [
    (
        "<h2>Elige cómo quieres trabajar</h2>",
        "<h2>Elige qué vas a hacer</h2>",
    ),
    (
        "<p>Cuatro herramientas. Empieza por la que necesitas hoy.</p>",
        "<p>Manta o molde. Cada tarjeta hace una cosa distinta.</p>",
    ),
    (
        "Toma la foto de la manta y obtén el área real en segundos.",
        "Recepción en planta. Fotografías la manta, marcas las esquinas y obtienes el área.",
    ),
    (
        "Rápido · Simple · En planta",
        "Celular · Área · Registro",
    ),
    (
        "Revisa defectos, zonas, moldes y el rendimiento de corte.",
        "Control en escritorio. Defectos, zonas de la manta y acomodo de corte.",
    ),
    (
        "Completo · Analítico · Profesional",
        "Escritorio · Calidad · Rendimiento",
    ),
    (
        "Mide solo con 4 tarjetas Dantix. No hace falta ingresar ancho ni largo.",
        "Medición con Dantix Card. Las 4 tarjetas dan la escala; no ingresas ancho ni largo.",
    ),
    (
        "Beta · Tarjetas Dantix · Sin medidas manuales",
        "Beta · Dantix Card · Sin cinta",
    ),
    (
        "Digitaliza moldes y descarga un DXF para tu software CAD.",
        "Piezas de molde a DXF. Para el CAD. Esta opción no mide mantas.",
    ),
    (
        "Piezas de molde · Contorno real · DXF",
        "Molde · Contorno · DXF",
    ),
]

changed = 0
for old, new in repls:
    if old in t:
        t = t.replace(old, new, 1)
        changed += 1
        print("ok", old[:72])
    else:
        print("MISSING", old[:80])

t = t.replace(
    "<title>Dantix Leather Vision v209</title>",
    "<title>Dantix Leather Vision v210</title>",
    1,
)

if changed == 0:
    raise SystemExit("no se aplico ningun cambio")

p.write_text(t, encoding="utf-8")
print("wrote html", p.stat().st_size, "changes", changed)

sw = Path("dantix-vision/sw.js")
s = sw.read_text(encoding="utf-8")
s = s.replace("service worker v209", "service worker v210")
s = s.replace("dantix-lv-v209-card-1", "dantix-lv-v210-cards-1")
sw.write_text(s, encoding="utf-8")
print("wrote sw")
