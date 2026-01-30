import discord
from discord.ext import commands
from discord import app_commands

ROLES = ["mage", "attack"]
BUILDS = {
    "mage": ["crit", "nonchase"],
    "attack": ["ultimate", "physical"]
}

class BestArtifact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def role_autocomplete(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=r, value=r) for r in ROLES if current.lower() in r.lower()]

    async def build_autocomplete(self, interaction: discord.Interaction, current: str):
        role = interaction.namespace.role.lower() if hasattr(interaction.namespace, "role") else ""
        options = BUILDS.get(role, [])
        return [app_commands.Choice(name=b, value=b) for b in options if current.lower() in b.lower()]

    @app_commands.command(
        name="bestartifact",
        description="Best artifact rolls for Mages and Attack Immortals"
    )
    @app_commands.describe(
        role="Select your role",
        build="Select your build"
    )
    @app_commands.autocomplete(role=role_autocomplete, build=build_autocomplete)
    async def bestartifact(
        self,
        interaction: discord.Interaction,
        role: str,
        build: str
    ):
        role = role.lower()
        build = build.lower()

        try:
            if role == "mage":
                if build == "crit":
                    text = (
                        "🔮 **Mage – Crit (Chase) Build**\n\n"
                        "Priority Rolls: Crit Rate → Magical Attack → Crit Damage → Magical → Defenses\n"
                        "💡 Best if VIP 13+"
                    )
                elif build == "nonchase":
                    text = (
                        "🔮 **Mage – Non-Chase Build**\n\n"
                        "Priority Rolls: Magical Attack → Magical Attack Value → Crit Rate → Crit Damage → Defenses\n"
                        "💡 Focus on pure % damage"
                    )
                else:
                    text = f"❌ Invalid build. Available: {', '.join(BUILDS['mage'])}"
            elif role == "attack":
                if build == "ultimate":
                    text = (
                        ⚔️ **Attack – Ultimate DPS**\n\n"
                        "Top Priority: Physical Attack → Surge → Iron Fist → Magical Defense → Accuracy → Physical Defense\n"
                        "📌 Examples: Herald, William, Attila, Ramesses, Hippolyta"
                    )
                elif build == "physical":
                    text = (
                        "⚔️ **Attack – Physical DPS**\n\n"
                        "Top Priority: Physical Attack → Rapid (Alex/Hannibal) → Accuracy → Physical Defense → Crit\n"
                        "📌 Examples: Alexander, Hannibal, Manco, Saladin"
                    )
                else:
                    text = f"❌ Invalid build. Available: {', '.join(BUILDS['attack'])}"
            else:
                text = f"❌ Invalid role. Available: {', '.join(ROLES)}"

            await interaction.response.send_message(text, ephemeral=False)

        except Exception as e:
            try:
                await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)
            except:
                await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BestArtifact(bot))
