from discord.ext import commands
from discord import app_commands
from mage_stats import MAGE_STATS
from helpers import get_hero_info
from ai_helper import fetch_hero_ai_data

class Damage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="damage", description="Compare ultimate damage between two heroes")
    @app_commands.describe(hero1="First hero", hero2="Second hero")
    async def damage(self, interaction: discord.Interaction, hero1: str, hero2: str):
        h1 = hero1.lower()
        h2 = hero2.lower()

        h1_data = MAGE_STATS.get(h1)
        h2_data = MAGE_STATS.get(h2)

        # Fallback AI if hero missing
        if not h1_data:
            h1_data = {"dps": "Unknown", "special": await fetch_hero_ai_data(hero1)}
        if not h2_data:
            h2_data = {"dps": "Unknown", "special": await fetch_hero_ai_data(hero2)}

        response = (
            f"**Damage comparison:**\n"
            f"{hero1.title()} DPS: {h1_data.get('dps')} | Special: {h1_data.get('special')}\n"
            f"{hero2.title()} DPS: {h2_data.get('dps')} | Special: {h2_data.get('special')}\n"
        )

        if isinstance(h1_data.get("dps"), (int, float)) and isinstance(h2_data.get("dps"), (int, float)):
            if h1_data["dps"] > h2_data["dps"]:
                response += f"🔥 {hero1.title()} has higher DPS!"
            elif h1_data["dps"] < h2_data["dps"]:
                response += f"🔥 {hero2.title()} has higher DPS!"
            else:
                response += "⚖️ Both heroes have equal DPS!"
        await interaction.response.send_message(response)

async def setup(bot):
    await bot.add_cog(Damage(bot))
