from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


# -----------------------
# MODELS INIT (load once)
# -----------------------
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

model.eval()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------
# STEP 1: BLIP CAPTION
# -----------------------
def _blip_caption(image, detailed=False):

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_length=120 if detailed else 60,
            num_beams=5 if detailed else 3,
            temperature=1.0,
            repetition_penalty=1.2
        )

    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption


# -----------------------
# STEP 2: GROQ REFINEMENT
# -----------------------
def _expand_with_llm(caption, detailed):

    if not detailed:
        return caption

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an accessibility assistant for blind users. "
                    "Expand image descriptions into detailed, clear, and helpful explanations. "
                    "Include objects, colors, spatial relations, and context."
                )
            },
            {
                "role": "user",
                "content": f"Describe this image in detail based on this caption:\n\n{caption}"
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


# -----------------------
# MAIN AGENT (LangGraph NODE)
# -----------------------
def visual_analysis_agent(state):

    image_path = state["image_path"]
    detailed = state.get("detailed", False)

    image = Image.open(image_path).convert("RGB")

    # STEP 1
    caption = _blip_caption(image, detailed=False)

    # STEP 2 (upgrade if needed)
    description = _expand_with_llm(caption, detailed)

    return {
        **state,
        "description": description
    }