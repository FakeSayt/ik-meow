import discord
from discord.ext import commands
from discord import app_commands
from ai_helper import fetch_hero_ai_data

class MeowWiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="meowwiki",
        description="Search Infinity Kingdom info and get a summarized guide"
    )
    @app_commands.describe(query="Event, hero, artifact or keyword in Infinity Kingdom")
    async def meowwiki(self, interaction: discord.Interaction, query: str):
        # Wywołaj AI dla całej gry
        ai_summary = await fetch_hero_ai_data(query)

        # Embed z tytułem i AI podsumowaniem
        embed = discord.Embed(
            title=f"Infinity Kingdom Info – {query.title()}",
            description=ai_summary,
            color=0x00ff00
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(MeowWiki(bot))
