#!/usr/bin/env python3
from pathlib import Path

p = Path("dantix-vision/index.html")
t = p.read_text(encoding="utf-8")

markers = [
    (
        '<div class="btn-row solo-escritorio">\n      <button class="ghost" id="btnResetCorners">Reiniciar puntos</button>',
        '<div class="btn-row" id="rowCalibAcciones">\n      <button class="ghost" type="button" id="btnUndoCorner">Quitar ultimo</button>\n      <button class="ghost" type="button" id="btnResetCorners">Reiniciar puntos</button>',
    ),
    (
        '<button class="ghost" id="btnDetectarAruco">',
        '<button class="ghost solo-escritorio" type="button" id="btnDetectarAruco">',
    ),
]

changed = 0
for old, new in markers:
    if old in t:
        t = t.replace(old, new, 1)
        changed += 1
        print("replaced", old[:60])
    else:
        print("MISSING", old[:80])

js_old = "document.getElementById('btnResetCorners').addEventListener('click', () => {"
undo = '''
document.getElementById('btnUndoCorner') && document.getElementById('btnUndoCorner').addEventListener('click', () => {
  if(!corners.length) return;
  corners.pop();
  draggingIndex = -1;
  hideLoupe();
  redrawOriginalWithCorners();
  updateCornerCount();
});
'''

if "btnUndoCorner').addEventListener" not in t and js_old in t:
    t = t.replace(js_old, undo + js_old, 1)
    changed += 1
    print("added undo listener")

t = t.replace("<title>Dantix Leather Vision v206</title>", "<title>Dantix Leather Vision v207</title>", 1)

if changed == 0:
    raise SystemExit("no se aplico ningun cambio")

p.write_text(t, encoding="utf-8")
print("wrote", p.stat().st_size, "changes", changed)
