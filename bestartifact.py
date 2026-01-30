import discord
from discord import app_commands
from helpers import get_hero_info

class BestArtifact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="bestartifact",
        description="Get best artifact rolls for an Immortal"
    )
    async def bestartifact(self, interaction: discord.Interaction, immortal: str):
        hero = get_hero_info(immortal)

        if not hero:
            await interaction.response.send_message(
                f"❓ Immortal **{immortal}** not found in database.\n"
                f"I will use AI to estimate best artifacts (soon).",
                ephemeral=True
            )
            return

        artifacts = hero.get("artifacts", "No artifact data.")
        await interaction.response.send_message(
            f"🧩 **Best artifacts for {hero['name']}**\n{artifacts}"
        )

async def setup(bot):
    await bot.add_cog(BestArtifact(bot))
