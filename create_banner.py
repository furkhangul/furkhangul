from PIL import Image, ImageDraw, ImageFont, ImageFilter

INPUT_GIF = "background.gif"
OUTPUT_GIF = "furkan-gul.gif"

TEXT = "Furkan Gül"

# İmza tarzı font
FONT_PATH = "GreatVibes-Regular.ttf"

gif = Image.open(INPUT_GIF)

width, height = gif.size

# Görselin oranına göre otomatik font boyutu
font_size = int(width * 0.14)

font = ImageFont.truetype(FONT_PATH, font_size)

frames = []
durations = []

for i in range(gif.n_frames):

    gif.seek(i)

    frame = gif.convert("RGBA")

    # =========================
    # YAZI KONUMU
    # =========================

    draw = ImageDraw.Draw(frame)

    bbox = draw.textbbox(
        (0, 0),
        TEXT,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # TAM ORTA
    x = (width - text_width) / 2
    y = (height - text_height) / 2 - bbox[1]

    # =========================
    # HAFİF SİYAH GÖLGE
    # =========================

    shadow = Image.new(
        "RGBA",
        frame.size,
        (0, 0, 0, 0)
    )

    shadow_draw = ImageDraw.Draw(shadow)

    shadow_draw.text(
        (x + 2, y + 3),
        TEXT,
        font=font,
        fill=(0, 0, 0, 190)
    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(3)
    )

    frame = Image.alpha_composite(
        frame,
        shadow
    )

    # =========================
    # ÇOK HAFİF BEYAZ GLOW
    # =========================

    glow = Image.new(
        "RGBA",
        frame.size,
        (0, 0, 0, 0)
    )

    glow_draw = ImageDraw.Draw(glow)

    glow_draw.text(
        (x, y),
        TEXT,
        font=font,
        fill=(255, 255, 255, 100)
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(4)
    )

    frame = Image.alpha_composite(
        frame,
        glow
    )

    # =========================
    # ANA İMZA
    # =========================

    draw = ImageDraw.Draw(frame)

    draw.text(
        (x, y),
        TEXT,
        font=font,
        fill=(255, 255, 255, 245)
    )

    frames.append(
        frame.convert("P", palette=Image.ADAPTIVE)
    )

    durations.append(
        gif.info.get("duration", 50)
    )

# =========================
# GIF OLARAK KAYDET
# =========================

frames[0].save(
    OUTPUT_GIF,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    disposal=2,
    optimize=False
)

print("Hazır:", OUTPUT_GIF)
print("Orijinal GIF boyutu korundu:", width, "x", height)
