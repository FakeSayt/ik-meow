from helpers import get_hero_info

async def get_best_artifact(ctx, hero_name: str):
    # Pobierz info o bohaterze (z naszej bazy lub AI)
    data = get_hero_info(hero_name)
    
    hero = data["hero"]
    price = data["price"]
    mage_stats = data["mage_stats"]

    # Tutaj logika wyboru najlepszych artefaktów w oparciu o rolę/mage stats
    if mage_stats:
        # Mage build
        best_rolls = "Primary: Crit Rate %, Bonus: Annihilation"
    else:
        # Jeśli nie mage lub brak danych, możemy użyć AI do uzupełnienia builda
        best_rolls = "Unknown – data fetched via AI"

    # Wyślij odpowiedź
    await ctx.send(f"Best Artifact for **{hero['full']} ({hero['short']})**\nPrice Tier: {price}\nRecommended Rolls: {best_rolls}")
