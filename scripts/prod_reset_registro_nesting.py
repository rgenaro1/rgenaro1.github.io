#!/usr/bin/env python3
"""Produccion: vaciar el cuadro de NESTING al empezar una nueva recepcion."""
from pathlib import Path

HTML = Path("dantix-vision/index.html")
SW = Path("dantix-vision/sw.js")
t = HTML.read_text(encoding="utf-8")

RESET = """    window._recepcion = null;
    window._nuevaMantaDatos = null;
    window._nuevaMantaCreada = false;
    window._ultimoNestImage = null;
    window._ultimoNestPares = null;
    try {
      if (typeof registroCompleto !== 'undefined' && Array.isArray(registroCompleto)) {
        registroCompleto.length = 0;
        if (typeof renderLogCompleto === 'function') renderLogCompleto();
      }
    } catch (e) {}
    const logWrap = document.getElementById('logCompletoWrap');
    if (logWrap) {
      logWrap.style.display = 'none';
      const logBody = document.getElementById('logCompletoBody');
      if (logBody) logBody.innerHTML = '';
    }
"""

OLD = """    window._recepcion = null;
    window._nuevaMantaDatos = null;
    window._nuevaMantaCreada = false;
"""

if "logCompletoWrap" in t and "registroCompleto.length = 0" in t and "iniciarNuevaRecepcionCompleta" in t:
    print("already patched")
else:
    if OLD not in t:
        raise SystemExit("anchor iniciarNuevaRecepcionCompleta not found")
    # only the first occurrence inside iniciarNuevaRecepcionCompleta
    idx = t.find("function iniciarNuevaRecepcionCompleta")
    if idx < 0:
        raise SystemExit("iniciarNuevaRecepcionCompleta not found")
    local = t.find(OLD, idx)
    if local < 0:
        raise SystemExit("null recepcion block not found inside function")
    t = t[:local] + RESET + t[local + len(OLD):]
    print("patched iniciarNuevaRecepcionCompleta")

for a, b in (
    ("<title>Dantix Leather Vision v222</title>", "<title>Dantix Leather Vision v223</title>"),
    ("Dantix Leather Vision v222", "Dantix Leather Vision v223"),
):
    if a in t:
        t = t.replace(a, b, 1)
        print("version", b)

HTML.write_text(t, encoding="utf-8")
print("html", HTML.stat().st_size)

if SW.exists():
    sw = SW.read_text(encoding="utf-8")
    sw = sw.replace("service worker v222", "service worker v223")
    sw = sw.replace("dantix-lv-v222", "dantix-lv-v223")
    SW.write_text(sw, encoding="utf-8")
    print("sw ok")
print("ok")
