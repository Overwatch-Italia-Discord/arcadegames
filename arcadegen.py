from PIL import Image, ImageDraw, ImageFont
import os, requests, io

class ArcadeImage:
    def __init__(self, image, name, players, label=None):
        self.image = image
        self.name = name
        self.players = players
        self.label = label

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
    s = 162.5
    img_width = s * width_ / height_ # 375 : a = x : b
    img = img.resize((int(img_width), int(s)))
    ai = ArcadeImage(img, modes[mode]["name"], modes[mode]["players"], modes[mode]["label"])
    images.append(ai)

# base = Image.new('RGB', (1600, 900), color = None)
base = Image.open("background.jpg").resize((1600, 900))
font_size = 60
font = ImageFont.truetype('bignoodletoo.ttf', font_size)
small_font = ImageFont.truetype('bignoodletoo.ttf', int(font_size - 10))
d = ImageDraw.Draw(base)
base_width, base_height = base.size
new_width = 0
new_height = 50
count = 0
border_space = 50

total_height = 0

for i in images:
    img = i.image
    img_width, img_height = img.size
    if (count % 2) == 0:
        base.paste(img, (border_space, new_height), img)
        text_width = int(img_width + border_space * 2)
        text_height = new_height
    else:
        s = base_width / 2 + border_space
        base.paste(img, (int(s), new_height), img)
        text_width = int(s + img_width + border_space)
        text_height = new_height
        new_height += (img_height + border_space)

    d.text((int(text_width + 5), int(text_height + 5)), i.name, fill=(0,0,0), font=font) # shadow
    d.text((text_width, text_height), i.name, fill=(255,255,255), font=font)

    d.text((int(text_width + 5), int(text_height + font_size + 5)), i.players, fill=(0,0,0), font=small_font) # shadow
    d.text((text_width, int(text_height + font_size)), i.players, fill=(255,255,255), font=small_font)
    if i.label:
        d.text((int(text_width + 5), int(text_height + font_size + (font_size - 10) + 5)), i.label, fill=(0,0,0), font=small_font)
        d.text((text_width, int(text_height + font_size + (font_size - 10))), i.label, fill=(255,255,255), font=small_font)

    count += 1
base.save("test.png")
