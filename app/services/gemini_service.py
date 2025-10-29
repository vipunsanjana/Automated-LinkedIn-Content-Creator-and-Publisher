from typing import Optional
from io import BytesIO
from PIL import Image
import os
from google import genai
from google.genai import errors as genai_errors
from langchain.tools import tool

from app.utils.config import GEMINI_API_KEY
from app.utils.logger import get_logger
from app.utils.constants import (
    GEMINI_CLIENT_INIT_FAIL,
    GEMINI_IMAGE_GEN_FAIL,
    GEMINI_NO_IMAGE_DATA,
    GEMINI_IMAGE_SAVE_FAIL,
    TEMP_FILE_REMOVED,
    GEMINI_MODEL,
    GEMINI_IMAGE_PROMPT_TEMPLATE,
)

logger = get_logger(__name__)

def get_gemini_client() -> Optional[genai.Client]:
    """Safely initialize and return a Gemini client instance."""
    if not GEMINI_API_KEY:
        logger.error("❌ Missing GEMINI_API_KEY in environment. Cannot initialize Gemini client.")
        return None
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info("✅ Gemini client initialized successfully.")
        return client
    except Exception as e:
        logger.error(GEMINI_CLIENT_INIT_FAIL.format(error=e))
        return None

@tool("generate_gemini_image")
def generate_gemini_image(prompt: str, temp_path: str = "temp_gemini_image.png") -> Optional[bytes]:
    """
    Generate a professional AI image for a LinkedIn post using Gemini API.

    Args:
        prompt (str): The topic or description for the image.
        temp_path (str, optional): Temporary file path to save the image. Defaults to "temp_gemini_image.png".

    Returns:
        Optional[bytes]: The image data in bytes, or None if generation failed.
    """
    gemini_client = get_gemini_client()
    if not gemini_client:
        return None

    full_prompt = GEMINI_IMAGE_PROMPT_TEMPLATE.format(topic=prompt)
    logger.info(f"🎨 Generating Gemini image for prompt: '{prompt}'")

    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[full_prompt],
        )

        image_bytes: Optional[bytes] = None
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    image_bytes = part.inline_data.data
                    break

        if not image_bytes:
            logger.warning(GEMINI_NO_IMAGE_DATA)
            return None

        try:
            image = Image.open(BytesIO(image_bytes))
            image.save(temp_path)
            logger.info(f"✅ Gemini image saved temporarily at {temp_path}")
        except Exception as e:
            logger.error(GEMINI_IMAGE_SAVE_FAIL.format(error=e))
            return None

        return image_bytes

    except genai_errors.APIError as e:
        logger.error(GEMINI_IMAGE_GEN_FAIL.format(error=e))
        return None
    except Exception as e:
        logger.error(GEMINI_IMAGE_GEN_FAIL.format(error=e))
        return None
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            logger.info(TEMP_FILE_REMOVED)
