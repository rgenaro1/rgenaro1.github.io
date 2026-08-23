#!/usr/bin/env python3
from pathlib import Path

HIDE = """  body.modo-escritorio.studio-medir #step5,
  body.modo-escritorio.studio-medir #step6,
  body.modo-escritorio.studio-medir #step7,
  body.modo-escritorio.studio-medir #step8{display:none !important;}
  body.modo-escritorio.studio-inspeccionar #step1,
  body.modo-escritorio.studio-inspeccionar #step2,
  body.modo-escritorio.studio-inspeccionar #step3,
  body.modo-escritorio.studio-inspeccionar #step4,
  body.modo-escritorio.studio-inspeccionar #step7,
  body.modo-escritorio.studio-inspeccionar #step8{display:none !important;}
  body.modo-escritorio.studio-rendimiento #step1,
  body.modo-escritorio.studio-rendimiento #step2,
  body.modo-escritorio.studio-rendimiento #step3,
  body.modo-escritorio.studio-rendimiento #step4,
  body.modo-escritorio.studio-rendimiento #step5,
  body.modo-escritorio.studio-rendimiento #step6{display:none !important;}
"""

OLD_JS = """document.getElementById('studioStages') && document.getElementById('studioStages').addEventListener('click', (ev) => {
  const btn = ev.target.closest('.studio-stage-btn');
  if(!btn) return;
  document.body.classList.remove('studio-medir', 'studio-inspeccionar', 'studio-rendimiento');
  document.body.classList.add('studio-' + btn.dataset.stage);
  document.querySelectorAll('.studio-stage-btn').forEach(b => b.classList.toggle('is-on', b === btn));
});"""

NEW_JS = """document.getElementById('studioStages') && document.getElementById('studioStages').addEventListener('click', (ev) => {
  const btn = ev.target.closest('.studio-stage-btn');
  if(!btn) return;
  document.querySelectorAll('.studio-stage-btn').forEach(b => b.classList.toggle('is-on', b === btn));
  const dest = {medir:'step1', inspeccionar:'step5', rendimiento:'step7'}[btn.dataset.stage];
  const el = dest && document.getElementById(dest);
  if(el){
    el.classList.remove('disabled');
    el.scrollIntoView({behavior:'smooth', block:'start'});
  }
});"""

OLD_FIT = """function fitCanvas(canvas, w, h, maxW){
  canvas.width = w; canvas.height = h;
  // width:100% + height:auto deja que el navegador escale manteniendo la proporción real
  // de la imagen sin importar qué tan angosto sea el contenedor.
  canvas.style.width = '100%';
  canvas.style.height = 'auto';
  canvas.style.maxWidth = maxW + 'px';
  return Math.min(1, maxW / w);
}"""

NEW_FIT = """function fitCanvas(canvas, w, h, maxW){
  const movil = window.innerWidth < 900 || /iPhone|iPad|iPod|Android/i.test(navigator.userAgent||'');
  const MAX = movil ? 2000 : 2800;
  const scale = Math.min(1, MAX / Math.max(w, h, 1));
  canvas.width = Math.max(1, Math.round(w * scale));
  canvas.height = Math.max(1, Math.round(h * scale));
  canvas.style.width = '100%';
  canvas.style.height = 'auto';
  canvas.style.maxWidth = maxW + 'px';
  return scale;
}"""


