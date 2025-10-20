# project2-multimodal/create_test_inputs.py
# Creates photo.jpg, document.png, chart.png, and a sample long_text.txt
# IMPORTANT: run this script from anywhere; it will place files into the same folder as itself.

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
IMAGES = HERE / "images"
IMAGES.mkdir(parents=True, exist_ok=True)

# 1) photo.jpg (simple mock scene)
photo_path = IMAGES / "photo.jpg"
img = Image.new("RGB", (1024, 768), color=(120, 180, 200))
draw = ImageDraw.Draw(img)
draw.rectangle([50, 300, 300, 700], fill=(200,120,120))
draw.ellipse([600,150,900,450], fill=(120,200,140))
draw.text((60, 50), "Sample photo scene", fill=(0,0,0))
img.save(photo_path)
print("WROTE:", photo_path)

# 2) document.png (synthetic doc for OCR)
doc_path = IMAGES / "document.png"
w,h = 1200,1600
doc = Image.new("RGB", (w,h), color="white")
draw = ImageDraw.Draw(doc)
lines = [
    "Title: Sample Research Report",
    "Author: Test Author",
    "",
    "Abstract: This is a synthetic abstract used to test OCR and document extraction.",
    "We demonstrate extraction of headings, paragraphs, and small tables.",
    "",
    "1. Introduction",
    "This document is created for the multimodal assignment.",
    "",
    "2. Methods",
    "We used sample data and synthetic text.",
    "",
    "Table 1: Results",
    "Metric,Value",
    "Accuracy,0.92",
    "F1,0.89",
]
y = 40
for line in lines:
    draw.text((40, y), line, fill=(0,0,0))
    y += 40
doc.save(doc_path)
print("WROTE:", doc_path)

# 3) chart.png (matplotlib)
chart_path = IMAGES / "chart.png"
months = ["Jan","Feb","Mar","Apr","May","Jun"]
sales = [100, 150, 130, 180, 220, 210]
plt.figure(figsize=(8,5))
plt.plot(months, sales, marker='o')
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales (units)")
plt.grid(True)
plt.tight_layout()
plt.savefig(chart_path, dpi=200)
plt.close()
print("WROTE:", chart_path)

# 4) long_text.txt (small example; replace with large file later)
long_path = HERE / "long_text.txt"
sample_long = ("This is a demo long text. " * 2000).strip()
long_path.write_text(sample_long, encoding="utf8")
print("WROTE:", long_path, "size:", long_path.stat().st_size)

# 5) show created files
print("\nCreated files under:", HERE)
for p in sorted(list((HERE).glob("*")) + list((IMAGES).glob("*"))):
    print("-", p.relative_to(HERE))
