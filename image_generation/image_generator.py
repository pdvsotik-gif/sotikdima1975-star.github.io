import subprocess
import sys
import os

def install_requirements():
    """
    Install required packages for image generation.
    """
    required_packages = [
        "torch", 
        "torchvision", 
        "transformers", 
        "diffusers", 
        "accelerate",
        "pillow"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} is already installed")
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ])


def generate_image_from_prompt(prompt, output_path="generated_image.jpg", width=1920, height=1080):
    """
    Generate an image from a text prompt using the Stable Diffusion model.
    
    Args:
        prompt (str): Text description of the image to generate
        output_path (str): Path where to save the generated image
        width (int): Width of the generated image
        height (int): Height of the generated image
    
    Returns:
        str: Path to the generated image or error message
    """
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        
        # Run the image generation script
        result = subprocess.run([
            sys.executable, "generate_image.py",
            prompt,
            "--output", output_path,
            "--width", str(width),
            "--height", str(height)
        ], cwd="C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/image_generation", capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Image generated successfully: {output_path}")
            return output_path
        else:
            error_msg = f"Image generation failed: {result.stderr}"
            print(error_msg)
            return error_msg
            
    except Exception as e:
        error_msg = f"Error running image generation: {str(e)}"
        print(error_msg)
        return error_msg


def main():
    """Example usage of the image generator."""
    print("Installing required packages...")
    install_requirements()
    
    # Example prompts
    example_prompts = [
        "A cinematic racing scene at sunset with dramatic lighting, professional motorsport photography, ultra sharp, 8k", 
        "A futuristic cityscape at night with neon lights reflecting on wet streets, cyberpunk style",
        "A serene mountain landscape at dawn with mist flowing through valleys, national geographic photo"
    ]
    
    print("\nGenerating example images...")
    for i, prompt in enumerate(example_prompts):
        output_path = f"C:/Users/sotik/IdeaProjects/sotikdima1975-star.github.io/image_generation/generated_examples/example_{i+1}.jpg"
        generate_image_from_prompt(prompt, output_path)
        
    print("\nSetup complete! You can now generate images with custom prompts.")

if __name__ == "__main__":
    main()