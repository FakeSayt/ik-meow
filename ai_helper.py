import os
import openai
from config import OPENAI_API_KEY
import asyncio

openai.api_key = OPENAI_API_KEY

# Prosty cache w pamięci: {query_lower: result}
AI_CACHE = {}

async def fetch_hero_ai_data(hero_name: str) -> str:
    query_lower = hero_name.lower()

    # Sprawdź cache
    if query_lower in AI_CACHE:
        return AI_CACHE[query_lower]

    if not OPENAI_API_KEY:
        return "AI data unavailable (no API key)"

    prompt = f"Provide a short summary and key meta information for the Infinity Kingdom hero, artifact, or event '{hero_name}'. Focus on what players should know."

    try:
        # Wykorzystanie OpenAI
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        ))

        result = response.choices[0].message.content.strip()
        # Zapis do cache
        AI_CACHE[query_lower] = result
        return result

    except Exception as e:
        return f"Error fetching AI data: {e}"
