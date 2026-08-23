#!/usr/bin/env python3
from pathlib import Path

p = Path("dantix-vision/index.html")
t = p.read_text(encoding="utf-8")
changed = 0

old_css_start = ".home-group{width:100%; margin-top:8px;}"
old_css_end = "    .mode-btn.home-molde .mode-btn-chips{grid-column:2;}\n  }"
i = t.find(old_css_start)
j = t.find(old_css_end)
if i < 0 or j < 0:
    raise SystemExit("no se encontro bloque css home-group")
j = j + len(old_css_end)

new_css = """\
.home-group{width:100%; margin-top:8px;}
  .home-group-label{
    font-size:11.5px; letter-spacing:0.14em; text-transform:uppercase; font-weight:700;
    color:var(--brand); margin:18px 0 12px;
  }
  .home-group-moldes .home-group-label{color:#c2782a;}
  .home-mantas,.home-moldes{width:100%;}
  .home-mantas .mode-btn,.mode-btn.home-molde{
    display:grid;
    grid-template-columns:58px 1fr auto;
    grid-template-areas:
      \"icon title title\"
      \"icon sub sub\"
      \"icon desc desc\"
      \"chips chips cta\";
    column-gap:14px; row-gap:2px;
    max-width:none; width:100%; flex:none;
    text-align:left; padding:22px 20px;
    border-left:4px solid var(--brand);
  }
  .mode-btn.home-molde{border-left-color:#c2782a; flex:1 1 100%;}
  .home-mantas .mode-btn .mode-btn-icon,
  .mode-btn.home-molde .mode-btn-icon{
    grid-area:icon; width:52px; height:52px; margin:0;
    background:transparent; align-self:start;
  }
  .home-mantas .mode-btn .mode-btn-icon svg,
  .mode-btn.home-molde .mode-btn-icon svg{width:40px; height:40px;}
  .mode-btn.home-molde .mode-btn-icon{color:#c2782a; background:transparent;}
  .home-mantas .mode-btn .mode-btn-title,
  .mode-btn.home-molde .mode-btn-title{grid-area:title; margin:0 0 2px;}
  .mode-btn-sub{grid-area:sub; font-size:12.5px; font-weight:600; color:var(--brand); margin:0;}
  .mode-btn.home-molde .mode-btn-sub{color:#c2782a;}
  .home-mantas .mode-btn .mode-btn-desc,
  .mode-btn.home-molde .mode-btn-desc{grid-area:desc; margin:8px 0 4px;}
  .mode-btn-chips{grid-area:chips; display:flex; flex-wrap:wrap; gap:8px; margin:10px 0 0; align-items:center;}
  .mode-chip{
    font-size:11px; border:1px solid var(--line); border-radius:999px;
    padding:4px 10px; color:var(--text-dim); background:var(--surface);
  }
  .mode-btn.home-molde .mode-chip{border-color:#e8d0b0; color:#8a5a20;}
  .home-mantas .mode-btn .mode-btn-cta,
  .mode-btn.home-molde .mode-btn-cta{
    grid-area:cta; justify-self:end; align-self:end;
    background:var(--brand); color:#fff; border-radius:999px;
    padding:8px 14px; margin:10px 0 0; font-size:12.5px;
  }
  .mode-btn.home-molde .mode-btn-cta{background:#c2782a; color:#fff;}
  @media (min-width:960px){
    .home-mantas{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px;}
    .home-moldes{display:block;}
  }"""

t = t[:i] + new_css + t[j:]
changed += 1
print("ok css")

icons = [
    (
        '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>',
        '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="8.2" cy="9.6" r="1.3"/><path d="m3 17 5.5-5.5 3.2 3.2 2.3-2.3L21 17"/>',
    ),
    (
        '<path d="M8 6h11a1 1 0 0 1 1 1v13H6V7a1 1 0 0 1 1-1h1z"/><path d="M8 6V4h6v2"/><path d="m9 12 2 2 4-4"/>',
        '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="m8.2 11 1.2 1.2L13 8.8"/><path d="M15.2 10.6h3"/><path d="m8.2 15.2 1.2 1.2L13 13"/><path d="M15.2 14.8h2.2"/><circle cx="17.4" cy="18.1" r="2.9"/><path d="m16.2 18.1 1 1.1 1.9-2"/>',
    ),
    (
        '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><rect x="7" y="7" width="10" height="10" rx="1"/>',
        '<path d="M4 9V6a2 2 0 0 1 2-2h3"/><path d="M15 4h3a2 2 0 0 1 2 2v3"/><path d="M20 15v3a2 2 0 0 1-2 2h-3"/><path d="M9 20H6a2 2 0 0 1-2-2v-3"/><rect x="8" y="8" width="8" height="8" rx="1"/>',
    ),
    (
        '<path d="M8 4c-2 2-3 5-2 8 2 5 6 8 10 7 2 0 4-3 3-6-1-4-5-7-8-9"/><path d="M9 9c1 2 3 4 6 5"/>',
        '<path d="M12 3.2c2.6.6 6.4 3.3 7.3 7.2 1.1 4.3-1.3 8-5 8.8-3.1.7-6.4-.7-8.3-3.8-2-3.2-1.7-7 .6-9.4C8.4 4.3 10.2 3.3 12 3.2z"/><path d="M8.1 10.6c1.7 2.7 4.4 4.8 8 5.4" stroke-dasharray="2.2 2"/>',
    ),
]
for old, new in icons:
    if old in t:
        t = t.replace(old, new, 1)
        changed += 1
        print("ok icon")
    else:
        print("MISSING icon", old[:50])

t = t.replace("<title>Dantix Leather Vision v211</title>", "<title>Dantix Leather Vision v212</title>", 1)
p.write_text(t, encoding="utf-8")
print("wrote html", p.stat().st_size, "changes", changed)

sw = Path("dantix-vision/sw.js")
s = sw.read_text(encoding="utf-8")
s = s.replace("service worker v211", "service worker v212")
s = s.replace("dantix-lv-v211-home-1", "dantix-lv-v212-home-2")
sw.write_text(s, encoding="utf-8")
print("wrote sw")
if changed < 2:
    raise SystemExit("pocos cambios")
