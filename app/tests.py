import torch
from diffusers import StableDiffusionXLImg2ImgPipeline
from diffusers.utils import load_image
from PIL import Image

pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
)
pipe = pipe.to('cuda')
url = "https://huggingface.co/datasets/patrickvonplaten/images/resolve/main/aa_xl/000000009.png"

init_image = Image.open('data/input_image.jpg').convert("RGB")
prompt = "generate the image with an anime style"
image = pipe(prompt, image=init_image).images
image.save('data/res.png')