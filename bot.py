import os
import json
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
from openai import OpenAI
import asyncio
import re

from immortals import IMMORTALS

# =====================================================
# WEB SERVER (RENDER)
# =====================================================
app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

# =====================================================
# OPENAI
# =====================================================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_artifact_build(name, data):
    prompt = f"""
You are a game build expert.

Return ONLY valid JSON:
{{
  "best_artifact": "",
  "best_main_stat": "",
  "best_passive": "",
  "alternative_passive": ""
}}

Game data:
Best: {data['best']}
Good: {data['good']}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are precise and factual."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
    except Exception as e:
        print("⚠️ OpenAI API error:", e)
        return {
            "best_artifact": "Unknown",
            "best_main_stat": "Unknown",
            "best_passive": "Unknown",
            "alternative_passive": "Unknown"
        }

    content = response.choices[0].message.content
    print("DEBUG AI RESPONSE:", content)

    # Extract JSON from text in case AI adds extra text
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        content = match.group(0)

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ AI returned invalid JSON, returning default object.")
        return {
            "best_artifact": "Unknown",
            "best_main_stat": "Unknown",
            "best_passive": "Unknown",
            "alternative_passive": "Unknown"
        }

# =====================================================
# DISCORD BOT
# =====================================================
intents = discord.Intents.default()
intents.message_content = True  # IMPORTANT: allows reading message content
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} | Slash commands synced")

# =====================================================
# SLASH COMMAND
# =====================================================
@bot.tree.command(
    name="bestartifact",
    description="Get the best artifact build for an immortal"
)
@app_commands.describe(immortal="Name of the immortal (e.g. alex)")
async def bestartifact(interaction: discord.Interaction, immortal: str):
    name = immortal.lower()

    if name not in IMMORTALS:
        await interaction.response.send_message(
            f"❌ Immortal **{immortal}** not found.",
            ephemeral=True
        )
        return

    # Defer – inform Discord the response will take some time
    await interaction.response.defer()

    try:
        # Run blocking function in a separate thread
        ai_data = await asyncio.to_thread(get_ai_artifact_build, name, IMMORTALS[name])
    except Exception as e:
        print("⚠️ AI error in slash command:", e)
        await interaction.followup.send("❌ AI error. Please try again later.")
        return

    embed = discord.Embed(
        title=f"✨ TL;DR – Best Artifact for {name.title()}",
        color=discord.Color.gold()
    )

    embed.add_field(name="⭐ Best Artifact", value=ai_data["best_artifact"], inline=False)
    embed.add_field(name="⚔️ Best Main Stat", value=ai_data["best_main_stat"], inline=False)
    embed.add_field(name="⚡ Best Passive Roll", value=ai_data["best_passive"], inline=False)
    embed.add_field(name="🔁 Alternative Passive", value=ai_data["alternative_passive"], inline=False)

    await interaction.followup.send(embed=embed)

# =====================================================
# RUN
# =====================================================
bot.run(os.getenv("DISCORD_TOKEN"))
