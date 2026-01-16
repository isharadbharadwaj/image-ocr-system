import os
from pathlib import Path
from PIL import Image
from typing import Tuple
from app.exceptions import ValidationError, ImageLoadError


def validate_image_path(image_path: str) -> str:
    """Validate image path exists and is readable"""
    if not image_path:
        raise ValidationError("Image path cannot be empty")
    
    path = Path(image_path)
    if not path.exists():
        raise ValidationError(f"Image path does not exist: {image_path}")
    
    if not path.is_file():
        raise ValidationError(f"Image path is not a file: {image_path}")
    
    if not os.access(path, os.R_OK):
        raise ValidationError(f"Image file is not readable: {image_path}")
    
    return str(path)


def validate_image_format(image: Image.Image) -> None:
    """Validate image format and basic properties"""
    if image.format is None:
        raise ImageLoadError("Image format could not be determined")
    
    if image.size[0] == 0 or image.size[1] == 0:
        raise ImageLoadError("Image has invalid dimensions")


def get_image_info(image: Image.Image) -> Tuple[int, int, str]:
    """Get image dimensions and format"""
    return image.size[0], image.size[1], image.format or "Unknown"

