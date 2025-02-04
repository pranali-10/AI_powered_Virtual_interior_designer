# interior_design.py

from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

class InteriorDesignGenerator:
    def __init__(self):
        # Load the Stable Diffusion model
        model_id = "stabilityai/stable-diffusion-2-1"
        self.pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)  # Use float32 for CPU
        self.pipe.to("cpu")  # Use CPU

    def generate_redesigned_image(self, prompt, uploaded_image_path):
        # Open the uploaded image
        image = Image.open(uploaded_image_path).convert("RGB")

        # Generate the new design using the model
        new_image = self.pipe(prompt, image=image).images[0]
        
        # Save the generated image
        generated_image_path = "generated_design.png"
        new_image.save(generated_image_path)
        print(f"Generated Image saved at {generated_image_path}")
        
        return generated_image_path
