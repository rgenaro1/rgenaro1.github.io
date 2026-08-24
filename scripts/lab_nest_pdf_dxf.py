#!/usr/bin/env python3
"""Lab: PDF QR una manta/hoja con acomodo + boton DXF del nesting."""
from pathlib import Path

HTML = Path("dantix-vision-lab/index.html")
SW = Path("dantix-vision-lab/sw.js")
t = HTML.read_text(encoding="utf-8")

if 'id="btnDescargarDxfNesting"' in t and "PDF manta + QR" in t:
    print("already patched")
else:
    old_btn = (
        '<button class="ghost" id="btnEditarNesting" disabled>'
        "Editar acomodo (arrastrar / rotar)</button>"
    )
    # match with emoji flexible
    import re
    m = re.search(r'<button class="ghost" id="btnEditarNesting" disabled>[^<]*</button>', t)
    if not m:
        raise SystemExit("btnEditarNesting anchor not found")
    old_btn = m.group(0)
    new_btn = old_btn + '\n      <button class="ghost" id="btnDescargarDxfNesting" disabled>DXF acomodo (manta + piezas)</button>'
    t = t.replace(old_btn, new_btn, 1)

    old_done = "setStatus(`Nesting completo: ${paresColocados} pares reales colocados.`, 'ok');"
    new_done = """setStatus(`Nesting completo: ${paresColocados} pares reales colocados.`, 'ok');
  try {
    window._ultimoNestImage = canvasNesting.toDataURL('image/jpeg', 0.88);
    window._ultimoNestPares = paresColocados;
    const bDxf = document.getElementById('btnDescargarDxfNesting');
    if(bDxf) bDxf.disabled = false;
  } catch(e){ console.warn('No se pudo guardar vista del nesting', e); }"""
    if old_done not in t:
        raise SystemExit("nest complete anchor not found")
    t = t.replace(old_done, new_done, 1)

    old_reg = "paresReales: window._paresRealesUltimo !== undefined ? window._paresRealesUltimo : '\u2014',"
    # try both dash types
    if old_reg not in t:
        old_reg = "paresReales: window._paresRealesUltimo !== undefined ? window._paresRealesUltimo : '\u2014',"
    if "paresReales: window._paresRealesUltimo" not in t:
        raise SystemExit("register manta anchor not found")
    # more robust replace
    import re as _re
    t2, n = _re.subn(
        r"paresReales:\s*window\._paresRealesUltimo\s*!==\s*undefined\s*\?\s*window\._paresRealesUltimo\s*:\s*'[^']*',",
        "paresReales: window._paresRealesUltimo !== undefined ? window._paresRealesUltimo : '\u2014',\n      nestImage: window._ultimoNestImage || null,\n      nestPares: window._ultimoNestPares != null ? window._ultimoNestPares : (window._paresRealesUltimo !== undefined ? window._paresRealesUltimo : null),",
        t, count=1)
    if n != 1:
        raise SystemExit("register replace failed n="+str(n))
    t = t2

    dxf_fn = r'''
function contornoMantaCmParaDxf(){
  if(!window._maskLimpia) return null;
  const mask = window._maskLimpia;
  const PX_POR_CM = 8;
  const alturaCm = mask.rows / PX_POR_CM;
  const contours = new cv.MatVector();
  const hierarchy = new cv.Mat();
  cv.findContours(mask, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);
  let maxArea = 0, maxIdx = -1;
  for(let i=0; i<contours.size(); i++){
    const a = cv.contourArea(contours.get(i));
    if(a > maxArea){ maxArea = a; maxIdx = i; }
  }
  if(maxIdx < 0){ hierarchy.delete(); contours.delete(); return null; }
  const c = contours.get(maxIdx);
  const approx = new cv.Mat();
  cv.approxPolyDP(c, approx, 1.5, true);
  const puntosCm = [];
  for(let k=0; k<approx.rows; k++){
    const px = approx.data32S[k*2], py = approx.data32S[k*2+1];
    puntosCm.push({x: px/PX_POR_CM, y: alturaCm - py/PX_POR_CM});
  }
  approx.delete(); hierarchy.delete(); contours.delete();
  return puntosCm.length >= 3 ? puntosCm : null;
}

function descargarDxfAcomodoNesting(){
  if(!window._nestState || !window._nestState.colocaciones || !window._nestState.colocaciones.length){
    setStatus('Primero simula el acomodo real.', 'err'); return;
  }
  if(!window._maskLimpia){ setStatus('No hay contorno de manta.', 'err'); return; }
  const PX_POR_CM = 8;
  const alturaCm = window._maskLimpia.rows / PX_POR_CM;
  const manta = contornoMantaCmParaDxf();
  if(!manta){ setStatus('No se pudo exportar el contorno de la manta.', 'err'); return; }
  let dxf = '';
  const linea = (codigo, valor) => { dxf += codigo + '\n' + valor + '\n'; };
  linea(0,'SECTION'); linea(2,'HEADER');
  linea(9,'$ACADVER'); linea(1,'AC1009');
  linea(0,'ENDSEC');
  linea(0,'SECTION'); linea(2,'ENTITIES');
  const emitPoly = (pts, capa) => {
    linea(0,'POLYLINE'); linea(8, capa); linea(66,'1'); linea(70,'1');
    pts.forEach(p => {
      linea(0,'VERTEX'); linea(8, capa);
      linea(10, Number(p.x).toFixed(3));
      linea(20, Number(p.y).toFixed(3));
    });
    linea(0,'SEQEND');
  };
  emitPoly(manta, 'MANTA');
  window._nestState.colocaciones.forEach((pl, i) => {
    const pts = (pl.contornoManta || []).map(p => ({x: p.x, y: alturaCm - p.y}));
    if(pts.length >= 3) emitPoly(pts, 'PIEZA_' + (i+1));
  });
  linea(0,'ENDSEC'); linea(0,'EOF');
  const codigoRec = (window._recepcion && window._recepcion.codigo)
    ? window._recepcion.codigo.replace(/[^a-zA-Z0-9-]/g,'') : 'nest';
  const nombre = codigoRec + '-acomodo-' + Date.now() + '.dxf';
  const blob = new Blob([dxf], {type:'application/dxf'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = nombre;
  a.click();
  setStatus('DXF del acomodo descargado (manta + ' + window._nestState.colocaciones.length + ' piezas, cm).', 'ok');
}

(function(){
  const b = document.getElementById('btnDescargarDxfNesting');
  if(b) b.addEventListener('click', descargarDxfAcomodoNesting);
})();

'''
    mark = "function polygonAreaLocal(points){"
    if mark not in t:
        raise SystemExit("polygonAreaLocal not found")
    t = t.replace(mark, dxf_fn + mark, 1)

    start = t.find("async function generarPDFEtiquetas(rec){")
    if start < 0:
        raise SystemExit("generarPDFEtiquetas not found")
    end = t.find("// ---------- Generar un documento individual", start)
    if end < 0:
        end = t.find("async function generarUnDocumento", start)
    if end < 0:
        raise SystemExit("end of generarPDFEtiquetas not found")

    new_pdf = r'''async function generarPDFEtiquetas(rec){
    await asegurarJsPDF();
    await asegurarQRCode();
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({unit:'pt', format:'a4'});
    const pageW = doc.internal.pageSize.getWidth();
    const pageH = doc.internal.pageSize.getHeight();
    const margin = 36;

    for(let idx=0; idx<rec.mantas.length; idx++){
      const m = rec.mantas[idx];
      if(idx > 0) doc.addPage();

      doc.setTextColor(20,24,28);
      doc.setFont('helvetica','bold'); doc.setFontSize(13);
      doc.text('Dantix Leather Vision \u2014 Hoja de manta', margin, margin + 4);
      doc.setFont('helvetica','normal'); doc.setFontSize(9); doc.setTextColor(100,105,110);
      doc.text('Recepcion ' + (rec.codigo || '\u2014'), margin, margin + 18);
      doc.setDrawColor(220,222,225);
      doc.line(margin, margin + 26, pageW - margin, margin + 26);

      let qrUrl = m.qrDataUrl || null;
      if(!qrUrl){
        try{ qrUrl = await generarQRDataURL(m.codigo); }catch(e){}
      }
      const qrSize = 78;
      const qrX = pageW - margin - qrSize;
      const qrY = margin + 36;
      if(qrUrl){
        try{ doc.addImage(qrUrl, 'GIF', qrX, qrY, qrSize, qrSize); }catch(e){
          try{ doc.addImage(qrUrl, 'PNG', qrX, qrY, qrSize, qrSize); }catch(e2){}
        }
      }
      doc.setFont('helvetica','bold'); doc.setFontSize(8); doc.setTextColor(13,157,148);
      doc.text(String(m.codigo||''), qrX + qrSize/2, qrY + qrSize + 12, {align:'center'});

      const pares = (m.nestPares != null && m.nestPares !== '') ? m.nestPares
        : (m.paresReales != null && m.paresReales !== '' && m.paresReales !== '\u2014' ? m.paresReales : '\u2014');
      const filas = [
        ['Codigo', m.codigo || '\u2014'],
        ['Area', (m.areaPie2 != null ? Number(m.areaPie2).toFixed(2) + ' pie2' : '\u2014')],
        ['Pares colocados', String(pares)],
        ['Clase', m.clase || '\u2014'],
        ['Proveedor', (rec.datos && rec.datos.proveedor) || '\u2014'],
        ['Cuero', (rec.datos && rec.datos.nombreCuero) || '\u2014'],
        ['Espesor', (rec.datos && rec.datos.espesorMm) ? rec.datos.espesorMm + ' mm' : '\u2014'],
        ['Fecha', m.fechaMedicion || (rec.datos && rec.datos.fecha) || '\u2014'],
        ['Operario', (rec.datos && rec.datos.operario) || '\u2014']
      ];
      let ty = margin + 48;
      filas.forEach(function(row){
        doc.setFont('helvetica','normal'); doc.setFontSize(8.5); doc.setTextColor(130,135,140);
        doc.text(row[0], margin, ty);
        doc.setFont('helvetica','bold'); doc.setTextColor(20,24,28);
        doc.text(String(row[1]), margin + 88, ty);
        ty += 13;
      });

      const imgTop = Math.max(ty, qrY + qrSize + 28) + 8;
      const imgMaxW = pageW - 2*margin;
      const imgMaxH = pageH - imgTop - margin - 20;
      const imgSrc = m.nestImage || null;
      if(imgSrc){
        try{
          doc.setDrawColor(230,232,234);
          doc.roundedRect(margin, imgTop, imgMaxW, imgMaxH, 4, 4, 'S');
          const pad = 6;
          doc.addImage(imgSrc, 'JPEG', margin+pad, imgTop+pad, imgMaxW-2*pad, imgMaxH-2*pad);
        }catch(e){
          doc.setFont('helvetica','normal'); doc.setFontSize(9); doc.setTextColor(150,80,80);
          doc.text('No se pudo insertar la imagen del acomodo.', margin, imgTop + 20);
        }
      } else {
        doc.setFillColor(247,251,249);
        doc.roundedRect(margin, imgTop, imgMaxW, Math.min(120, imgMaxH), 4, 4, 'F');
        doc.setFont('helvetica','normal'); doc.setFontSize(9); doc.setTextColor(100,110,115);
        doc.text('Sin imagen de acomodo. Ejecuta Simular acomodo real y guarda la manta antes de generar el PDF.', margin + 12, imgTop + 28);
      }

      doc.setFont('helvetica','normal'); doc.setFontSize(7.5); doc.setTextColor(150,155,160);
      doc.text('Manta ' + (idx+1) + ' de ' + rec.mantas.length + ' · Una manta por hoja', margin, pageH - 16);
    }
    doc.save((rec.codigo || 'recepcion') + '_mantas_qr.pdf');
  }

'''
    t = t[:start] + new_pdf + t[end:]

    t = t.replace('Descargar etiquetas QR</button>', 'PDF manta + QR (1 hoja c/u)</button>', 1)
    t = t.replace("etiquetas:'Etiquetas QR generadas.'", "etiquetas:'PDF de mantas con QR generado.'", 1)

    old_redraw = "function redibujarConSeleccion(){\n  const st = window._nestState;\n  dibujarNesting(st.colocaciones, st.nestCellCm);"
    new_redraw = """function redibujarConSeleccion(){
  const st = window._nestState;
  dibujarNesting(st.colocaciones, st.nestCellCm);
  try { window._ultimoNestImage = canvasNesting.toDataURL('image/jpeg', 0.88); } catch(e){}"""
    if old_redraw in t:
        t = t.replace(old_redraw, new_redraw, 1)
    else:
        print("warn: redibujarConSeleccion anchor not exact")

t = t.replace("LAB v224", "LAB v225").replace("LAB v223", "LAB v225")
HTML.write_text(t, encoding="utf-8")
print("html", HTML.stat().st_size, "btn", 'btnDescargarDxfNesting' in t)

if SW.exists():
    sw = SW.read_text(encoding="utf-8")
    sw = sw.replace("LAB v224", "LAB v225").replace("LAB v223", "LAB v225")
    for old in ("dantix-lv-lab-v224-fix", "dantix-lv-lab-v223-precision", "dantix-lv-lab-v222-studio"):
        sw = sw.replace(old, "dantix-lv-lab-v225-nest-pdf")
    SW.write_text(sw, encoding="utf-8")
    print("sw ok")
print("ok")
