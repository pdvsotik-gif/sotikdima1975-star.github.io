from PIL import Image, ImageDraw, ImageFont
import os

def create_forza_placeholder():
    # Create image with specific dimensions 600x300 (3x larger)
    width, height = 600, 300
    img = Image.new('RGB', (width, height), '#0f172a')
    
    # Draw gradient background
    draw = ImageDraw.Draw(img)
    for i in range(height):
        # Create gradient from dark blue to slightly lighter blue
        r = int(15 + (i/height) * 10)
        g = int(23 + (i/height) * 15)
        b = int(42 + (i/height) * 20)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Draw racing elements
    # Circuit lines
    for y in range(0, height, 30):
        draw.rectangle([10, y+5, 45, y+20], fill='#fbbf24')  # Larger yellow track lines
    
    # Add Forza text
    try:
        # Try to use Arial font, fallback to default if not available
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()
    
    draw.text((width//2 - 100, height//2 - 40), "FORZA", fill='#fbbf24', font=font, font_size=60)
    draw.text((width//2 - 80, height//2 + 10), "MOTORSPORT", fill='#ffffff', font=font, font_size=40)
    
    # Add racing flag pattern
    for x in range(width-40, width, 15):
        for y in range(0, height, 25):
            color = '#ffffff' if (x+y) % 50 < 25 else '#000000'
            draw.rectangle([x, y, x+15, y+15], fill=color)
    
    # Save image
    from pathlib import Path
    BASE_DIR = Path(__file__).parent.parent
    output_dir = str(BASE_DIR / "images")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    img.save(f"{output_dir}/forza-placeholder.jpg", "JPEG", quality=95)
    print(f"Placeholder image created at {output_dir}/forza-placeholder.jpg")

if __name__ == "__main__":
    create_forza_placeholder()