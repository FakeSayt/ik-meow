from discord.ext import commands
from discord import app_commands

class HelpMeow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="helpmeow", description="Shows all available bot commands")
    async def helpmeow(self, interaction: discord.Interaction):
        response = (
            "**Available Commands:**\n"
            "/helpmeow - Show this help message\n"
            "/bestartifact <hero> - Shows recommended artifact for a hero\n"
            "/damage <hero1> <hero2> - Compares ultimate damage between two heroes"
        )
        await interaction.response.send_message(response)

async def setup(bot):
    await bot.add_cog(HelpMeow(bot))
