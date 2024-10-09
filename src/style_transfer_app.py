from src.image_stylizer import ImageStylizer
from PIL import Image

class StyleTransferApp:
    """
    StyleTransferApp handles the flow of the style transfer process, 
    including applying the selected style to the uploaded image.
    """
    
    def __init__(self, input_image: Image.Image, style: str):
        """
        Initialize the application with the input image and style choice.

        :param input_image: PIL Image object of the input image
        :param style: Selected style for the transfer ('pixar', 'pixel_art', 'vice', 'anime')
        """
        self.input_image = input_image
        self.style = style

    def run(self) -> Image.Image:
        """
        Apply the style to the input image and return the result.

        :return: PIL Image object of the stylized image
        """
        try:
            stylizer = ImageStylizer(self.input_image, self.style)
            stylized_image = stylizer.apply_style()
            return stylized_image
        except Exception as e:
            raise Exception(f"Error applying style: {e}")