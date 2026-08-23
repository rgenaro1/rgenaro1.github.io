#!/usr/bin/env python3
from pathlib import Path

p = Path("dantix-vision/index.html")
t = p.read_text(encoding="utf-8")

old_css = ".mode-options{display:flex; gap:20px; flex-wrap:wrap; justify-content:center;}"
new_css = """.mode-options{display:flex; gap:20px; flex-wrap:wrap; justify-content:center;}
  .home-group{width:100%; margin-top:8px;}
  .home-group-label{
    font-size:11.5px; letter-spacing:0.14em; text-transform:uppercase; font-weight:700;
    color:var(--brand); margin:18px 0 12px;
  }
  .home-group-moldes .home-group-label{color:#c2782a;}
  .home-mantas .mode-btn{border-left:4px solid var(--brand);}
  .mode-btn.home-molde{border-left:4px solid #c2782a; max-width:100%; flex:1 1 100%;}
  .mode-btn.home-molde .mode-btn-icon{background:#f8ead8; color:#c2782a;}
  .mode-btn.home-molde .mode-btn-sub{color:#c2782a;}
  .mode-btn.home-molde .mode-btn-cta{color:#c2782a;}
  .mode-btn-sub{font-size:12.5px; font-weight:600; color:var(--brand); margin:-2px 0 8px;}
  .mode-btn-chips{display:flex; flex-wrap:wrap; gap:8px; margin:0 0 14px;}
  .mode-chip{
    font-size:11px; border:1px solid var(--line); border-radius:999px;
    padding:4px 10px; color:var(--text-dim); background:var(--surface);
  }
  .mode-btn.home-molde .mode-chip{border-color:#e8d0b0; color:#8a5a20;}
  @media (min-width:960px){
    .home-mantas{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px;}
    .home-mantas .mode-btn{max-width:none; flex:none; width:100%;}
    .home-moldes{display:block;}
    .mode-btn.home-molde{display:grid; grid-template-columns:auto 1fr auto; grid-template-rows:auto auto auto; column-gap:20px; align-items:center;}
    .mode-btn.home-molde .mode-btn-icon{grid-row:1 / span 3; margin-bottom:0;}
    .mode-btn.home-molde .mode-btn-cta{grid-column:3; grid-row:2; justify-self:end;}
    .mode-btn.home-molde .mode-btn-chips{grid-column:2;}
  }"""

if old_css in t:
    t = t.replace(old_css, new_css, 1)
    print("ok css")
else:
    print("MISSING css")

old_sec_start = '<section class="dlv-solutions" id="dlv-soluciones">'
old_sec_end = '<section class="dlv-steps"'
i = t.find(old_sec_start)
j = t.find(old_sec_end)
if i < 0 or j < 0:
    raise SystemExit("no se encontro seccion soluciones")

new_sec = r'''<section class="dlv-solutions" id="dlv-soluciones">
      <div class="dlv-section-head">
        <h2>Elige qué vas a hacer</h2>
        <p>Manta o molde. Cada opción hace una cosa distinta.</p>
      </div>
      <div class="home-group">
        <div class="home-group-label">Mantas</div>
        <div class="mode-options home-mantas">
          <button type="button" class="mode-btn" id="btnModoMovil">
            <div class="mode-btn-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg></div>
            <div class="mode-btn-title">Recepción rápida</div>
            <div class="mode-btn-sub">VisionMeasure</div>
            <div class="mode-btn-desc">Mide el área desde el celular o la PC y deja el registro.</div>
            <div class="mode-btn-chips"><span class="mode-chip">Celular o PC</span><span class="mode-chip">Área</span></div>
            <div class="mode-btn-cta">Empezar →</div>
          </button>
          <button type="button" class="mode-btn" id="btnModoEscritorio">
            <div class="mode-btn-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 6h11a1 1 0 0 1 1 1v13H6V7a1 1 0 0 1 1-1h1z"/><path d="M8 6V4h6v2"/><path d="m9 12 2 2 4-4"/></svg></div>
            <div class="mode-btn-title">Recepción e inspección</div>
            <div class="mode-btn-sub">VisionStudio</div>
            <div class="mode-btn-desc">En PC. Mide la manta, clasifica defectos y calcula el rendimiento.</div>
            <div class="mode-btn-chips"><span class="mode-chip">Solo PC</span><span class="mode-chip">Medición</span><span class="mode-chip">Calidad</span></div>
            <div class="mode-btn-cta">Empezar →</div>
          </button>
          <button type="button" class="mode-btn" id="btnModoInteligente">
            <div class="mode-btn-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><rect x="7" y="7" width="10" height="10" rx="1"/></svg></div>
            <div class="mode-btn-title">Medición con Dantix Card</div>
            <div class="mode-btn-sub">Intelligent Measure</div>
            <div class="mode-btn-desc">Mide el área en cualquier sitio, con las 4 tarjetas, sin cinta.</div>
            <div class="mode-btn-chips"><span class="mode-chip">Dantix Card</span><span class="mode-chip">Sin cinta</span><span class="mode-chip">Beta</span></div>
            <div class="mode-btn-cta">Empezar →</div>
          </button>
        </div>
      </div>
      <div class="home-group home-group-moldes">
        <div class="home-group-label">Moldes</div>
        <div class="mode-options home-moldes">
          <button type="button" class="mode-btn home-molde" id="btnModoMoldes">
            <div class="mode-btn-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 4c-2 2-3 5-2 8 2 5 6 8 10 7 2 0 4-3 3-6-1-4-5-7-8-9"/><path d="M9 9c1 2 3 4 6 5"/></svg></div>
            <div class="mode-btn-title">Digitalizar moldes</div>
            <div class="mode-btn-sub">Pattern</div>
            <div class="mode-btn-desc">Sin escáner. Contorno listo para corte o para tu software de diseño.</div>
            <div class="mode-btn-chips"><span class="mode-chip">DXF</span><span class="mode-chip">Sin escáner</span></div>
            <div class="mode-btn-cta">Empezar →</div>
          </button>
        </div>
      </div>
    </section>

    
'''

t = t[:i] + new_sec + t[j:]
print("ok section", i, j)

t = t.replace("<title>Dantix Leather Vision v210</title>", "<title>Dantix Leather Vision v211</title>", 1)
p.write_text(t, encoding="utf-8")
print("wrote html", p.stat().st_size)

sw = Path("dantix-vision/sw.js")
s = sw.read_text(encoding="utf-8")
s = s.replace("service worker v210", "service worker v211")
s = s.replace("dantix-lv-v210-cards-1", "dantix-lv-v211-home-1")
sw.write_text(s, encoding="utf-8")
print("wrote sw")
