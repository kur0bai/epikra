import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY
client = openai.Client()


def generate_suggestion(content: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional writing assistant."},
            {"role": "user", "content": f"Improve this content: {content}"}
        ],
        temperature=0.7,
        max_tokens=512
    )
    return {"improved_content": response.choices[0].message.content.strip()}
