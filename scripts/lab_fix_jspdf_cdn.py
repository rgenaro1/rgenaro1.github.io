#!/usr/bin/env python3
"""LAB v227: cargar jsPDF/QR desde CDN si el embebido no está disponible + reparar blob jsPDF."""
from pathlib import Path

HTML = Path("dantix-vision-lab/index.html")
SW = Path("dantix-vision-lab/sw.js")
t = HTML.read_text(encoding="utf-8")

if "LAB v227" in t and "jspdf@2.5.1" in t and "cdnFallback" in t:
    print("already patched v227")
else:
    # 1) Reparar newline extra dentro del blob jsPDF (corrupción conocida)
    old_corrupt = "<\\/script>\n</body></html>"
    new_clean = "<\\/script></body></html>"
    if old_corrupt in t:
        t = t.replace(old_corrupt, new_clean, 1)
        print("fixed jspdf embedded newline corruption")
    else:
        print("no jspdf newline corruption found (ok)")

    # 2) Reemplazar asegurar* por versión con fallback CDN
    old_aseg = """  function asegurarQRCode(){
    if(typeof qrcode === 'undefined') throw new Error('El generador de QR no está disponible en este archivo.');
  }
  function asegurarJsPDF(){
    if(!window.jspdf || !window.jspdf.jsPDF) throw new Error('El generador de PDF no está disponible en este archivo.');
  }"""

    new_aseg = r"""  function loadScriptOnce(src, globalCheck){
    return new Promise(function(resolve, reject){
      try{
        if(globalCheck()){ resolve(true); return; }
      }catch(e){}
      var existing = document.querySelector('script[data-dantix-cdn="'+src+'"]');
      if(existing){
        existing.addEventListener('load', function(){ resolve(true); });
        existing.addEventListener('error', function(){ reject(new Error('No se pudo cargar '+src)); });
        return;
      }
      var s = document.createElement('script');
      s.src = src;
      s.async = true;
      s.setAttribute('data-dantix-cdn', src);
      s.onload = function(){ resolve(true); };
      s.onerror = function(){ reject(new Error('No se pudo cargar '+src)); };
      document.head.appendChild(s);
    });
  }

  async function asegurarQRCode(){
    if(typeof qrcode !== 'undefined') return;
    // Fallback CDN (mismo API qrcode-generator)
    await loadScriptOnce('https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.min.js', function(){
      return typeof qrcode !== 'undefined';
    });
    if(typeof qrcode === 'undefined') throw new Error('El generador de QR no está disponible.');
  }

  async function asegurarJsPDF(){
    if(window.jspdf && window.jspdf.jsPDF) return;
    // Fallback CDN si el jsPDF embebido no llegó a ejecutarse
    await loadScriptOnce('https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js', function(){
      return !!(window.jspdf && window.jspdf.jsPDF);
    });
    if(!window.jspdf || !window.jspdf.jsPDF) throw new Error('El generador de PDF no está disponible (embebido ni CDN).');
  }
  // marca para detectar el parche
  window._dantixPdfCdnFallback = true;
"""

    if old_aseg not in t:
        raise SystemExit("asegurar block not found")
    t = t.replace(old_aseg, new_aseg, 1)
    print("asegurar* with CDN fallback")

    # 3) Volver a await en generarPDFReporte y generarPDFEtiquetas
    t = t.replace(
        "async function generarPDFReporte(rec){\n    asegurarJsPDF();\n    const { jsPDF } = window.jspdf;",
        "async function generarPDFReporte(rec){\n    await asegurarJsPDF();\n    const { jsPDF } = window.jspdf;",
        1,
    )
    t = t.replace(
        "async function generarPDFEtiquetas(rec){\n    asegurarJsPDF();\n    asegurarQRCode();\n    const { jsPDF } = window.jspdf;",
        "async function generarPDFEtiquetas(rec){\n    await asegurarJsPDF();\n    await asegurarQRCode();\n    const { jsPDF } = window.jspdf;",
        1,
    )
    print("await restored on PDF generators")

    # 4) Version bump
    for a, b in (
        ("LAB v226", "LAB v227"),
        ("LAB v225", "LAB v227"),
        ("Dantix Leather Vision LAB v226", "Dantix Leather Vision LAB v227"),
        ("Dantix Leather Vision LAB v225", "Dantix Leather Vision LAB v227"),
        ("<title>Dantix Leather Vision LAB v226</title>", "<title>Dantix Leather Vision LAB v227</title>"),
        ("<title>Dantix Leather Vision LAB v225</title>", "<title>Dantix Leather Vision LAB v227</title>"),
    ):
        t = t.replace(a, b)

    HTML.write_text(t, encoding="utf-8")
    print("html", HTML.stat().st_size, "v227", "LAB v227" in t, "cdn", "jspdf@2.5.1" in t)

if SW.exists():
    sw = SW.read_text(encoding="utf-8")
    sw = sw.replace("LAB v226", "LAB v227").replace("LAB v225", "LAB v227")
    for old in (
        "dantix-lv-lab-v226-pdf-fix",
        "dantix-lv-lab-v225-nest-pdfbody",
        "dantix-lv-lab-v225-nest-pdf",
    ):
        sw = sw.replace(old, "dantix-lv-lab-v227-jspdf-cdn")
    SW.write_text(sw, encoding="utf-8")
    print("sw ok")
print("ok")
