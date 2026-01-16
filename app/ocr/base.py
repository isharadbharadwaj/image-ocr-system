from abc import ABC, abstractmethod
from PIL import Image
from typing import Any


class OCRClient(ABC):
    """Base class for OCR client implementations"""

    @abstractmethod
    def extract(self, image: Image.Image, system_prompt: str, user_prompt: str) -> Any:
        """Extract text/data from image using provided prompts"""
        pass
