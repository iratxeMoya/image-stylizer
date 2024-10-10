import torch
from PIL import Image
from torchvision import transforms

# Load pre-trained style transfer model (example using torchvision)
style_models = {
    "anime": torch.hub.load('pytorch/examples', 'fast_neural_style', model='rain_princess'),
    "pixar": torch.hub.load('pytorch/examples', 'fast_neural_style', model='mosaic'),
    # Add more models here
}

def apply_style(image_path: str, style: str):
    # Load image
    image = Image.open(image_path).convert("RGB")
    
    # Apply transformations (resize, normalize, etc.)
    transform = transforms.Compose([
        transforms.Resize((512, 512)),  # Ensure consistent size
        transforms.ToTensor(),
    ])
    
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension

    # Apply the style model
    model = style_models.get(style)
    if not model:
        raise ValueError(f"Style {style} is not supported.")
    
    with torch.no_grad():
        styled_image = model(image_tensor)  # Model inference
    
    # Save processed image
    processed_image = transforms.ToPILImage()(styled_image.squeeze())
    processed_image.save(f"processed/{image_path.split('/')[-1]}")  # Save in 'processed' directory