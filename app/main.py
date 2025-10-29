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


# from PIL import Image
# import logging
# import os

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)

# def generate_dummy_image_keep_file() -> str:
#     """
#     Generate a dummy 512x512 RGB image and keep it saved on disk.
#     Returns the file path.
#     """
#     temp_path = "dummy_image.png"  # Hardcoded path
#     image = Image.new("RGB", (512, 512), color=(73, 109, 137))
#     image.save(temp_path)
#     logger.info(f"✅ Dummy image saved at {temp_path}")
#     return temp_path

# # Example usage
# if __name__ == "__main__":
#     file_path = generate_dummy_image_keep_file()
#     print(f"Image saved at: {file_path}")

#     # Open the image to view
#     img = Image.open(file_path)
#     img.show()
