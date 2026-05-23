from graph.workflow import workflow


def run_agentforge(image_path):

    state = {
        "image_path": image_path,
        "user_prompt": "Describe image",
        "detailed": False,
        "description": "",
        "audio_path": "",
        "history": [],
        "valid_image": False,
        "error": None,
    }

    result = workflow.invoke(state)

    return result