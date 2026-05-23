from typing import TypedDict, Optional, List, Dict, Any


class AgentState(TypedDict):
    image_path: str
    session_id: str

    image_hash: Optional[str]

    user_prompt: str
    detailed: bool

    description: Optional[str]
    audio_path: Optional[str]

    history: List[Dict[str, Any]]

    valid_image: Optional[bool]
    error: Optional[str]