def patch_lab(p: Path):
    t = p.read_text(encoding="utf-8")
    n = 0
    if HIDE in t:
        t = t.replace(HIDE, "  /* Studio: las pestañas solo sugieren, no ocultan pasos */\n")
        n += 1
        print("lab hide css removed")
    else:
        print("lab hide css already gone or missing")
    if OLD_JS in t:
        t = t.replace(OLD_JS, NEW_JS, 1)
        n += 1
        print("lab stage js scroll")
    else:
        print("lab stage js missing/changed")
    old_av = "VisionStudio está pensado para PC. En el celular usa Recepción rápida."
    new_av = "Sugerencia: VisionStudio se ve mejor en PC. En el celular puedes seguir aquí o usar Recepción rápida."
    if old_av in t:
        t = t.replace(old_av, new_av, 1)
        n += 1
        print("lab aviso")
    old_st = '<div id="studioStages" class="solo-escritorio" style="display:flex;gap:8px;flex-wrap:wrap;margin:8px 16px 16px;">'
    new_st = (
        '<p class="hint solo-escritorio" style="margin:4px 16px 0;">Sugerencia: puedes saltar a esa parte. Los demás pasos (incluido nesting) siguen visibles.</p>\n'
        + old_st
    )
    if old_st in t and "Los demás pasos" not in t:
        t = t.replace(old_st, new_st, 1)
        n += 1
        print("lab hint")
    t = t.replace("<title>Dantix Leather Vision LAB v221</title>", "<title>Dantix Leather Vision LAB v222</title>")
    t = t.replace("<title>Dantix Leather Vision LAB v220</title>", "<title>Dantix Leather Vision LAB v222</title>")
    p.write_text(t, encoding="utf-8")
    sw = p.parent / "sw.js"
    if sw.exists():
        s = sw.read_text(encoding="utf-8")
        s = s.replace("LAB v221", "LAB v222").replace("LAB v220", "LAB v222")
        s = s.replace("dantix-lv-lab-v221-fototeca", "dantix-lv-lab-v222-studio")
        s = s.replace("dantix-lv-lab-v220-mejoras-1", "dantix-lv-lab-v222-studio")
        sw.write_text(s, encoding="utf-8")
        print("lab sw")
    print("lab ops", n)
    if n < 1:
        raise SystemExit("lab: no changes")


def patch_prod(p: Path):
    t = p.read_text(encoding="utf-8")
    n = 0
    if OLD_FIT in t:
        t = t.replace(OLD_FIT, NEW_FIT, 1)
        n += 1
        print("prod fitCanvas")
    else:
        print("prod fitCanvas missing")
    old1 = """    fitCanvas(canvasOriginal, img.width, img.height, 700);
    const ctx = canvasOriginal.getContext('2d');
    ctx.drawImage(img, 0, 0, img.width, img.height);"""
    new1 = """    const iw = img.naturalWidth || img.width, ih = img.naturalHeight || img.height;
    fitCanvas(canvasOriginal, iw, ih, 700);
    const ctx = canvasOriginal.getContext('2d', {alpha:false});
    ctx.drawImage(img, 0, 0, canvasOriginal.width, canvasOriginal.height);"""
    if old1 in t:
        t = t.replace(old1, new1, 1)
        n += 1
        print("prod manta draw")
    old2 = """        ctx.drawImage(img, 0, 0, img.width, img.height);"""
    new2 = """        ctx.drawImage(img, 0, 0, canvasOriginal.width, canvasOriginal.height);"""
    if old2 in t:
        t = t.replace(old2, new2, 1)
        n += 1
        print("prod manta raf")
    old3 = """      fitCanvas(canvasMoldeOriginal, img.width, img.height, 700);
      const ctx = canvasMoldeOriginal.getContext('2d');
      ctx.drawImage(img, 0, 0, img.width, img.height);"""
    new3 = """      const iw = img.naturalWidth || img.width, ih = img.naturalHeight || img.height;
      fitCanvas(canvasMoldeOriginal, iw, ih, 700);
      const ctx = canvasMoldeOriginal.getContext('2d', {alpha:false});
      ctx.drawImage(img, 0, 0, canvasMoldeOriginal.width, canvasMoldeOriginal.height);"""
    if old3 in t:
        t = t.replace(old3, new3, 1)
        n += 1
        print("prod molde draw")
    if "ctx.drawImage(img, 0, 0, img.width, img.height)" in t:
        t = t.replace(
            "ctx.drawImage(img, 0, 0, img.width, img.height)",
            "ctx.drawImage(img, 0, 0, canvasMoldeOriginal.width, canvasMoldeOriginal.height)",
            1,
        )
        n += 1
        print("prod molde raf")
    t = t.replace("<title>Dantix Leather Vision v213</title>", "<title>Dantix Leather Vision v214</title>", 1)
    p.write_text(t, encoding="utf-8")
    sw = p.parent / "sw.js"
    if sw.exists():
        s = sw.read_text(encoding="utf-8")
        s = s.replace("service worker v213", "service worker v214")
        s = s.replace("dantix-lv-v213-pattern-1", "dantix-lv-v214-canvas-1")
        sw.write_text(s, encoding="utf-8")
        print("prod sw")
    print("prod ops", n)
    if n < 2:
        raise SystemExit("prod: few changes")


if __name__ == "__main__":
    patch_lab(Path("dantix-vision-lab/index.html"))
    patch_prod(Path("dantix-vision/index.html"))
    print("ok")
