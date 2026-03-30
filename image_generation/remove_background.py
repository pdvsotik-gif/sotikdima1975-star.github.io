from pathlib import Path
from rembg import remove
from PIL import Image
import os

# Настройки
BASE_DIR = Path(__file__).parent.parent
INPUT_PATH = BASE_DIR / "images" / "image1.png"
OUTPUT_DIR = BASE_DIR / "images" / "character"

# Создаем папку для результатов
os.makedirs(str(OUTPUT_DIR), exist_ok=True)

# Удаляем фон
input_image = Image.open(INPUT_PATH)
output_image = remove(input_image)

# Сохраняем результат
output_path = f"{OUTPUT_DIR}/character.png"
output_image.save(output_path, "PNG")

print(f"Фон удален. Изображение сохранено: {output_path}")