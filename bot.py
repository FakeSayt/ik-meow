import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
from openai import OpenAI
import asyncio
import traceback

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

def get_ai_artifact_build(name: str):
    """
    Funkcja wysyła prompt do OpenAI i zwraca tekst w TL;DR stylu, mocno ograniczony do Infinity Kingdom.
    """
    prompt = f"""
You are an expert in the game Infinity Kingdom. Only provide information from Infinity Kingdom. 
Do not mention any other games. 

The player provided the immortal hero name "{name}". 

Provide the **best artifact build** including:
- Best Artifact
- Best Main Stat
- Best Passive
- Alternative Passive

Use the TL;DR format exactly like this example:

✨ TL;DR – Best Artifact for Alex
⭐ Best Artifact: [artifact name]⚔️ Best Main Stat: [main stat]
⚡ Best Passive Roll: [passive]
🔁 Alternative Passive: [alternative passive]

Respond only with the build. Do not add extra commentary.
"""

    try:
        print(f"[DEBUG] Sending prompt to OpenAI for {name}:")
        print(prompt)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2  # niska temperatura, żeby ograniczyć wymyślanie
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
    description="Get the best artifact build for any immortal"
)
@app_commands.describe(immortal="Name of the immortal (e.g., Himiko, Wu, Alex)")
async def bestartifact(interaction: discord.Interaction, immortal: str):
    name = immortal.strip()

    # Defer interaction – pozwala AI pracować bez timeoutu Discorda
    try:
        await interaction.response.defer()
    except discord.errors.NotFound:
        print(f"[WARNING] Interaction for {name} already expired.")
        return
    except discord.errors.HTTPException as e:
        print(f"[WARNING] Interaction already acknowledged: {repr(e)}")
        return
    except Exception as e:
        print("[ERROR] defer() failed:", repr(e))
        traceback.print_exc()
        return

    # Wywołanie AI w osobnym wątku z timeoutem 2 minuty
    try:
        ai_text = await asyncio.wait_for(
            asyncio.to_thread(get_ai_artifact_build, name),
            timeout=120.0
        )
    except asyncio.TimeoutError:
        await interaction.followup.send("⏱ AI took too long to respond (over 2 minutes). Please try again later.")
        return
    except Exception as e:
        print("[ERROR] AI execution failed:", repr(e))
        traceback.print_exc()
        await interaction.followup.send("❌ AI error occurred. Check logs.")
        return

    if not ai_text:
        await interaction.followup.send(f"⚠️ AI could not generate artifact build for **{name}**. Please try again later.")
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
