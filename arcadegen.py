from PIL import Image, ImageDraw, ImageFont
import os, requests, io

images = []
width = 0
height_base = 0

url = "https://overwatcharcade.today/api/overwatch/today"
r = requests.get(url).json()
modes = r["modes"]

for mode in modes:
    image_url = modes[mode]["image"]
    image = requests.get(image_url).content
    img = Image.open(io.BytesIO(image)).convert("RGBA")
    width_, height_ = img.size
    s = 200
    img_height = s * height_ / width_ # 400 : a = b : 9
    img = img.resize((s, int(img_height)))
    images.append(img)

count = 0
for i in images:
    if count > 4:
        height += height_base
        count = 0
    count += 1

base = Image.new('RGB', (1600, 900), color = None)
base_width, base_height = base.size
new_width = 0
new_height = 0
count = 0
for img in images:
    if count == 0:
        base.paste(img, (50, ))

base.save("test.png")
