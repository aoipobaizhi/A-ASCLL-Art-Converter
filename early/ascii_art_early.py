import sys
import io
import os
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE, "leimu.png")
img = Image.open(img_path)
print(f"Original size: {img.size}")

# Gentle enhancement - don't crush details
img = ImageEnhance.Contrast(img).enhance(1.3)
img = ImageEnhance.Sharpness(img).enhance(1.8)
img = ImageEnhance.Brightness(img).enhance(1.1)

# Auto-equalize for better tonal range
img = ImageOps.autocontrast(img, cutoff=2)

# High resolution - 200 chars wide
width = 200
aspect = img.height / img.width
height = int(width * aspect * 0.45)  # slightly less vertical compression
img = img.resize((width, height), Image.LANCZOS)
img = img.convert("L")

# Rich character ramp for detailed gradation
chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "

pixels = list(img.getdata())

# Build pixel intensity histogram for adaptive mapping
lines = []
for y in range(height):
    row = pixels[y * width:(y + 1) * width]
    line = ""
    for p in row:
        idx = min(int(p / 255 * (len(chars) - 1)), len(chars) - 1)
        line += chars[idx]
    lines.append(line)

result = "\n".join(lines)

with open(os.path.join(BASE, "leimu_ascii.txt"), "w", encoding="utf-8") as f:
    f.write(result)

print(f"Output size: {width}x{height}")
print("Done! Open leimu_ascii.txt and zoom out / shrink font to see full image.")
# Print first few lines as preview
for line in lines[:8]:
    print(line)
