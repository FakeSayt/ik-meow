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
        query_lower = query.lower()

        # Spróbuj dopasować do lokalnych artefaktów
        artifact_info = await self.get_artifact_summary(query_lower)

        # Tworzymy embed
        embed = discord.Embed(title=f"Infinity Kingdom Info – {query.title()}", color=0x00ff00)

        if artifact_info:
            embed.description = artifact_info
        else:
            ai_summary = await fetch_hero_ai_data(query)
            embed.description = ai_summary

        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def get_artifact_summary(self, keyword: str) -> str:
        summaries = {
            "mage": "Mage builds focus on magical damage. Use Crit for high DPS chase builds, Nonchase for stable pure damage.",
            "attack": "Attack builds focus on physical damage. Ultimate-based builds rely on energy regen (Surge), Physical builds focus on accuracy.",
            "crit": "Mage – Crit (Chase) Build:\nPriority Rolls: Crit Rate → Magical Attack → Crit Damage → Magical → Defenses\nBest for VIP 13+",
            "nonchase": "Mage – Non-Chase Build:\nPriority Rolls: Magical Attack → Magical Attack Value → Crit Rate → Crit Damage → Defenses\nFocus on pure damage.",
            "ultimate": "Attack – Ultimate Ability Based DPS:\nTop Priority: Physical Attack → Iron Fist → Magical Defense → Accuracy → Physical Defense\nSurge mandatory.",
            "physical": "Attack – Physical Damage Dealer:\nTop Priority: Physical Attack → Rapid (Alex/Hannibal) → Accuracy → Physical Defense → Crit\nAccuracy mandatory."
        }
        return summaries.get(keyword)

async def setup(bot):
    await bot.add_cog(MeowWiki(bot))
