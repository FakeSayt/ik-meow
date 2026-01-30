import discord
from discord.ext import commands
from discord import app_commands
from helpers import get_hero_info

class BestArtifact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bestartifact", description="Shows the best artifact for a given hero")
    @app_commands.describe(hero="The hero name")
    async def bestartifact(self, interaction: discord.Interaction, hero: str):
        info = get_hero_info(hero)
        response = (
            f"**{info['full_name']} ({info['short_name']})**\n"
            f"Recommended artifact info: 🛡️ Best artifact setup for {info['full_name']}\n"
            f"Cost/rarity: {info['price']}"
        )
        await interaction.response.send_message(response)

async def setup(bot):
    await bot.add_cog(BestArtifact(bot))
