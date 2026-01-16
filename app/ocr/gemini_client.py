from google import genai
from google.genai import types
from PIL import Image
from typing import Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.config.settings import Settings
from app.ocr.base import OCRClient
from app.exceptions import APIError, ConfigurationError


class GeminiOCRClient(OCRClient):
    """Gemini API implementation of OCR client with retry logic"""

    _instance: Optional['GeminiOCRClient'] = None
    _client: Optional[Any] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is not None:
            return
        
        try:
            self._client = genai.Client(api_key=Settings.get_api_key())
        except ConfigurationError as e:
            raise ConfigurationError(f"Failed to initialize Gemini client: {str(e)}") from e
        except Exception as e:
            raise APIError(f"Failed to create Gemini client: {str(e)}") from e

    @property
    def client(self):
        if self._client is None:
            raise APIError("Client not initialized")
        return self._client

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(APIError),
        reraise=True
    )
    def extract(self, image: Image.Image, system_prompt: str, user_prompt: str) -> Any:
        """Extract data from image using Gemini API with retry logic"""
        try:
            config = types.GenerateContentConfig(
                temperature=Settings.get_temperature(),
                top_p=Settings.get_top_p(),
                response_mime_type="application/json",
                system_instruction=system_prompt,
            )

            response = self.client.models.generate_content(
                model=Settings.get_model_id(),
                contents=[image, user_prompt],
                config=config
            )

            if not response:
                raise APIError("Empty response from Gemini API")

            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                block_reason = getattr(response.prompt_feedback, 'block_reason', None)
                if block_reason:
                    raise APIError(f"Content blocked by safety filters: {block_reason}")

            if not response.text:
                raise APIError("Empty response text from Gemini API")

            return response
        except APIError:
            raise
        except Exception as e:
            raise APIError(f"Gemini API call failed: {str(e)}") from e
