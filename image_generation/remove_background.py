from rembg import remove
from PIL import Image
import os

# Настройки
INPUT_PATH = "C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/images/image1.png"
OUTPUT_DIR = "C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/images/character"

# Создаем папку для результатов
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Удаляем фон
input_image = Image.open(INPUT_PATH)
output_image = remove(input_image)

# Сохраняем результат
output_path = f"{OUTPUT_DIR}/character.png"
output_image.save(output_path, "PNG")

print(f"Фон удален. Изображение сохранено: {output_path}")