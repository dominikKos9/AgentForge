from typing import TypedDict, Optional, List


class AgentState(TypedDict):
    image_path: str
    image_hash: str

    user_prompt: str
    detailed: bool

    description: str
    audio_path: str

    history: List[str]

    valid_image: bool
    error: Optional[str]