from backend.tools.image_validator import validate_image
from backend.tools.hash_tool import generate_hash
from backend.memory.session_memory import SessionMemory


memory_store = SessionMemory()


def orchestrator_agent(state):

    path = state["image_path"]
    session_id = state["session_id"]

    memory = memory_store.get(session_id)

    # validate
    is_valid = validate_image(path)
    if not is_valid:
        return {
            **state,
            "valid_image": False,
            "error": "Invalid image"
        }

    # hash
    image_hash = generate_hash(path)

    state["image_hash"] = image_hash

    if image_hash in memory["cache"]:
        cached = memory["cache"][image_hash]

        return {
            **state,
            "valid_image": True,
            **cached,
            "description": cached["description"],
            "audio_path": cached["audio_path"]
        }

    return {
        **state,
        "valid_image": True
    }