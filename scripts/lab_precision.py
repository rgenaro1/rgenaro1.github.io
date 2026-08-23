#!/usr/bin/env python3
from pathlib import Path

HTML = Path("dantix-vision-lab/index.html")
SW = Path("dantix-vision-lab/sw.js")
t = HTML.read_text(encoding="utf-8")

if "id=\"dtx-precision-section\"" in t:
    print("precision already present")
else:
    css = r"""
  /* ---- Precisión vs medidora (lab) ---- */
  .dtx-precision{font-family:inherit;color:#132420;max-width:1080px;margin:0 auto;padding:56px 24px 32px;}
  .dtx-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#0d9d94;margin-bottom:16px;}
  .dtx-eyebrow::before{content:"";width:7px;height:7px;border-radius:2px;background:#0d9d94;display:inline-block;transform:rotate(45deg);}
  .dtx-headline{font-size:clamp(26px,4vw,40px);line-height:1.15;font-weight:800;letter-spacing:-.02em;margin:0 0 18px;max-width:18ch;}
  .dtx-headline em{font-style:normal;color:#0d9d94;}
  .dtx-sub{font-size:16px;line-height:1.65;color:#4c5f59;max-width:62ch;margin:0 0 36px;}
  .dtx-sub strong{color:#132420;font-weight:650;}
  .dtx-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#dce7e2;border:1px solid #dce7e2;border-radius:14px;overflow:hidden;margin-bottom:36px;}
  .dtx-stat{background:#eef6f2;padding:24px 20px;}
  .dtx-stat-value{font-variant-numeric:tabular-nums;font-size:clamp(24px,3vw,32px);font-weight:800;color:#0a6e68;line-height:1;margin-bottom:8px;}
  .dtx-stat-value small{font-size:14px;font-weight:600;color:#4c5f59;margin-left:4px;}
  .dtx-stat-label{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#4c5f59;}
  .dtx-compare{background:#f7fbf9;border:1px solid #dce7e2;border-radius:14px;padding:28px;margin-bottom:28px;}
  .dtx-compare-title{font-size:14px;font-weight:700;margin:0 0 4px;}
  .dtx-compare-caption{font-size:13px;color:#4c5f59;margin:0 0 22px;}
  .dtx-bar-row{margin-bottom:18px;}
  .dtx-bar-row:last-child{margin-bottom:0;}
  .dtx-bar-meta{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px;font-size:13px;gap:12px;}
  .dtx-bar-name{font-weight:700;}
  .dtx-bar-name .dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px;}
  .dtx-bar-val{color:#4c5f59;font-size:12.5px;white-space:nowrap;}
  .dtx-bar-track{height:10px;background:#e3ece8;border-radius:6px;overflow:hidden;}
  .dtx-bar-fill{height:100%;width:0;border-radius:6px;transition:width 1.1s cubic-bezier(.22,.9,.25,1);}
  .dtx-bar-fill.dantix{background:linear-gradient(90deg,#0a6e68,#0d9d94);}
  .dtx-bar-fill.industrial{background:#b5651d;}
  .dtx-note{font-size:12.5px;color:#4c5f59;margin-top:18px;padding-top:14px;border-top:1px dashed #dce7e2;line-height:1.6;}
  .dtx-closing{display:flex;flex-wrap:wrap;gap:20px;align-items:center;justify-content:space-between;}
  .dtx-closing p{font-size:15px;line-height:1.55;margin:0;max-width:46ch;}
  .dtx-link{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:700;color:#0a6e68;text-decoration:none;padding:11px 16px;border:1px solid #0a6e68;border-radius:9px;}
  @media (max-width:680px){.dtx-stats{grid-template-columns:1fr;}.dtx-precision{padding:40px 16px 24px;}}
"""
    if "/* ---- Precisión vs medidora (lab) ---- */" not in t:
        if "</style>" not in t:
            raise SystemExit("no style tag")
        t = t.replace("</style>", css + "\n</style>", 1)

    section = """
<section class=\"dtx-precision\" id=\"dtx-precision-section\">
  <span class=\"dtx-eyebrow\">Validación estadística</span>
  <h2 class=\"dtx-headline\">Precisión de nivel industrial, <em>sin la inversión industrial</em>.</h2>
  <p class=\"dtx-sub\">
    Diez mediciones independientes de <strong>la misma manta y la misma foto</strong>
    (solo cambia el clic de las 4 esquinas) muestran una variación de
    <strong>0.43%</strong>. Es un margen comparable al piso de una medidora de rodillo
    de USD 15,000–40,000. La diferencia: el error de Dantix se puede bajar por software.
  </p>
  <div class=\"dtx-stats\">
    <div class=\"dtx-stat\">
      <div class=\"dtx-stat-value\">0.43<small>%</small></div>
      <div class=\"dtx-stat-label\">Coeficiente de variación</div>
    </div>
    <div class=\"dtx-stat\">
      <div class=\"dtx-stat-value\">≈4<small>mm</small></div>
      <div class=\"dtx-stat-label\">Clic de vértice (estimado)</div>
    </div>
    <div class=\"dtx-stat\">
      <div class=\"dtx-stat-value\">10/10<small>tomas</small></div>
      <div class=\"dtx-stat-label\">Misma pieza, rango esperado</div>
    </div>
  </div>
  <div class=\"dtx-compare\">
    <p class=\"dtx-compare-title\">Dispersión del error de medición (σ), manta de ~20 pie²</p>
    <p class=\"dtx-compare-caption\">Barra más corta = menos error. Dantix: n=10, misma foto. Industrial: modelo de cuantización a ¼ pie².</p>
    <div class=\"dtx-bar-row\">
      <div class=\"dtx-bar-meta\">
        <span class=\"dtx-bar-name\"><span class=\"dot\" style=\"background:#0d9d94\"></span>Dantix (visión)</span>
        <span class=\"dtx-bar-val\">σ = 0.0855 pie²</span>
      </div>
      <div class=\"dtx-bar-track\"><div class=\"dtx-bar-fill dantix\" data-width=\"61\"></div></div>
    </div>
    <div class=\"dtx-bar-row\">
      <div class=\"dtx-bar-meta\">
        <span class=\"dtx-bar-name\"><span class=\"dot\" style=\"background:#b5651d\"></span>Medidora industrial (rodillo)</span>
        <span class=\"dtx-bar-val\">σ = 0.0722 pie²</span>
      </div>
      <div class=\"dtx-bar-track\"><div class=\"dtx-bar-fill industrial\" data-width=\"52\"></div></div>
    </div>
    <p class=\"dtx-note\">
      Mismo orden de magnitud. El error de la medidora es un piso fijo de fábrica;
      el de Dantix se reduce por software, sin comprar otra máquina.
      Prueba interna RCP-2026-0007. No es certificado metrológico.
    </p>
  </div>
  <div class=\"dtx-closing\">
    <p>El error de una medidora de rodillo <strong>no cambia</strong> sin comprar otra máquina.
    El de Dantix <strong>baja con cada mejora</strong> del algoritmo.</p>
    <a class=\"dtx-link\" href=\"./paper-precision-dantix.pdf\" target=\"_blank\" rel=\"noopener\">Ver el análisis estadístico</a>
  </div>
</section>
"""
    mark = '<section class="dlv-steps" id="dlv-tecnologia">'
    idx = t.find(mark)
    if idx < 0:
        raise SystemExit("anchor not found")
    t = t[:idx] + section + "\n" + t[idx:]

    js = """
<script>
(function(){
  var bars = document.querySelectorAll('#dtx-precision-section .dtx-bar-fill');
  var target = document.getElementById('dtx-precision-section');
  if(!target || !bars.length) return;
  if(!('IntersectionObserver' in window)){
    bars.forEach(function(bar){ bar.style.width = bar.getAttribute('data-width') + '%'; });
    return;
  }
  var observer = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){
        bars.forEach(function(bar){ bar.style.width = bar.getAttribute('data-width') + '%'; });
        observer.disconnect();
      }
    });
  }, {threshold:0.35});
  observer.observe(target);
})();
</script>
"""
    if "dtx-bar-fill" in t and "IntersectionObserver" not in t[t.find("dtx-precision-section"):t.find("dtx-precision-section")+8000]:
        if "</body>" in t:
            t = t.replace("</body>", js + "\n</body>", 1)

t = t.replace("Dantix Leather Vision LAB v222", "Dantix Leather Vision LAB v223")
t = t.replace("LAB v222", "LAB v223")
HTML.write_text(t, encoding="utf-8")
print("html", HTML.stat().st_size, "has section", 'id="dtx-precision-section"' in t)

if SW.exists():
    sw = SW.read_text(encoding="utf-8")
    sw = sw.replace("LAB v222", "LAB v223").replace("dantix-lv-lab-v222-studio", "dantix-lv-lab-v223-precision")
    SW.write_text(sw, encoding="utf-8")
    print("sw ok")
print("ok lab precision")
