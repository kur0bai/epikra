import requests
from app.schemas.ai import ContentRequest
from app.core.config import settings

HUGGINGFACE_API_KEY = settings.HUGGINGFACE_API_KEY
HF_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}


def improve_text(data: ContentRequest):
    prompt = f"<s>[INST] You are a professional writting assistant, please improve this content: {data.content} [/INST]"
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json={"inputs": prompt}
    )

    result = response.json()
    if isinstance(result, list):
        generated_text = result[0]["generated_text"]
        cleaned_text = generated_text.split('[/INST]')[-1].strip()
    else:
        cleaned_text = "Something weng wrong improving the text"

    return {"improved_content": cleaned_text}
