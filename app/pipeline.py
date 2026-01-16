import json
from typing import Dict, Any
from app.ocr.gemini_client import GeminiOCRClient
from app.processors.image_loader import load_image
from app.utils.file_utils import read_file
from app.exceptions import JSONParseError, OCRException


_PROMPT_CACHE: Dict[str, str] = {}


def _get_cached_prompt(path: str) -> str:
    """Get prompt from cache or load from file"""
    if path not in _PROMPT_CACHE:
        _PROMPT_CACHE[path] = read_file(path)
    return _PROMPT_CACHE[path]


def run_pipeline(image_path: str) -> Dict[str, Any]:
    """Run OCR pipeline on image and return extracted data"""
    try:
        image = load_image(image_path)
        system_prompt = _get_cached_prompt("app/prompts/system.txt")
        user_prompt = _get_cached_prompt("app/prompts/extraction.txt")

        ocr_client = GeminiOCRClient()
        response = ocr_client.extract(image, system_prompt, user_prompt)

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            raise JSONParseError(f"Failed to parse JSON response: {str(e)}") from e

        if response.usage_metadata:
            data["usage_metadata"] = {
                "input_tokens": response.usage_metadata.prompt_token_count,
                "output_tokens": response.usage_metadata.candidates_token_count,
                "note": "Populated from Gemini API"
            }

        return data
    except OCRException:
        raise
    except Exception as e:
        raise OCRException(f"Pipeline execution failed: {str(e)}") from e
