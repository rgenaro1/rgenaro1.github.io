#!/usr/bin/env python3
from pathlib import Path

html = Path("dantix-vision-lab/index.html")
sw = Path("dantix-vision-lab/sw.js")
t = html.read_text(encoding="utf-8")

start = t.find("\n<script>\n(function(){\n  var bars = document.querySelectorAll('#dtx-precision-section")
if start < 0:
    start = t.find('<script>\n(function(){\n  var bars = document.querySelectorAll("#dtx-precision-section")
if start >= 0:
    end = t.find("</script>", start)
    if end < 0:
        raise SystemExit("no close script")
    end = end + len("</script>")
    while end < len(t) and t[end] in "\n\r":
        end += 1
    t = t[:start] + t[end:]
    print("removed mid-jspdf injection", start)
else:
    print("no mid injection found")

js = """
<script>
(function(){
  var bars = document.querySelectorAll('#dtx-precision-section .dtx-bar-fill');
  var target = document.getElementById('dtx-precision-section');
  if(!target || !bars.length) return;
  function fill(){
    bars.forEach(function(bar){ bar.style.width = bar.getAttribute('data-width') + '%'; });
  }
  if(!('IntersectionObserver' in window)){ fill(); return; }
  var observer = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){ fill(); observer.disconnect(); }
    });
  }, {threshold:0.35});
  observer.observe(target);
})();
</script>
"""
last = t.rfind("</body>")
nearby = t[max(0, last-800):last]
if last >= 0 and "dtx-precision-section .dtx-bar-fill" not in nearby:
    t = t[:last] + js + "\n" + t[last:]
    print("appended script at real </body>", last)
else:
    print("footer script already present or no body")

t = t.replace("LAB v223", "LAB v224")
html.write_text(t, encoding="utf-8")
print("bodies", t.count("</body>"), "title", "LAB v224" in t)

if sw.exists():
    s = sw.read_text(encoding="utf-8")
    s = s.replace("LAB v223", "LAB v224").replace("dantix-lv-lab-v223-precision", "dantix-lv-lab-v224-fixbody")
    sw.write_text(s, encoding="utf-8")
    print("sw ok")
print("ok")
