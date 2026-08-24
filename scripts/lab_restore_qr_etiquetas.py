#!/usr/bin/env python3
"""LAB: devolver generarPDFEtiquetas al formato de produccion (plancha 3x6).
Sin foto de acomodo y sin aviso 'Sin imagen de acomodo'.
"""
from pathlib import Path

HTML = Path("dantix-vision-lab/index.html")
SW = Path("dantix-vision-lab/sw.js")
t = HTML.read_text(encoding="utf-8")

PROD_PDF = r'''async function generarPDFEtiquetas(rec){
    asegurarJsPDF();
    asegurarQRCode();
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({unit:'pt', format:'a4'});
    const pageW = doc.internal.pageSize.getWidth();
    const pageH = doc.internal.pageSize.getHeight();
    const marginX = 24, marginY = 24, gap = 10;
    const cols = 3, rows = 6;
    const cardW = (pageW - 2*marginX - (cols-1)*gap)/cols;
    const cardH = (pageH - 2*marginY - (rows-1)*gap)/rows;
    const porPagina = cols*rows;

    for(let idx=0; idx<rec.mantas.length; idx++){
      const m = rec.mantas[idx];
      if(idx>0 && idx % porPagina === 0) doc.addPage();
      const pos = idx % porPagina;
      const col = pos % cols, row = Math.floor(pos/cols);
      const x = marginX + col*(cardW+gap);
      const y = marginY + row*(cardH+gap);

      doc.setDrawColor(220,222,225);
      doc.roundedRect(x, y, cardW, cardH, 6, 6, 'S');

      let qrUrl = m.qrDataUrl || null;
      if(!qrUrl){
        try{ qrUrl = generarQRDataURL(m.codigo); }
        catch(e){ console.warn('No se pudo generar el QR de', m.codigo, e); }
      }
      const qrSize = Math.min(cardH-16, 62);
      if(qrUrl){
        try{ doc.addImage(qrUrl, 'GIF', x+8, y+cardH/2-qrSize/2, qrSize, qrSize); }
        catch(e){
          try{ doc.addImage(qrUrl, 'PNG', x+8, y+cardH/2-qrSize/2, qrSize, qrSize); }
          catch(e2){}
        }
      }

      const tx = x + qrSize + 18;
      const d = rec.datos || {};
      doc.setTextColor(20,24,28); doc.setFont('helvetica','bold'); doc.setFontSize(9.5);
      doc.text(String(m.codigo || '\u2014'), tx, y+18);
      doc.setFont('helvetica','normal'); doc.setFontSize(7.6); doc.setTextColor(90,95,100);
      doc.text(String(d.nombreCuero||'\u2014'), tx, y+31);
      doc.text('Espesor: ' + (d.espesorMm ? d.espesorMm+' mm' : '\u2014'), tx, y+42);
      doc.text(String(d.proveedor||'\u2014'), tx, y+53);
      doc.setFont('helvetica','bold'); doc.setTextColor(13,157,148); doc.setFontSize(9);
      doc.text((m.areaPie2||0).toFixed(2)+' pie\u00b2', tx, y+cardH-10);
    }
    doc.save((rec.codigo || 'recepcion') + '_etiquetas_qr.pdf');
  }

'''

start = t.find("async function generarPDFEtiquetas(rec){")
if start < 0:
    raise SystemExit("generarPDFEtiquetas not found")
end = t.find("// ---------- Generar un documento individual", start)
if end < 0:
    end = t.find("async function generarUnDocumento", start)
if end < 0:
    raise SystemExit("end of generarPDFEtiquetas not found")

if "Sin imagen de acomodo" not in t[start:end] and "cols = 3, rows = 6" in t[start:end]:
    print("already production layout")
else:
    t = t[:start] + PROD_PDF + t[end:]
    print("restored production etiquetas grid")

replacements = [
    ("QR-Manta</button>", "Descargar etiquetas QR</button>"),
    ("PDF manta + QR (1 hoja c/u)</button>", "Descargar etiquetas QR</button>"),
    ("etiquetas: 'PDF QR-Manta generado.'", "etiquetas: 'Etiquetas QR generadas.'"),
    ("etiquetas:'PDF de mantas con QR generado.'", "etiquetas:'Etiquetas QR generadas.'"),
    ("etiquetas:'PDF QR-Manta generado.'", "etiquetas:'Etiquetas QR generadas.'"),
]
for old, new in replacements:
    if old in t:
        t = t.replace(old, new)
        print("renamed", old[:40])

for oldv in ("LAB v227", "LAB v226", "LAB v225"):
    t = t.replace(oldv, "LAB v228")
t = t.replace(
    "<title>Dantix Leather Vision LAB v227</title>",
    "<title>Dantix Leather Vision LAB v228</title>",
)
t = t.replace(
    "<title>Dantix Leather Vision LAB v226</title>",
    "<title>Dantix Leather Vision LAB v228</title>",
)

HTML.write_text(t, encoding="utf-8")
print("html", HTML.stat().st_size, "aviso", "Sin imagen de acomodo" in HTML.read_text(encoding="utf-8"))

if SW.exists():
    sw = SW.read_text(encoding="utf-8")
    for oldv in ("LAB v227", "LAB v226", "LAB v225"):
        sw = sw.replace(oldv, "LAB v228")
    for old in (
        "dantix-lv-lab-v227",
        "dantix-lv-lab-v226-pdf-fix",
        "dantix-lv-lab-v225-nest-pdf",
    ):
        sw = sw.replace(old, "dantix-lv-lab-v228-qr-prod")
    SW.write_text(sw, encoding="utf-8")
    print("sw ok")
print("ok")
