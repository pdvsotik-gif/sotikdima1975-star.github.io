# Image Generation System

This directory contains tools for generating images from text prompts using Stable Diffusion.

## Installation

1. Make sure you have Python 3.8+ installed
2. Install the required packages:

```bash
pip install torch torchvision transformers diffusers accelerate pillow
```

## Usage

### Command Line

```bash
# Basic usage
python generate_image.py "A beautiful sunset over mountains" --output ../images/generated/sunset.jpg

# With custom resolution
python generate_image.py "A futuristic city at night" --output ../images/generated/city.jpg --width 1920 --height 1080 --steps 50
```

### Python Script

```python
from image_generator import generate_image_from_prompt

# Generate an image
result = generate_image_from_prompt(
    "A cinematic racing scene at sunset", 
    "../images/generated/racing.jpg", 
    width=1920, 
    height=1080
)

if result.startswith("Error"):
    print(f"Generation failed: {result}")
else:
    print(f"Image generated at: {result}")
```

## Features

- Uses Stable Diffusion 2.1 for high-quality image generation
- Optimized for 1920x1080 resolution (can generate any size)
- Includes memory optimization for lower-end GPUs
- Pre-configured with sensible defaults for fast generation
- Supports custom prompts, resolutions, and quality settings

## Example Prompts

- "A cinematic racing scene at sunset with dramatic lighting, professional motorsport photography, ultra sharp, 8k"
- "A futuristic cityscape at night with neon lights reflecting on wet streets, cyberpunk style"
- "A serene mountain landscape at dawn with mist flowing through valleys, national geographic photo"
- "A vintage sports car driving on a coastal road during golden hour, cinematic composition"

## Notes

- Generation quality improves with more inference steps (default: 50)
- The first run will download the model (approximately 5GB)
- GPU acceleration is highly recommended for reasonable generation times
- On CPU, generation may take several minutes per image
- Images are saved in JPEG format with high quality (95%)