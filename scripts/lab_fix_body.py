#!/usr/bin/env python3
from pathlib import Path

html = Path("dantix-vision-lab/index.html")
sw = Path("dantix-vision-lab/sw.js")
t = html.read_text(encoding="utf-8")

needle = "var bars = document.querySelectorAll('#dtx-precision-section .dtx-bar-fill')"
i = t.find(needle)
if i >= 0:
    start = t.rfind("<script>", 0, i)
    end = t.find("</script>", i)
    if start < 0 or end < 0:
        raise SystemExit("script bounds not found")
    end = end + len("</script>")
    while end < len(t) and t[end] in "\n\r":
        end += 1
    t = t[:start] + t[end:]
    print("removed injection", start, end)
else:
    print("no mid injection found")

js = (
    "\n<script>\n"
    "(function(){\n"
    "  var bars = document.querySelectorAll('#dtx-precision-section .dtx-bar-fill');\n"
    "  var target = document.getElementById('dtx-precision-section');\n"
    "  if(!target || !bars.length) return;\n"
    "  function fill(){\n"
    "    bars.forEach(function(bar){ bar.style.width = bar.getAttribute('data-width') + '%'; });\n"
    "  }\n"
    "  if(!('IntersectionObserver' in window)){ fill(); return; }\n"
    "  var observer = new IntersectionObserver(function(entries){\n"
    "    entries.forEach(function(entry){\n"
    "      if(entry.isIntersecting){ fill(); observer.disconnect(); }\n"
    "    });\n"
    "  }, {threshold:0.35});\n"
    "  observer.observe(target);\n"
    "})();\n"
    "</script>\n"
)
last = t.rfind("</body>")
nearby = t[max(0, last-500):last]
if last >= 0 and "dtx-precision-section .dtx-bar-fill" not in nearby:
    t = t[:last] + js + t[last:]
    print("appended at", last)
else:
    print("footer script already present or no body")

t = t.replace("LAB v223", "LAB v224")
html.write_text(t, encoding="utf-8")
print("bodies", t.count("</body"), "v224", "LAB v224" in t)

if sw.exists():
    s = sw.read_text(encoding="utf-8")
    s = s.replace("LAB v223", "LAB v224").replace("dantix-lv-lab-v223-precision", "dantix-lv-lab-v224-fixbody")
    sw.write_text(s, encoding="utf-8")
    print("sw ok")
print("ok")
