import os
import asyncio
import edge_tts
from dotenv import load_dotenv

load_dotenv()


async def _generate_speech(text, output_path):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-JennyNeural"
    )
    await communicate.save(output_path)


def speech_agent(state):
    text = state["description"]
    audio_path = "outputs/output.mp3"

    # ensure folder exists
    os.makedirs("outputs", exist_ok=True)

    # run async TTS
    asyncio.run(_generate_speech(text, audio_path))

    return {"audio_path": audio_path}
