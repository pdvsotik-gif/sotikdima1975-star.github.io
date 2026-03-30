from pathlib import Path
from PIL import Image, ImageSequence
import os

# Настройки
BASE_DIR = Path(__file__).parent.parent
CHARACTER_PATH = BASE_DIR / "images" / "character" / "character.png"
OUTPUT_DIR = BASE_DIR / "images" / "character" / "animation"
FRAME_COUNT = 8

# Создаем папку для анимации
os.makedirs(str(OUTPUT_DIR), exist_ok=True)

# Загружаем персонажа без фона
character = Image.open(CHARACTER_PATH).convert("RGBA")
width, height = character.size

# Создаем кадры анимации
for i in range(FRAME_COUNT):
    # Создаем новое изображение
    frame = Image.new("RGBA", (width * 2, height), (0, 0, 0, 0))
    
    # Рассчитываем позицию персонажа
    progress = i / (FRAME_COUNT - 1)
    x_pos = int(width * 0.2 + width * 1.2 * progress)
    
    # Для жеста руками используем простую анимацию
    # Масштабируем персонажа в зависимости от фазы жеста
    if i % 4 == 0 or i % 4 == 1:
        # Руки вниз
        scale = 1.0
    else:
        # Руки вверх (жест)
        scale = 1.1
    
    # Изменяем размер персонажа
    frame_width = int(width * scale)
    frame_height = int(height * scale)
    resized_character = character.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
    
    # Вставляем персонажа
    frame.paste(resized_character, (int(x_pos - frame_width/2), int(height/2 - frame_height/2)), resized_character)
    
    # Сохраняем кадр
    frame.save(f"{OUTPUT_DIR}/char_{i:03d}.png", "PNG")
    
    print(f"Кадр {i+1}/{FRAME_COUNT} сгенерирован")

print(f"Анимация персонажа создана: {OUTPUT_DIR}")