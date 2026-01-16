from dotenv import load_dotenv
import os
from typing import Optional
from app.exceptions import ConfigurationError

_load_dotenv_called = False


def _ensure_env_loaded():
    global _load_dotenv_called
    if not _load_dotenv_called:
        load_dotenv()
        _load_dotenv_called = True


class Settings:
    _api_key: Optional[str] = None
    _model_id: Optional[str] = None
    _temperature: Optional[float] = None
    _top_p: Optional[float] = None

    @classmethod
    def _get_api_key(cls) -> str:
        _ensure_env_loaded()
        if cls._api_key is None:
            cls._api_key = os.getenv("GEMINI_API_KEY")
            if not cls._api_key:
                raise ConfigurationError("GEMINI_API_KEY environment variable is not set")
        return cls._api_key

    @classmethod
    def _get_model_id(cls) -> str:
        _ensure_env_loaded()
        if cls._model_id is None:
            cls._model_id = os.getenv("GEMINI_MODEL")
            if not cls._model_id:
                raise ConfigurationError("GEMINI_MODEL environment variable is not set")
        return cls._model_id

    @classmethod
    def _get_temperature(cls) -> float:
        _ensure_env_loaded()
        if cls._temperature is None:
            cls._temperature = float(os.getenv("TEMPERATURE", "0.0"))
        return cls._temperature

    @classmethod
    def _get_top_p(cls) -> float:
        _ensure_env_loaded()
        if cls._top_p is None:
            cls._top_p = float(os.getenv("TOP_P", "0.1"))
        return cls._top_p

    @classmethod
    def get_api_key(cls) -> str:
        return cls._get_api_key()

    @classmethod
    def get_model_id(cls) -> str:
        return cls._get_model_id()

    @classmethod
    def get_temperature(cls) -> float:
        return cls._get_temperature()

    @classmethod
    def get_top_p(cls) -> float:
        return cls._get_top_p()
