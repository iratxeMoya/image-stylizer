from diffusers import StableDiffusionPipeline
import torch

class ModelLoader:
    """
    ModelLoader handles loading the appropriate pre-trained model based on the selected style.
    It abstracts the model loading process to keep the ImageStylizer class focused on image operations.
    """
    
    def __init__(self, style):
        """
        Initialize the ModelLoader with the selected style.

        :param style: Chosen artistic style (e.g., 'pixar', 'pixel_art', etc.)
        """
        self.style = style
    
    def load_model(self):
        """
        Load the pre-trained model for the selected style.

        :return: A Stable Diffusion model or any other appropriate model for the style
        """
        # Here we can dynamically load different models if needed for each style
        # Currently, we are using Stable Diffusion for all styles as an example
        try:
            print(f"Loading model for style: {self.style}")
            model = StableDiffusionPipeline.from_pretrained("hf-internal-testing/tiny-stable-diffusion-pipe").to("cuda")
            return model
        except Exception as e:
            raise Exception(f"Failed to load model: {e}")