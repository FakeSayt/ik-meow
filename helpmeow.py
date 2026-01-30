import discord
from discord import app_commands
from discord.ext import commands

class HelpMeow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="helpmeow", description="Show all available commands and usage")
    async def helpmeow(self, interaction: discord.Interaction):
        msg = (
            "**Available Commands:**\n"
            "/bestartifact [hero_name] – Show best artifact rolls for an Immortal\n"
            "/damage [hero1] [hero2] – Compare ultimate damage of two Immortals\n"
            "/helpmeow – Show this help message"
        )
        await interaction.response.send_message(msg)

async def setup(bot):
    await bot.add_cog(HelpMeow(bot))
