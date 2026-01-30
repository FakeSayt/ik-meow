import discord
from discord import app_commands
from discord.ext import commands
from mage_stats import MAGE_STATS
from helpers import get_hero_info
from ai_helper import fetch_hero_ai_data

class Damage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="damage", description="Compare ultimate damage between two Immortals")
    async def damage(self, interaction: discord.Interaction, hero1_name: str, hero2_name: str):
        # Pobierz dane lokalnie
        hero1_data = get_hero_info(hero1_name)
        hero2_data = get_hero_info(hero2_name)

        # Jeśli nie ma w bazie – użyj AI
        if hero1_data is None:
            hero1_data = {"hero": {"full": hero1_name, "short": hero1_name}, "mage_stats": await fetch_hero_ai_data(hero1_name)}
        if hero2_data is None:
            hero2_data = {"hero": {"full": hero2_name, "short": hero2_name}, "mage_stats": await fetch_hero_ai_data(hero2_name)}

        h1_stats = hero1_data.get("mage_stats")
        h2_stats = hero2_data.get("mage_stats")

        # Porównanie DPS
        h1_dps = h1_stats.get("dps", 0) if h1_stats else 0
        h2_dps = h2_stats.get("dps", 0) if h2_stats else 0

        if h1_dps > h2_dps:
            winner = hero1_data["hero"]["full"]
        elif h2_dps > h1_dps:
            winner = hero2_data["hero"]["full"]
        else:
            winner = "Tie"

        await interaction.response.send_message(
            f"**{hero1_data['hero']['full']}** DPS: {h1_dps}\n"
            f"**{hero2_data['hero']['full']}** DPS: {h2_dps}\n"
            f"Better Ultimate: {winner}"
        )

async def setup(bot):
    await bot.add_cog(Damage(bot))
