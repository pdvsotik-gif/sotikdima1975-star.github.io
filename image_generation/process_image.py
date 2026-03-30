from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import os

# === Исходное изображение ===
BASE_DIR = Path(__file__).parent.parent
SOURCE = BASE_DIR / "images" / "cayman2017.jpg"

# === Папка для результата ===
OUT = BASE_DIR / "images" / "wallpapers"
os.makedirs(str(OUT), exist_ok=True)

img = Image.open(SOURCE).convert("RGB")

# === 1. Тёплый вариант (Sunset Warm) ===
warm = img.copy()
warm = ImageEnhance.Contrast(warm).enhance(1.15)
warm = ImageEnhance.Color(warm).enhance(1.25)
warm = warm.filter(ImageFilter.GaussianBlur(0.3))
warm.save(f"{OUT}/hero-1.jpg", quality=95)

# === 2. Ночной вариант (Night Mode) ===
night = img.copy()
night = ImageEnhance.Brightness(night).enhance(0.60)
night = ImageEnhance.Color(night).enhance(0.55)
night = night.filter(ImageFilter.GaussianBlur(1.2))
night.save(f"{OUT}/hero-2.jpg", quality=95)

# === 3. Агрессивный вариант (Track Heat) ===
heat = img.copy()
heat = ImageEnhance.Contrast(heat).enhance(1.30)
heat = ImageEnhance.Color(heat).enhance(1.40)
heat = heat.filter(ImageFilter.GaussianBlur(0.6))
heat.save(f"{OUT}/hero-3.jpg", quality=95)

print("Готово! Файлы сохранены в папку:", OUT)