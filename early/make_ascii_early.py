from PIL import Image, ImageEnhance, ImageOps
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE, "leimu.png")
img = Image.open(img_path)

gray = img.convert("L")
gray = ImageOps.autocontrast(gray, cutoff=1)
gray = ImageEnhance.Contrast(gray).enhance(3.0)
gray = ImageEnhance.Sharpness(gray).enhance(2.0)

W, H = 180, int(180 * img.height / img.width * 0.45)
gray_small = gray.resize((W, H), Image.LANCZOS)
gp = list(gray_small.getdata())

# Normal chars: @%#*+=-:. (dark -> light)
# Inverted: reverse the ramp so bright pixels = dense chars

# Version 1: Normal (dark ink on light paper)
chars = "@%#*+=-:. "
v1 = []
for y in range(H):
    row = gp[y * W:(y + 1) * W]
    v1.append("".join(chars[min(int(p/255*(len(chars)-1)), len(chars)-1)] for p in row))

# Version 2: Inverted (light ink on dark paper)
chars_inv = list(reversed(chars))
v2 = []
for y in range(H):
    row = gp[y * W:(y + 1) * W]
    v2.append("".join(chars_inv[min(int(p/255*(len(chars)-1)), len(chars)-1)] for p in row))

# Version 3: Block pixel inverted
gray2 = ImageOps.autocontrast(img.convert("L"), cutoff=1)
gray2 = ImageEnhance.Contrast(gray2).enhance(2.5)
Wb, Hb = 120, int(120 * img.height / img.width * 0.5)
gray2 = gray2.resize((Wb, Hb), Image.LANCZOS)
gp2 = list(gray2.getdata())

blocks = ['█', '▓', '▒', '░', ' ']
blocks_inv = list(reversed(blocks))
v3 = []
for y in range(Hb):
    row = gp2[y * Wb:(y + 1) * Wb]
    v3.append("".join(blocks_inv[min(int(p/255*len(blocks)), len(blocks)-1)] for p in row))

# ========================================
# HTML viewer with toggle
# ========================================
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Rem ASCII Art</title>
<style>
  :root {{ --bg: #1a1a2e; --text: #e0e0e0; }}
  body.light {{ --bg: #f5f0eb; --text: #222; }}
  body {{ background: var(--bg); color: var(--text); font-family: monospace; margin: 20px; transition: background 0.3s; }}
  h2 {{ color: #66aaff; margin: 20px 0 5px; }}
  body.light h2 {{ color: #3366cc; }}
  .container {{ margin-bottom: 30px; }}
  .ascii {{
    font-family: "Courier New", "Source Code Pro", "Consolas", "DejaVu Sans Mono", monospace;
    line-height: 1.0; white-space: pre; margin: 8px 0;
  }}
  .small {{ font-size: 3px; letter-spacing: 0; }}
  .block {{ font-size: 5px; line-height: 0.9; }}
  .zoom-hint {{ color: #999; font-size: 13px; }}
  button, input {{ font-size: 13px; }}
  .toolbar {{
    position: sticky; top: 0; background: var(--bg); padding: 12px 0;
    border-bottom: 1px solid #444; margin-bottom: 20px; z-index: 10;
    display: flex; align-items: center; gap: 15px; flex-wrap: wrap;
  }}
</style></head><body>
<div class="toolbar">
  <strong style="font-size:16px;">Rem (雷姆) - ASCII Art</strong>
  <label>Font: <input type="range" id="zoom" min="1" max="16" value="3"
    oninput="document.querySelectorAll('.ascii').forEach(e=>e.style.fontSize=this.value+'px');document.getElementById('zoomVal').textContent=this.value+'px'"></label>
  <span id="zoomVal">3px</span>
  <button onclick="document.body.classList.toggle('light')">Toggle Theme</button>
</div>

<div class="container">
  <h2>Inverted (light on dark) - {W}x{H}</h2>
  <pre class="ascii small">{esc(chr(10).join(v2))}</pre>
</div>

<div class="container">
  <h2>Block Inverted (light on dark) - {Wb}x{Hb}</h2>
  <pre class="ascii block">{esc(chr(10).join(v3))}</pre>
</div>

<div class="container">
  <h2>Original (dark on light) - {W}x{H}</h2>
  <pre class="ascii small">{esc(chr(10).join(v1))}</pre>
</div>

</body></html>"""

with open(os.path.join(BASE, "leimu_ascii.html"), "w", encoding="utf-8") as f:
    f.write(html)

# Also save individual inverted files
with open(os.path.join(BASE, "leimu_inverted.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(v2))
with open(os.path.join(BASE, "leimu_block_inverted.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(v3))

print("Done! Generated inverted versions.")
print(f"  leimu_inverted.txt - {W}x{H} inverted")
print(f"  leimu_block_inverted.txt - {Wb}x{Hb} block inverted")
print(f"  leimu_ascii.html - interactive viewer with theme toggle")
print()
print("Inverted preview:")
for l in v2[:8]:
    print(l)
print()
print("Block inverted preview:")
for l in v3[:8]:
    print(l)
