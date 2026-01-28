import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
from openai import OpenAI
import asyncio

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
# OPENAI CLIENT
# =====================================================
openai_api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

def get_ai_artifact_build_freeform(name, data):
    prompt = f"""
You are an expert in the game Infinity Kingdom. 
Given the following game data for an immortal, suggest the best artifact, main stat, passive, and alternative passive.

Game data:
Best: {data['best']}
Good: {data['good']}

Return your answer in a short TL;DR style, for example:
Best Artifact: ...
Best Main Stat: ...
Best Passive: ...
Alternative Passive: ...
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        content = response.choices[0].message.content
        print("DEBUG AI RESPONSE:", content)
        return content
    except Exception as e:
        print("[WARNING] OpenAI API error:", e)
        return "AI could not generate the artifact build. Please try again later."

# =====================================================
# DISCORD BOT
# =====================================================
discord_token = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
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

    await interaction.response.defer()

    try:
        ai_text = await asyncio.to_thread(get_ai_artifact_build_freeform, name, IMMORTALS[name])
    except Exception as e:
        print("[WARNING] AI error in slash command:", e)
        await interaction.followup.send("❌ AI error. Please try again later.")
        return

    embed = discord.Embed(
        title=f"✨ TL;DR – Best Artifact for {name.title()}",
        description=ai_text,
        color=discord.Color.gold()
    )

    await interaction.followup.send(embed=embed)

# =====================================================
# RUN
# =====================================================
bot.run(discord_token)
