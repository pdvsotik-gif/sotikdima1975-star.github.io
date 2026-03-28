from PIL import Image
import os

# Настройки
FRAMES_DIR = "C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/images/character/animation"
OUTPUT_PATH = "C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/images/character/animation/character_animation.gif"

# Проверяем существование папки с кадрами
if not os.path.exists(FRAMES_DIR):
    print(f"Папка не найдена: {FRAMES_DIR}")
    exit(1)

# Собираем список кадров
frames = []
frame_files = sorted([f for f in os.listdir(FRAMES_DIR) if f.endswith('.png')])

if not frame_files:
    print(f"В папке {FRAMES_DIR} не найдено PNG-файлов")
    exit(1)

# Загружаем кадры
for frame_file in frame_files:
    frame_path = os.path.join(FRAMES_DIR, frame_file)
    try:
        frame = Image.open(frame_path)
        frames.append(frame)
        print(f"Загружен кадр: {frame_file}")
    except Exception as e:
        print(f"Ошибка при загрузке {frame_file}: {e}")

if frames:
    # Создаем GIF из кадров
    frames[0].save(
        OUTPUT_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=100,  # 100ms между кадрами (10 кадров в секунду)
        loop=0,  # бесконечный цикл
        transparency=0,
        disposal=2  # очищать предыдущий кадр
    )
    print(f"\nАнимация создана: {OUTPUT_PATH}")
    print(f"Количество кадров: {len(frames)}")
    print(f"Формат: GIF с прозрачностью")
else:
    print("Не удалось создать анимацию: нет загруженных кадров")