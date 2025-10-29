from app.models.agent import AgentState
from app.utils.logger import get_logger
from app.services.agent_graph import app

logger = get_logger(__name__)

def run_daily_post(niche: str):
    try:
        state = AgentState(
            niche=niche,
            topic=None,
            post_draft=None,
            final_post=None,
            image_asset_urn=None,
            is_approved=False,
            iteration_count=0,
        )

        logger.info("🚀 Starting workflow for niche: %s", niche)

        final_state = None
        for s in app.stream(state):
            node_name = list(s.keys())[0]
            logger.info("➡ Node executed: %s", node_name)
            final_state = s

        logger.info("🎯 Workflow finished. Final state: %s", final_state)

    except Exception as e:
        logger.exception("❌ Workflow execution failed: %s", e)

if __name__ == "__main__":
    run_daily_post("Artificial aIntelligence")



# import os
# import base64
# import requests
# from io import BytesIO
# from PIL import Image

# from google import genai
# from google.genai import errors as genai_errors
# from google.genai import types

# # API KEY
# GEMINI_API_KEY = "AIzaSyBY2KP33F8AUbcICOf_I3_U4wURABVJAPY"
# OUTPUT_FILE = "generated_image.png"
# MODEL = "gemini-2.5‑flash-image"   # image model as per docs :contentReference[oaicite:1]{index=1}

# # Initialize client
# try:
#     client = genai.Client(api_key=GEMINI_API_KEY)
#     print("✅ Gemini client initialized")
# except Exception as e:
#     print(f"❌ Failed to initialize Gemini client: {e}")
#     exit(1)

# # Prompt
# prompt = "A professional, high-resolution AI generated image of a serene ocean sunset with gentle waves"

# # Generate image via models.generate_content
# try:
#     response = client.models.generate_content(
#         model=MODEL,
#         contents=[prompt],
#         config=types.GenerateContentConfig(   # set response modalities to include image
#             response_modalities=[types.Modality.IMAGE]
#         )
#     )

#     image_bytes = None
#     for part in response.candidates[0].content.parts:
#         if hasattr(part, "inline_data") and part.inline_data:
#             image_bytes = part.inline_data.data
#             break

#     if not image_bytes:
#         print("⚠️ No image data returned")
#         exit(1)

#     image = Image.open(BytesIO(image_bytes))
#     image.save(OUTPUT_FILE)
#     print(f"✅ Image saved as {OUTPUT_FILE}")

# except genai_errors.APIError as e:
#     print(f"❌ Gemini API Error: {e}")
# except Exception as e:
#     print(f"❌ Unexpected error: {e}")
