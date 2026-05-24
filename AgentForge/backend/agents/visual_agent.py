from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


# MODELS INIT
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

model.eval()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


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


def _expand_with_llm(caption, detailed):

    # obični način rada → vrati kratki opis na hrvatskom
    if not detailed:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ti si pomoćnik za pristupačnost slijepim i slabovidnim osobama. "
                        "Tvoj zadatak je pretvoriti opis slike u prirodan i kratak opis na hrvatskom jeziku. "
                        "Uvijek odgovaraj ISKLJUČIVO na hrvatskom jeziku."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Prevedi i prirodno opiši ovu sliku na hrvatskom jeziku:\n\n{caption}\n\n"
                        "Napiši jednu kratku i jasnu rečenicu."
                    )
                }
            ],
            temperature=0.5
        )

        return response.choices[0].message.content


    # detailed način rada
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ti si pomoćnik za pristupačnost slijepim i slabovidnim osobama. "
                    "Tvoj zadatak je generirati detaljan i koristan opis slike na hrvatskom jeziku. "
                    "Opis mora biti prirodan, jasan i lako razumljiv osobi koja ne vidi sliku. "
                    "Uvijek odgovaraj ISKLJUČIVO na hrvatskom jeziku. "
                    "Uključi sljedeće ako je vidljivo na slici: "
                    "objekte, boje, raspored elemenata, položaje u prostoru, radnje, izraz ili atmosferu scene i kontekst."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Na temelju ovog opisa slike napravi detaljan opis na hrvatskom jeziku:\n\n{caption}\n\n"
                    "Objasni što se nalazi na slici tako da slijepa ili slabovidna osoba može što bolje razumjeti sadržaj. "
                    "Opis neka bude detaljan, ali prirodan i lako razumljiv."
                )
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


def visual_analysis_agent(state):

    image_path = state["image_path"]
    detailed = state.get("detailed", False)

    image = Image.open(image_path).convert("RGB")

    caption = _blip_caption(image, detailed=False)

    description = _expand_with_llm(caption, detailed)

    return {
        **state,
        "description": description
    }