from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# load once (important for LangGraph performance)
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)


def visual_analysis_agent(state):
    """
    LangGraph node:
    input: state["image_path"], state["detailed"]
    output: {"description": "..."}
    """

    image_path = state["image_path"]
    detailed = state.get("detailed", False)

    image = Image.open(image_path).convert("RGB")

    # prompt strategy (BLIP uses text conditioning but still works like this)
    prompt = (
        "a very detailed description of the image"
        if detailed
        else "a short description of the image"
    )

    inputs = processor(images=image, text=prompt, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_length=120 if detailed else 60
        )

    description = processor.decode(output[0], skip_special_tokens=True)

    return {
        **state,
        "description": description
    }