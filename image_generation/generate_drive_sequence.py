from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import os
import numpy as np

# Настройки
SOURCE = "C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/images/cayman2017.jpg"
OUT = "C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/images/drive"
FRAME_COUNT = 12  # Количество кадров для эффекта движения

# Создаем папку для результатов
os.makedirs(OUT, exist_ok=True)

# Открываем исходное изображение
img = Image.open(SOURCE).convert("RGB")
width, height = img.size

print(f"Генерация последовательности из {FRAME_COUNT} кадров...")

for i in range(FRAME_COUNT):
    # Рассчитываем позицию движения (от левого края к правому)
    progress = i / (FRAME_COUNT - 1)  # 0.0 до 1.0
    
    # Создаем копию изображения
    frame = img.copy()
    
    # Эффект движения: небольшой размытие в направлении движения
    if i > 0 and i < FRAME_COUNT - 1:
        # Увеличиваем размытие в зависимости от скорости
        motion_blur_radius = 0.3 + progress * 0.7
        frame = frame.filter(ImageFilter.GaussianBlur(motion_blur_radius))
    
    # Эффект параллакса: небольшое смещение изображения
    # Имитирует движение камеры при проезде мимо
    parallax_shift = int(width * 0.1 * progress)
    frame = ImageOps.crop(frame, (parallax_shift, 0, 0, 0))
    frame = frame.resize((width, height), Image.Resampling.LANCZOS)
    
    # Сохраняем кадр
    frame.save(f"{OUT}/drive_{i:03d}.jpg", quality=95)
    
    # Печатаем прогресс
    print(f"Кадр {i+1}/{FRAME_COUNT} сгенерирован")

print(f"Готово! Последовательность сохранена в папку: {OUT}")