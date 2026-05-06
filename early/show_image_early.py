from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(BASE, "leimu.png")
img = Image.open(img_path)
print(f"Size: {img.size}, Mode: {img.mode}")

# Show histogram distribution
gray = img.convert("L")
pixels = list(gray.getdata())
print(f"Min pixel: {min(pixels)}, Max pixel: {max(pixels)}, Avg: {sum(pixels)//len(pixels)}")

# Try different edge-detection approaches and pick best

# Approach 1: Edge detection line-art style
edges = img.convert("L")
edges = edges.filter(ImageFilter.FIND_EDGES)
edges = ImageOps.invert(edges)
edges = ImageEnhance.Contrast(edges).enhance(3.0)

width = 200
aspect = img.height / img.width
height = int(width * aspect * 0.45)
edges = edges.resize((width, height), Image.LANCZOS)

chars = "@%#*+=-:. "
ep = list(edges.getdata())
elines = []
for y in range(height):
    row = ep[y * width:(y + 1) * width]
    elines.append("".join(chars[min(int(p/255*(len(chars)-1)), len(chars)-1)] for p in row))

with open(os.path.join(BASE, "leimu_ascii_edge.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(elines))

print("\n=== Edge style (leimu_ascii_edge.txt) ===")
for l in elines[:10]:
    print(l)

# Approach 2: High-contrast standard
std = ImageEnhance.Contrast(img).enhance(2.0)
std = ImageEnhance.Sharpness(std).enhance(2.0)
std = std.resize((width, height), Image.LANCZOS)
std = std.convert("L")

sp = list(std.getdata())
slines = []
for y in range(height):
    row = sp[y * width:(y + 1) * width]
    slines.append("".join(chars[min(int(p/255*(len(chars)-1)), len(chars)-1)] for p in row))

with open(os.path.join(BASE, "leimu_ascii.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(slines))

print("\n=== High contrast style (leimu_ascii.txt) ===")
for l in slines[:10]:
    print(l)
