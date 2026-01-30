from heroes import HERO_INFO

def normalize_name(name: str) -> str:
    return name.strip().lower()

def get_hero(hero_name: str) -> dict | None:
    """
    Returns hero info from HERO_INFO.
    If hero does not exist, returns None (AI can handle later).
    """
    key = normalize_name(hero_name)
    return HERO_INFO.get(key)

# 🔹 ALIAS – żeby stare importy NIE WYKRZACZAŁY BOTA
get_hero_info = get_hero
