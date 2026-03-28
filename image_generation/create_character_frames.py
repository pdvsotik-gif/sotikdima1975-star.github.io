from PIL import Image
import os

# Настройки
CHARACTER_PATH = "C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/images/character/character.png"
OUT_DIR = "C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/images/character/animation"

# Создаем папку для кадров
os.makedirs(OUT_DIR, exist_ok=True)

# Загружаем изображение персонажа
src = Image.open(CHARACTER_PATH)

# Создаем 8 кадров анимации с поворотом
for i in range(8):
    frame = src.copy()
    frame = frame.rotate(-2 + i * 0.5, resample=Image.BICUBIC, expand=False)
    frame.save(f"{OUT_DIR}/frame_{i}.png")

print(f"Создано 8 кадров анимации в папке: {OUT_DIR}")
print("Анимация поворота персонажа готова к использованию")