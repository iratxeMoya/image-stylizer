from PIL import Image
import torch
from src.model_loader import ModelLoader

class ImageStylizer:
    """
    ImageStylizer is responsible for applying the selected artistic style to the input image.
    """
    
    def __init__(self, input_image: Image.Image, style: str):
        """
        Initialize the ImageStylizer with the image and chosen style.

        :param input_image: PIL Image object of the input image
        :param style: Chosen artistic style
        """
        self.input_image = input_image
        self.style = style
        self.model_loader = ModelLoader(style)  # Initialize ModelLoader with the selected style

    def apply_style(self) -> Image.Image:
        """
        Apply the selected style to the input image using the appropriate model.

        :return: PIL Image object of the stylized image
        """
        # Load the pre-trained model using the ModelLoader class
        model = self.model_loader.load_model()

        # Generate the style prompt based on the selected style
        prompt = self._generate_prompt()

        # Apply the style using the model (e.g., Stable Diffusion)
        with torch.autocast("cuda"):
            stylized_image = model(prompt, init_image=self.input_image, strength=0.75).images[0]

        return stylized_image
    
    def _generate_prompt(self) -> str:
        """
        Generate the style-specific text prompt to guide the model in generating the stylized image.

        :return: A string containing the style prompt
        """
        style_prompts = {
            "pixar": "Pixar style illustration of ",
            "pixel_art": "Pixel art of ",
            "vice": "80s retro vice style art of ",
            "anime": "Anime art of "
        }
        
        # Example content: A landscape. This can be customized as needed.
        content = "a beautiful landscape"
        
        return style_prompts.get(self.style, "") + content