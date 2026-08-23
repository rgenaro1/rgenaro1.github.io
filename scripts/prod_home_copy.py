#!/usr/bin/env python3
from pathlib import Path

p = Path("dantix-vision/index.html")
t = p.read_text(encoding="utf-8")

old = (
    '<path d="M12 3.2c2.6.6 6.4 3.3 7.3 7.2 1.1 4.3-1.3 8-5 8.8-3.1.7-6.4-.7-8.3-3.8-2-3.2-1.7-7 .6-9.4C8.4 4.3 10.2 3.3 12 3.2z"/>'
    '<path d="M8.1 10.6c1.7 2.7 4.4 4.8 8 5.4" stroke-dasharray="2.2 2"/>'
)
new = (
    '<path d="M12 3c2.1 0 3.6 1.2 4.6 2.4 1.8 2.1 4.2 3.2 4.2 6.2 0 2-1.1 3.3-2.7 4.1-.6.3-1 .9-.9 1.5l.3 2.2c.2 1.1-1.1 2-3.5 2H9c-2.4 0-3.7-.9-3.5-2l.3-2.2c.1-.6-.3-1.2-.9-1.5C3.3 14.9 2.2 13.6 2.2 11.6c0-3 2.4-4.1 4.2-6.2C7.4 4.2 8.9 3 12 3z"/>'
    '<path d="M8.2 10.6c1.6 2.3 3.9 3.8 7.6 4.3" stroke-dasharray="2 2"/>'
    '<path d="M10 7.2h4"/>'
)
if old not in t:
    raise SystemExit("no se encontro icono pattern")
t = t.replace(old, new, 1)
t = t.replace("<title>Dantix Leather Vision v212</title>", "<title>Dantix Leather Vision v213</title>", 1)
p.write_text(t, encoding="utf-8")
print("wrote html", p.stat().st_size)

sw = Path("dantix-vision/sw.js")
s = sw.read_text(encoding="utf-8")
s = s.replace("service worker v212", "service worker v213")
s = s.replace("dantix-lv-v212-home-2", "dantix-lv-v213-pattern-1")
sw.write_text(s, encoding="utf-8")
print("wrote sw")
