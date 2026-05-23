from backend.graph.workflow import workflow
from dotenv import load_dotenv
load_dotenv()


def run_agentforge(image_path, session_id="default", detailed=False):

    state = {
        "image_path": image_path,
        "session_id": session_id,

        "detailed": detailed,   

        "user_prompt": "Describe image",

        "description": "",
        "audio_path": "",

        "history": [],
        "valid_image": None,
        "error": None
    }

    return workflow.invoke(state)