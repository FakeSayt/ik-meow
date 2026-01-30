from heroes import HERO_INFO, HERO_PRICE
from mage_stats import MAGE_STATS


def normalize(name: str) -> str:
    return name.strip().lower()


def get_hero(hero_name: str):
    key = normalize(hero_name)

    if key not in HERO_INFO:
        return None

    return {
        "info": HERO_INFO[key],
        "price": HERO_PRICE.get(key, "Unknown"),
        "mage": MAGE_STATS.get(key)
    }
