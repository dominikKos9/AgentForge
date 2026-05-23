from openai import OpenAI

client = OpenAI()


def speech_agent(state):

    text = state["description"]

    audio_path = "outputs/output.mp3"

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    response.stream_to_file(audio_path)

    return {"audio_path": audio_path}