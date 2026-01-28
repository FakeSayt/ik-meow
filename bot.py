import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
from openai import OpenAI
import asyncio
import traceback

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
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is missing!")

client = OpenAI(api_key=openai_api_key)

def get_ai_artifact_build(name, data):
    prompt = f"""
You are an expert in the game Infinity Kingdom. 
The following data lists artifacts for a specific immortal hero in the game. 

"Best" are the top recommended artifacts.
"Good" are other viable artifacts.

Using this data, provide the best artifact build for this immortal, including:
- Best Artifact
- Best Main Stat
- Best Passive
- Alternative Passive

Game data:
Best: {data['best']}
Good: {data['good']}

Return your answer in TL;DR style. Only use values from the Best and Good lists if possible.
"""
    try:
        print(f"[DEBUG] Sending prompt to OpenAI for {name}:")
        print(prompt)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        content = response.choices[0].message.content
        print("[DEBUG] AI Response:")
        print(content)
        return content.strip()
    except Exception as e:
        print("[ERROR] AI error while generating artifact build!")
        print("Exception:", repr(e))
        traceback.print_exc()
        return None

# =====================================================
# DISCORD BOT
# =====================================================
discord_token = os.environ.get("DISCORD_TOKEN")
if not discord_token:
    raise ValueError("DISCORD_TOKEN environment variable is missing!")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} | Slash commands synced")

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
            f"Immortal **{immortal}** not found.",
            ephemeral=True
        )
        return

    await interaction.response.defer()

    ai_text = await asyncio.to_thread(get_ai_artifact_build, name, IMMORTALS[name])

    if not ai_text:
        await interaction.followup.send("AI could not generate the artifact build. Please check logs for details.")
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
