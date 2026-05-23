from backend.tools.image_validator import validate_image
from backend.tools.hash_tool import generate_hash


def orchestrator_agent(state):

    path = state["image_path"]

    is_valid = validate_image(path)

    if not is_valid:
        return {
            "valid_image": False,
            "error": "Invalid image format."
        }

    image_hash = generate_hash(path)

    return {
        "valid_image": True,
        "image_hash": image_hash
    }