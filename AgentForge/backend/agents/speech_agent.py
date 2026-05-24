import os
import asyncio
import edge_tts


async def _tts(text, path):
    communicate = edge_tts.Communicate(
        text=text,
        voice="hr-HR-GabrijelaNeural"
    )
    await communicate.save(path)


def speech_agent(state):

    session_id = state["session_id"]
    text = state["description"]

    output_dir = f"data/{session_id}"
    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(output_dir, "output.mp3")

    asyncio.run(_tts(text, audio_path))

    return {
        **state,
        "audio_path": audio_path
    }