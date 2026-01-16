class OCRException(Exception):
    """Base exception for OCR operations"""
    pass


class ImageLoadError(OCRException):
    """Raised when image cannot be loaded"""
    pass


class APIError(OCRException):
    """Raised when API call fails"""
    pass


class ValidationError(OCRException):
    """Raised when input validation fails"""
    pass


class ConfigurationError(OCRException):
    """Raised when configuration is invalid"""
    pass


class JSONParseError(OCRException):
    """Raised when JSON parsing fails"""
    pass

