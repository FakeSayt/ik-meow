import discord
from discord.ext import commands
from discord import app_commands

from helpers import get_hero_info


class BestArtifact(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="bestartifact",
        description="Get the best artifact recommendation for a hero"
    )
    async def bestartifact(self, interaction: discord.Interaction, hero: str):
        hero_data = get_hero_info(hero)

        if not hero_data:
            await interaction.response.send_message(
                f"❌ Hero **{hero}** not found.",
                ephemeral=True
            )
            return

        name = hero_data["full"]
        price = hero_data["price"]

        await interaction.response.send_message(
            f"🏺 **Best Artifact for {name}**\n"
            f"💰 Cost Tier: {price}\n\n"
            f"✨ *Artifact recommendation logic goes here*"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(BestArtifact(bot))
