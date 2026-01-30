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

    # AUTOCOMPLETE dla role
    async def role_autocomplete(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=r, value=r) for r in ROLES if current.lower() in r.lower()]

    # AUTOCOMPLETE dla build w zależności od role
    async def build_autocomplete(self, interaction: discord.Interaction, current: str):
        # pobieramy wartość wybranej role z interaction
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

        text = None

        try:
            # =========================
            # MAGE ARTIFACTS
            # =========================
            if role == "mage":
                if build == "crit":
                    text = (
                        "🔮 **Mage – Crit (Chase) Build**\n\n"
                        "**Priority Rolls:**\n"
                        1️⃣ Crit Rate → Crit Rate (%)\n"
                        "2️⃣ Magical Attack (%) → Crit Rate Value\n"
                        "3️⃣ Crit Value / Magical Attack Value → Crit Damage\n"
                        "4️⃣ Magical (%) / Magical Attack\n"
                        "5️⃣ Resilience / Dodge / Defenses\n\n"
                        "💡 Best if you are VIP 13+ with high crit rate."
                    )
                elif build == "nonchase":
                    text = (
                        "🔮 **Mage – Non-Chase Build**\n\n"
                        "**Priority Rolls:**\n"
                        "1️⃣ Magical Attack (%) → Magical (%)\n"
                        "2️⃣ Magical Attack Value → Magical Attack\n"
                        "3️⃣ Crit Rate → Crit Rate / Crit Value\n"
                        "4️⃣ Crit Value → Crit Damage\n"
                        "5️⃣ Resilience / Dodge / Defenses\n\n"
                        "💡 Focus on pure % damage, crit is secondary."
                    )
                else:
                    text = f"❌ Invalid build. Available: {', '.join(BUILDS['mage'])}"

            # =========================
            # ATTACK ARTIFACTS
            # =========================
            elif role == "attack":
                if build == "ultimate":
                    text = (
                        "⚔️ **Attack – Ultimate Ability DPS**\n\n"
                        "**Top Priority:**\n"
                        "1️⃣ Physical Attack Rate → Surge\n"
                        "2️⃣ Physical Attack Value → Iron Fist\n"
                        "3️⃣ Magical Defense\n"
                        "4️⃣ Accuracy\n"
                        "5️⃣ Physical Defense\n\n"
                        "**Examples:** Herald, William, Attila, Ramesses, Hippolyta"
                    )
                elif build == "physical":
                    text = (
                        "⚔️ **Attack – Physical DPS**\n\n"
                        "**Top Priority:**\n"
                        "1️⃣ Physical Attack Rate → Iron Fist\n"
                        "2️⃣ Physical Attack Value → Rapid (Alex/Hannibal)\n"
                        "3️⃣ Accuracy\n"
                        "4️⃣ Physical Defense\n"
                        "5️⃣ Crit Rate / Crit Value\n\n"
                        "**Examples:** Alexander, Hannibal, Manco, Saladin"
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
