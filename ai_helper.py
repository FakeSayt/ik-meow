import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def fetch_immortal_info(name: str):
    """
    Funkcja używa OpenAI, żeby pobrać informacje o brakującym Immortalu
    Zwraca słownik w formacie zgodnym z HERO_INFO, HERO_PRICE, MAGE_STATS
    """
    prompt = f"""
    You are a knowledgeable Infinity Kingdom assistant.
    Give me full hero info for '{name}':
    - full name
    - short name (4-5 chars)
    - price tier
    - mage ultimate stats (element, single_target, four_target, energy_regen, skill_per_sec, dps, special)
    Respond in JSON format with keys: hero_info, price, mage_stats
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        content = response.choices[0].message.content
        # Spróbuj sparsować JSON
        import json
        return json.loads(content)
    except Exception as e:
        print(f"AI fetch failed for {name}: {e}")
        return None
