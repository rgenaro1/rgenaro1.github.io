#!/usr/bin/env python3
"""LAB v226: arreglar botones PDF reporte + QR-Manta (gesto de descarga, nombre, errores)."""
from pathlib import Path

HTML = Path("dantix-vision-lab/index.html")
SW = Path("dantix-vision-lab/sw.js")
t = HTML.read_text(encoding="utf-8")

if "LAB v226" in t and "QR-Manta" in t and "btnDescargarQrManta" in t:
    print("already patched v226")
else:
    # 1) Renombrar botón en el HTML dinámico del resumen de finalización
    old_btn = (
        '<button type="button" class="ghost" id="btnDescargarEtiquetasRecepcion">'
        "🏷️ PDF manta + QR (1 hoja c/u)</button>"
    )
    new_btn = (
        '<button type="button" class="ghost" id="btnDescargarQrManta">'
        "QR-Manta</button>"
    )
    if old_btn not in t:
        # variantes posibles
        alts = [
            old_btn,
            '<button type="button" class="ghost" id="btnDescargarEtiquetasRecepcion">🏷️ Descargar etiquetas QR</button>',
            '<button type="button" class="ghost" id="btnDescargarEtiquetasRecepcion">🏷️ PDF manta + QR (1 hoja c/u)</button>',
        ]
        found = False
        for a in alts:
            if a in t:
                t = t.replace(a, new_btn, 1)
                found = True
                print("renamed button via alt")
                break
        if not found:
            raise SystemExit("button HTML for etiquetas not found")
    else:
        t = t.replace(old_btn, new_btn, 1)
        print("renamed button")

    # 2) Reemplazar el binding frágil (getElementById justo después de innerHTML)
    #    por delegación de eventos en #rcResumen + descarga que preserva el gesto del usuario.
    old_bind = """    document.getElementById('btnGenerarReporte').addEventListener('click', () => generarUnDocumento(generarPDFReporte, 'reporte'));
    document.getElementById('btnDescargarCsvRecepcion').addEventListener('click', () => generarUnDocumento(async (rec) => {
      descargarBlob(new Blob([generarCSVRecepcion(rec)], {type:'text/csv'}), `${rec.codigo}.csv`);
    }, 'csv'));
    document.getElementById('btnDescargarEtiquetasRecepcion').addEventListener('click', () => generarUnDocumento(generarPDFEtiquetas, 'etiquetas'));
    document.getElementById('btnEmpezarNuevaRecepcion').addEventListener('click', () => {
      if(typeof iniciarNuevaRecepcionCompleta === 'function') iniciarNuevaRecepcionCompleta();
    });"""

    new_bind = """    // Delegación: un solo listener estable en #rcResumen (no se pierde al regenerar HTML)
    if(!resumen._dantixDocBound){
      resumen._dantixDocBound = true;
      resumen.addEventListener('click', (ev) => {
        const btn = ev.target && ev.target.closest ? ev.target.closest('button') : null;
        if(!btn) return;
        const id = btn.id || '';
        if(id === 'btnGenerarReporte'){
          ev.preventDefault();
          generarUnDocumento(generarPDFReporte, 'reporte');
        } else if(id === 'btnDescargarCsvRecepcion'){
          ev.preventDefault();
          generarUnDocumento(function(rec){
            descargarBlob(new Blob([generarCSVRecepcion(rec)], {type:'text/csv;charset=utf-8'}), (rec.codigo || 'recepcion') + '.csv');
          }, 'csv');
        } else if(id === 'btnDescargarQrManta' || id === 'btnDescargarEtiquetasRecepcion'){
          ev.preventDefault();
          generarUnDocumento(generarPDFEtiquetas, 'etiquetas');
        } else if(id === 'btnEmpezarNuevaRecepcion'){
          ev.preventDefault();
          if(typeof iniciarNuevaRecepcionCompleta === 'function') iniciarNuevaRecepcionCompleta();
        }
      });
    }"""

    if old_bind not in t:
        raise SystemExit("old button bind block not found")
    t = t.replace(old_bind, new_bind, 1)
    print("rewired resumen buttons with delegation")

    # 3) asegurarJsPDF / asegurarQRCode síncronos (evita perder el gesto de usuario por microtask)
    old_aseg = """  async function asegurarQRCode(){
    if(typeof qrcode === 'undefined') throw new Error('El generador de QR no está disponible en este archivo.');
  }
  async function asegurarJsPDF(){
    if(!window.jspdf) throw new Error('El generador de PDF no está disponible en este archivo.');
  }"""
    new_aseg = """  function asegurarQRCode(){
    if(typeof qrcode === 'undefined') throw new Error('El generador de QR no está disponible en este archivo.');
  }
  function asegurarJsPDF(){
    if(!window.jspdf || !window.jspdf.jsPDF) throw new Error('El generador de PDF no está disponible en este archivo.');
  }"""
    if old_aseg not in t:
        raise SystemExit("asegurar* block not found")
    t = t.replace(old_aseg, new_aseg, 1)
    print("asegurar* now sync")

    # 4) generarPDFReporte: quitar await innecesario de asegurarJsPDF
    t = t.replace(
        "async function generarPDFReporte(rec){\n    await asegurarJsPDF();\n    const { jsPDF } = window.jspdf;",
        "async function generarPDFReporte(rec){\n    asegurarJsPDF();\n    const { jsPDF } = window.jspdf;",
        1,
    )
    print("reporte: sync asegurar")

    # 5) generarPDFEtiquetas: sync asegurar + QR sin await inútil
    old_etiq_head = """async function generarPDFEtiquetas(rec){
    await asegurarJsPDF();
    await asegurarQRCode();
    const { jsPDF } = window.jspdf;"""
    new_etiq_head = """async function generarPDFEtiquetas(rec){
    asegurarJsPDF();
    asegurarQRCode();
    const { jsPDF } = window.jspdf;"""
    if old_etiq_head not in t:
        raise SystemExit("etiquetas head not found")
    t = t.replace(old_etiq_head, new_etiq_head, 1)

    # qrUrl = await generarQRDataURL → síncrono
    t = t.replace(
        "try{ qrUrl = await generarQRDataURL(m.codigo); }catch(e){}",
        "try{ qrUrl = generarQRDataURL(m.codigo); }catch(e){}",
        1,
    )
    print("etiquetas: sync asegurar + QR")

    # 6) generarUnDocumento más robusto + mensaje de error visible
    old_gud = """  async function generarUnDocumento(fn, tipo){
    const rec = window._recepcion;
    if(!rec || !rec.mantas.length) return;
    const aviso = document.getElementById('avisoGenerando');
    if(aviso) aviso.style.display = 'block';
    try{
      await fn(rec);
      const nombres = {reporte:'Reporte PDF generado.', csv:'CSV descargado.', etiquetas:'PDF de mantas con QR generado.'};
      setStatus(nombres[tipo] || 'Documento generado.', 'ok');
    } catch(e){
      console.error(e);
      setStatus(e && e.message ? e.message : 'Ocurrió un problema generando el documento. Vuelve a intentarlo.', 'err');
    } finally {
      if(aviso) aviso.style.display = 'none';
    }
  }"""

    new_gud = """  async function generarUnDocumento(fn, tipo){
    const rec = window._recepcion;
    if(!rec || !rec.mantas || !rec.mantas.length){
      setStatus('No hay mantas en la recepción para generar el documento.', 'err');
      return;
    }
    const aviso = document.getElementById('avisoGenerando');
    if(aviso) aviso.style.display = 'block';
    try{
      // Ejecutar de forma síncrona lo posible para no perder el gesto de descarga en móviles
      const ret = fn(rec);
      if(ret && typeof ret.then === 'function') await ret;
      const nombres = {
        reporte: 'Reporte PDF generado.',
        csv: 'CSV descargado.',
        etiquetas: 'PDF QR-Manta generado.'
      };
      setStatus(nombres[tipo] || 'Documento generado.', 'ok');
    } catch(e){
      console.error('generarUnDocumento', tipo, e);
      const msg = (e && e.message) ? e.message : 'Ocurrió un problema generando el documento.';
      setStatus(msg, 'err');
      try { alert('No se pudo generar el documento:\\n' + msg); } catch(_){}
    } finally {
      if(aviso) aviso.style.display = 'none';
    }
  }"""
    if old_gud not in t:
        raise SystemExit("generarUnDocumento block not found")
    t = t.replace(old_gud, new_gud, 1)
    print("generarUnDocumento hardened")

    # 7) Version bump
    t = t.replace("LAB v225", "LAB v226")
    t = t.replace("Dantix Leather Vision LAB v225", "Dantix Leather Vision LAB v226")
    # title
    t = t.replace(
        "<title>Dantix Leather Vision LAB v225</title>",
        "<title>Dantix Leather Vision LAB v226</title>",
    )
    HTML.write_text(t, encoding="utf-8")
    print("html", HTML.stat().st_size, "QR-Manta", "QR-Manta" in t, "v226", "LAB v226" in t)

if SW.exists():
    sw = SW.read_text(encoding="utf-8")
    sw = sw.replace("LAB v225", "LAB v226")
    for old in (
        "dantix-lv-lab-v225-nest-pdfbody",
        "dantix-lv-lab-v225-nest-pdf",
        "dantix-lv-lab-v224-fixbody",
    ):
        sw = sw.replace(old, "dantix-lv-lab-v226-pdf-fix")
    SW.write_text(sw, encoding="utf-8")
    print("sw ok", "v226" in SW.read_text(encoding="utf-8"))
print("ok")
