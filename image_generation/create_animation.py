from PIL import Image, ImageDraw
import os
import math

def create_animated_character():
    # Пути
    input_path = "C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/images/character/character.png"
    output_dir = "C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/images/character/anims"
    
    # Создаем папку для анимации
    os.makedirs(output_dir, exist_ok=True)
    
    # Открываем изображение персонажа
    character = Image.open(input_path)
    
    # Параметры анимации
    frames = 30  # количество кадров
    duration = 2.0  # секунд
    amplitude = 20  # амплитуда движения
    frequency = 2.0  # частота движения
    
    # Создаем кадры анимации
    for i in range(frames):
        # Создаем новое изображение
        img = Image.new('RGBA', (800, 600), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Рассчитываем позицию
        t = i / frames
        x = 400 + amplitude * math.sin(t * frequency * 2 * math.pi)
        y = 300 + amplitude * math.cos(t * frequency * 2 * math.pi)
        
        # Вставляем персонажа
        img.paste(character, (int(x - character.width // 2), int(y - character.height // 2)), character)
        
        # Сохраняем кадр
        img.save(f"{output_dir}/frame_{i:03d}.png", 'PNG')
    
    # Создаем GIF
    images = []
    for i in range(frames):
        images.append(Image.open(f"{output_dir}/frame_{i:03d}.png"))
    
    images[0].save(
        f"{output_dir}/character_animated.gif",
        save_all=True,
        append_images=images[1:],
        duration=int(duration * 1000 / frames),
        loop=0,
        transparency=0
    )
    
    print(f"Анимация создана: {output_dir}/character_animated.gif")
    print(f"Создано {frames} кадров")

if __name__ == "__main__":
    create_animated_character()