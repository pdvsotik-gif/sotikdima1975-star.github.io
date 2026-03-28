import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import numpy as np
from PIL import Image
import os
import argparse

def generate_image(prompt, output_path, width=1920, height=1080, num_inference_steps=50):
    """
    Generate an image from a text prompt using Stable Diffusion.
    
    Args:
        prompt (str): Text prompt describing the image to generate
        output_path (str): Path where to save the generated image
        width (int): Width of the generated image (default: 1920)
        height (int): Height of the generated image (default: 1080)
        num_inference_steps (int): Number of denoising steps (higher = better quality but slower)
    """
    
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load the model
    # Using a smaller, faster model for better performance
    model_id = "stabilityai/stable-diffusion-2-1-base"
    
    # Use Euler scheduler for faster generation
    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    
    # Load pipeline
    try:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler)
        pipe = pipe.to(device)
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Trying with lower memory requirements...")
        
        # Try with lower memory requirements
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            scheduler=scheduler,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        )
        pipe = pipe.to(device)
    
    # Enable attention slicing to reduce memory usage
    if device == "cuda":
        pipe.enable_attention_slicing()
    
    # Generate image
    print(f"Generating image with prompt: '{prompt}'")
    print(f"Resolution: {width}x{height}")
    
    with torch.no_grad():
        try:
            result = pipe(
                prompt,
                width=width,
                height=height,
                num_inference_steps=num_inference_steps,
                guidance_scale=7.5,
                generator=torch.Generator(device).manual_seed(42) if device == "cuda" else None
            )
            
            image = result.images[0]
            
            # Save image
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            image.save(output_path, "JPEG", quality=95)
            print(f"Image saved to {output_path}")
            
            return image
            
        except Exception as e:
            print(f"Error during image generation: {e}")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate images from text prompts')
    parser.add_argument('prompt', type=str, help='Text prompt for image generation')
    parser.add_argument('--output', '-o', type=str, default='generated_image.jpg', 
                       help='Output path for the generated image')
    parser.add_argument('--width', '-w', type=int, default=1920, help='Image width')
    parser.add_argument('--height', '-h', type=int, default=1080, help='Image height')
    parser.add_argument('--steps', '-s', type=int, default=50, help='Number of inference steps')
    
    args = parser.parse_args()
    
    generate_image(args.prompt, args.output, args.width, args.height, args.steps)