from heroes import HERO_INFO, HERO_PRICE

def get_hero_info(hero_name: str):
    key = hero_name.lower()
    if key in HERO_INFO:
        hero = HERO_INFO[key]
        price = HERO_PRICE.get(key, "Unknown")
        return {
            "full_name": hero["full"],
            "short_name": hero["short"],
            "price": price
        }
    else:
        return {
            "full_name": hero_name,
            "short_name": hero_name[:4],
            "price": "Unknown"
        }
