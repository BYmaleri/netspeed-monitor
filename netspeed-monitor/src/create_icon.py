"""
NetSpeed Monitor için .ico dosyası üretir.
Build sırasında PyInstaller öncesi çalıştırılır.
Gereksinim: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

SIZES = [16, 24, 32, 48, 64, 128, 256]

def make_icon(path: str):
    frames = []
    for size in SIZES:
        img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Arka plan – koyu yuvarlak dikdörtgen
        r = size // 6
        draw.rounded_rectangle([0, 0, size - 1, size - 1],
                                radius=r,
                                fill=(17, 17, 17, 255))

        # Yeşil çubuk (indirme)
        bar_h = max(2, size // 8)
        y1    = size // 4
        draw.rectangle([size//6, y1, size*5//6, y1 + bar_h],
                       fill=(74, 222, 128, 255))

        # Turuncu çubuk (yükleme)
        y2 = size * 5 // 8
        draw.rectangle([size//6, y2, size*5//6, y2 + bar_h],
                       fill=(251, 146, 60, 255))

        frames.append(img)

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    frames[0].save(path, format="ICO", sizes=[(s, s) for s in SIZES],
                   append_images=frames[1:])
    print(f"✔ İkon oluşturuldu: {path}")


if __name__ == "__main__":
    make_icon("assets/icon.ico")
