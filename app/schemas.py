from pydantic import BaseModel
from enum import Enum

class StyleOptions(str, Enum):
    anime = "anime"
    pixar = "pixar"
    pixel_art = "pixel_art"
    vice = "vice"