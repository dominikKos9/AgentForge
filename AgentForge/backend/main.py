from backend.graph.workflow import workflow


def run_agentforge(image_path):
    state = {
        "image_path": image_path,
        "user_prompt": "Describe image",
        "detailed": False,
        "description": "",
        "audio_path": "",
        "history": [],
        "valid_image": None,   
        "error": None,
    }

    try:
        result = workflow.invoke(state)

        # optional safety fallback
        if result.get("valid_image") is False:
            return {
                "error": result.get("error", "Invalid image"),
                "valid_image": False
            }

        return result

    except Exception as e:
        return {
            "valid_image": False,
            "error": str(e)
        }