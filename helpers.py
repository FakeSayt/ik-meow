from heroes import HERO_INFO, HERO_PRICE
from mage_stats import MAGE_STATS
from ai_helper import fetch_immortal_info

# Sprawdza, czy Immortal istnieje w naszej bazie, jeśli nie używa AI
def get_hero_info(name: str):
    key = name.lower()
    
    hero = HERO_INFO.get(key)
    price = HERO_PRICE.get(key)
    mage_stats = MAGE_STATS.get(key)

    # Jeśli nie znaleziono, użyj AI do pobrania danych
    if not hero or not price or not mage_stats:
        ai_data = fetch_immortal_info(name)
        # Możesz tutaj od razu uzupełnić nasze słowniki
        if ai_data:
            HERO_INFO[key] = ai_data.get("hero_info", {"full": name, "short": name[:4]})
            HERO_PRICE[key] = ai_data.get("price", "Unknown")
            MAGE_STATS[key] = ai_data.get("mage_stats", {})
        hero = HERO_INFO[key]
        price = HERO_PRICE[key]
        mage_stats = MAGE_STATS[key]
    
    return {
        "hero": hero,
        "price": price,
        "mage_stats": mage_stats
    }
