from openai import OpenAI

client = OpenAI()


def visual_analysis_agent(state):

    image_path = state["image_path"]

    detailed = state["detailed"]

    prompt = (
        "Describe this image for a blind person."
        if not detailed
        else
        "Describe this image in high detail for a blind person."
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"file://{image_path}"
                        }
                    },
                ],
            }
        ]
    )

    description = response.choices[0].message.content

    return {"description": description}