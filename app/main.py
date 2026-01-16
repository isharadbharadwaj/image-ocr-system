import json
import sys
from app.pipeline import run_pipeline
from app.exceptions import OCRException


def main():
    """Main entry point for OCR pipeline"""
    
    image_path = "images/sample.webp"
    print(f"Processing image: {image_path}")
    
    try:
        result = run_pipeline(image_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except OCRException as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
