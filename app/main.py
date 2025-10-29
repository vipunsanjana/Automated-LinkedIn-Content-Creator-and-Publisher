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
    run_daily_post("Artificial Intelligence")
