import os
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def fetch_hero_ai_data(hero_name: str) -> str:
    if not OPENAI_API_KEY:
        return "AI data unavailable (no API key)"
    
    prompt = f"Provide a short description and meta about artifact info for the Infinity Kingdom hero '{hero_name}'."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error fetching AI data: {e}"
