#!/usr/bin/env python3
from pathlib import Path

p = Path("dantix-vision/index.html")
t = p.read_text(encoding="utf-8")

repls = [
    (
        "<h1>Entrá a trabajar.<span class=\"accent\">Medí o digitalizá ahora.</span></h1>",
        "<h1>Empieza a trabajar.<span class=\"accent\">Mide o digitaliza ahora.</span></h1>",
    ),
    (
        "<p class=\"mode-sub\">Taller primero: elegí la herramienta y seguí. Marketing abajo, si lo necesitás.</p>",
        "<p class=\"mode-sub\">Elige la herramienta y comienza. Más abajo está el detalle del proceso.</p>",
    ),
    (
        "<b>Instalá Dantix en el teléfono</b>",
        "<b>Instala Dantix en el teléfono</b>",
    ),
    (
        "Queda como app, con icono en la pantalla de inicio. Sigue 100% local.",
        "Queda como una app, con icono en la pantalla de inicio. Todo se procesa en el teléfono.",
    ),
    (
        "<h2>Elige cómo quieres trabajar hoy</h2>",
        "<h2>Elige cómo quieres trabajar</h2>",
    ),
    (
        "<p>Herramientas diseñadas para cada etapa de tu proceso.</p>",
        "<p>Cuatro herramientas. Empieza por la que necesitas hoy.</p>",
    ),
    (
        "Captura y mide mantas al instante. Obtén el área real y crea el registro digital en segundos.",
        "Toma la foto de la manta y obtén el área real en segundos.",
    ),
    (
        "Inspección técnica completa: defectos, zonas, moldes, rendimiento y nesting real.",
        "Revisa defectos, zonas, moldes y el rendimiento de corte.",
    ),
    (
        "Mide fácilmente con Intelligent Measure de Dantix: solo 4 marcadores ArUco, sin ingresar ancho ni largo.",
        "Mide solo con 4 marcadores ArUco. No hace falta ingresar ancho ni largo.",
    ),
    (
        "Digitaliza tus moldes y descarga en un archivo estándar DXF compatible con tu software CAD.",
        "Digitaliza moldes y descarga un DXF para tu software CAD.",
    ),
    (
        "<h2>Una cámara. Un clic. Control total.</h2>",
        "<h2>De la foto al reporte, en cinco pasos.</h2>",
    ),
    (
        "Cada paso del proceso, asistido por visión por computadora — de la foto al reporte trazable.",
        "Tomas la foto en planta. El sistema corrige, mide, clasifica y deja el registro.",
    ),
    (
        "<h2>El control de recepción se paga solo.</h2>",
        "<h2>Mides lo que entra y pagas lo que corresponde.</h2>",
    ),
    (
        "Cada manta se mide con exactitud, no con la palabra del proveedor.",
        "Cada manta se mide en planta, no con la cifra del proveedor.",
    ),
]

changed = 0
missing = []
for old, new in repls:
    if old in t:
        t = t.replace(old, new, 1)
        changed += 1
        print("ok", old[:70])
    else:
        missing.append(old[:80])
        print("MISSING", old[:80])

t = t.replace(
    "<title>Dantix Leather Vision v207</title>",
    "<title>Dantix Leather Vision v208</title>",
    1,
)
t = t.replace(
    "<title>Dantix Leather Vision v206</title>",
    "<title>Dantix Leather Vision v208</title>",
    1,
)

if changed == 0:
    raise SystemExit("no se aplico ningun cambio")

p.write_text(t, encoding="utf-8")
print("wrote", p.stat().st_size, "changes", changed, "missing", len(missing))
