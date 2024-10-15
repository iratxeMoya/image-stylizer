import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
import PIL

def apply_style(image_path: str, style: str):
    model_id = "timbrooks/instruct-pix2pix"
    
    # Load model with float16 precision
    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
    pipe.to("cuda")
    
    # Use Euler Ancestral Discrete Scheduler
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    
    # Load and preprocess image
    image = PIL.Image.open(image_path)
    image = PIL.ImageOps.exif_transpose(image)
    image = image.convert("RGB")
    
    # Optimize GPU usage using autocast (mixed precision)
    if style == 'anime':
        prompt = "Transform the image into an anime style, with sharp and expressive lines, vibrant colors, and exaggerated facial expressions. Use smooth shading and highlight key features like large, detailed eyes and dynamic hair movement. Keep the background simplified, with subtle gradients and minimal textures to emphasize the character's emotions and action."
    elif style == 'pixar':
        prompt = "Restyle the image in the Pixar animation style, focusing on 3D-rendered characters with soft, rounded features and expressive facial details. Use vibrant colors, realistic lighting, and smooth textures. Preserve the warmth and family-friendly feel typical of Pixar, with exaggerated but lifelike proportions. Add a glossy, polished finish to all elements."
    elif style=='watercolor':
        prompt = "Restyle the image using a watercolor technique, with soft, flowing brushstrokes and gentle blending of colors. Incorporate light, translucent washes that allow the colors to bleed into one another. Emphasize a delicate and airy feel, using muted tones and splashes of vivid color for contrast. Maintain key details, but give the overall composition a loose, hand-painted appearance."
    elif style=='oleo':
        prompt = "Transform the image into an oil painting (oleo) style, with rich, thick brushstrokes and a bold use of color. Capture texture through visible layers of paint, giving the image depth and a sense of realism. Focus on dramatic lighting and shadow to create a more classic, fine art feel, similar to traditional oil portraits or landscapes. Preserve key details but enhance them with texture and movement in the brushwork."
    elif style=='pixel art':
        prompt = "Restyle the image into pixel art, with low-resolution, blocky graphics and a limited color palette. Break down the image into simple, grid-like patterns, focusing on bold, clear shapes and easily distinguishable features. Use pixel-sized detailing for intricate parts, and ensure that the overall composition feels nostalgic and retro, like classic video game art."
    
    with torch.cuda.amp.autocast():
        images = pipe(prompt, image=image, num_inference_steps=15, image_guidance_scale=0.8).images

    # Save output image
    images[0].save(f"processed/{image_path.split('/')[-1]}")