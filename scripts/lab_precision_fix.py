#!/usr/bin/env python3
from pathlib import Path

HTML = Path("dantix-vision-lab/index.html")
SW = Path("dantix-vision-lab/sw.js")
t = HTML.read_text(encoding="utf-8")

JS = """
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

start = t.find("<script>\n(function(){\n  var bars = document.querySelectorAll('#dtx-precision-section .dtx-bar-fill')")
if start < 0:
    start = t.find("var bars = document.querySelectorAll('#dtx-precision-section .dtx-bar-fill')")
    if start >= 0:
        start = t.rfind("<script>", 0, start)

removed = 0
while start >= 0:
    end = t.find("</script>", start)
    if end < 0:
        break
    end += len("</script>")
    last_body = t.rfind("</body>")
    if start > last_body - 800 and start < last_body:
        break
    t = t[:start] + t[end:]
    removed += 1
    start = t.find("<script>\n(function(){\n  var bars = document.querySelectorAll('#dtx-precision-section .dtx-bar-fill')")

last_body = t.rfind("</body>")
if last_body < 0:
    raise SystemExit("no </body>")
if "dtx-precision-section .dtx-bar-fill" not in t[last_body-900:last_body]:
    t = t[:last_body] + JS + "\n" + t[last_body:]

t = t.replace("LAB v223", "LAB v224")
t = t.replace("LAB v222", "LAB v224")
HTML.write_text(t, encoding="utf-8")
print("removed", removed, "size", HTML.stat().st_size, "section", 'id="dtx-precision-section"' in t)

if SW.exists():
    sw = SW.read_text(encoding="utf-8")
    for old in ("dantix-lv-lab-v223-precision", "dantix-lv-lab-v222-studio", "LAB v223", "LAB v222"):
        sw = sw.replace(old, "dantix-lv-lab-v224-fix" if old.startswith("dantix") else "LAB v224")
    SW.write_text(sw, encoding="utf-8")
    print("sw ok")
print("ok")
