from PIL import Image
from typing import Optional
from app.exceptions import ImageLoadError
from app.utils.validation import validate_image_path, validate_image_format


def load_image(path: str) -> Image.Image:
    """Load and validate image from file path"""
    try:
        validated_path = validate_image_path(path)
        image = Image.open(validated_path)
        image.load()
        validate_image_format(image)
        return image
    except (OSError, IOError, Image.UnidentifiedImageError) as e:
        raise ImageLoadError(f"Failed to load image from {path}: {str(e)}") from e
