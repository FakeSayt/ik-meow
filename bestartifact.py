import discord
from discord.ext import commands
from discord import app_commands

class BestArtifact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="bestartifact",
        description="Best artifact rolls for Mages and Attack Immortals"
    )
    @app_commands.describe(
        role="mage / attack",
        build="mage: crit or nonchase | attack: ultimate or physical"
    )
    async def bestartifact(
        self,
        interaction: discord.Interaction,
        role: str,
        build: str
    ):
        role = role.lower()
        build = build.lower()

        # =========================
        # MAGE ARTIFACTS
        # =========================
        if role == "mage":
            if build == "crit":
                text = (
                    "🔮 **Mage – Crit (Chase) Build**\n\n"
                    "**Priority Rolls:**\n"
                    1️⃣ **Crit Rate (%)** → Crit Rate (%)\n"
                    "2️⃣ Magical Attack (%) → Crit Rate Value\n"
                    "3️⃣ Crit Value / Magical Attack Value → Crit Damage Value\n"
                    "4️⃣ Magical (%) / Magical Attack\n"
                    "5️⃣ Resilience / Dodge / Defenses\n\n"
                    "💡 Best if you are **VIP 13+** with high crit rate."
                )

            elif build == "nonchase":
                text = (
                    "🔮 **Mage – Non-Chase (Concentration) Build**\n\n"
                    "**Priority Rolls:**\n"
                    "1️⃣ **Magical Attack (%)** → Magical (%)\n"
                    "2️⃣ Magical Attack Value → Magical Attack\n"
                    "3️⃣ Crit Rate (%) → Crit Rate / Crit Rate Value\n"
                    "4️⃣ Crit Value → Crit Damage Value\n"
                    "5️⃣ Resilience / Dodge / Defenses\n\n"
                    "💡 Focus on **pure % damage**, crit is secondary."
                )

            else:
                text = "❌ Mage build must be: **crit** or **nonchase**"

        # =========================
        # ATTACK ARTIFACTS
        # =========================
        elif role == "attack":
            if build == "ultimate":
                text = (
                    "⚔️ **Attack – Ultimate Ability Based Utility & DPS**\n\n"
                    "**Top Priority:**\n"
                    "1️⃣ Physical Attack Rate (%) → **Surge (energy regen)**\n"
                    "2️⃣ Physical Attack Value → Iron Fist\n"
                    "3️⃣ Magical Defense Rate / Value\n"
                    "4️⃣ Accuracy Rate / Value\n"
                    "5️⃣ Physical Defense\n\n"
                    "📌 Surge is **mandatory** – these Immortals depend on Ultimates.\n"
                    "📌 Accuracy is critical if you don't run Coercion.\n\n"
                    "**Examples:** Herald, William, Attila, Ramesses, Hippolyta"
                )

            elif build == "physical":
                text = (
                    "⚔️ **Attack – Physical Damage Dealer**\n\n"
                    "**Top Priority:**\n"
                    "1️⃣ Physical Attack Rate (%) → **Iron Fist**\n"
                    "2️⃣ Physical Attack Value → Rapid (Alex / Hannibal only)\n"
                    "3️⃣ Accuracy Rate / Value\n"
                    "4️⃣ Physical Defense\n"
                    "5️⃣ Crit Rate / Crit Value\n\n"
                    "📌 **Accuracy is mandatory** unless fully hit-capped.\n"
                    "📌 Surge is useless for Alex & Hannibal.\n\n"
                    "**Examples:** Alexander, Hannibal, Manco, Saladin"
                )

            else:
                text = "❌ Attack build must be: **ultimate** or **physical**"

        else:
            text = "❌ Role must be: **mage** or **attack**"

        await interaction.response.send_message(text)

async def setup(bot):
    await bot.add_cog(BestArtifact(bot))
