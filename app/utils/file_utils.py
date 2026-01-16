from pathlib import Path
from typing import Optional
from app.exceptions import ValidationError


def read_file(path: str) -> str:
    """Read file content with validation"""
    file_path = Path(path)
    if not file_path.exists():
        raise ValidationError(f"File does not exist: {path}")
    if not file_path.is_file():
        raise ValidationError(f"Path is not a file: {path}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, IOError, UnicodeDecodeError) as e:
        raise ValidationError(f"Failed to read file {path}: {str(e)}") from e
