from pathlib import Path
from PIL import Image
import os

# Настройки
BASE_DIR = Path(__file__).parent.parent
CHARACTER_PATH = BASE_DIR / "images" / "character" / "character.png"
OUT_DIR = BASE_DIR / "images" / "character" / "animation"

# Создаем папку для кадров
os.makedirs(str(OUT_DIR), exist_ok=True)

# Загружаем изображение персонажа
src = Image.open(CHARACTER_PATH)

# Создаем 8 кадров анимации с поворотом
for i in range(8):
    frame = src.copy()
    frame = frame.rotate(-2 + i * 0.5, resample=Image.BICUBIC, expand=False)
    frame.save(f"{OUT_DIR}/frame_{i}.png")

print(f"Создано 8 кадров анимации в папке: {OUT_DIR}")
print("Анимация поворота персонажа готова к использованию")