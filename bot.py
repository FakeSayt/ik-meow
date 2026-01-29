import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread
import asyncio
import traceback
from openai import OpenAI

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

# =====================================================
# HERO BUILDS DICTIONARY (pełna lista Immortali)
# =====================================================
HERO_BUILDS = {
    "wukong": """✨ TL;DR – Best Artifact for Wukong
⭐ Best Artifact: Heart of Spiritual Stone
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "louis ix": """✨ TL;DR – Best Artifact for Louis IX
⭐ Best Artifact: Justice Grasp
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "tutankhamun": """✨ TL;DR – Best Artifact for Tutankhamun
⭐ Best Artifact: Meteoric Dagger
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "khubilai khan": """✨ TL;DR – Best Artifact for Khubilai Khan
⭐ Best Artifact: The Code of Yuan
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "manco": """✨ TL;DR – Best Artifact for Manco
⭐ Best Artifact: Barricade of Light
⚔️ Best Main Stat: HP %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "alexander the great": """✨ TL;DR – Best Artifact for Alexander the Great
⭐ Best Artifact: Homer’s Epic
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "hippolyta": """✨ TL;DR – Best Artifact for Hippolyta
⭐ Best Artifact: Godesses’ Waist Belt
⚔️ Best Main Stat: HP %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "william": """✨ TL;DR – Best Artifact for William
⭐ Best Artifact: The Domesday Book
⚔️ Best Main Stat: HP %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "attila the hun": """✨ TL;DR – Best Artifact for Attila the Hun
⭐ Best Artifact: Celestial’s Blade
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "saladin": """✨ TL;DR – Best Artifact for Saladin
⭐ Best Artifact: Wings of War
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "muhammad ii": """✨ TL;DR – Best Artifact for Muhammad II
⭐ Best Artifact: Code of Order
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "siegfried": """✨ TL;DR – Best Artifact for Siegfried
⭐ Best Artifact: Dark Dragon’s Blood
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "peter the great": """✨ TL;DR – Best Artifact for Peter the Great
⭐ Best Artifact: Justice Grasp
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "ramesses ii": """✨ TL;DR – Best Artifact for Ramesses II
⭐ Best Artifact: The Sun’s Gift
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "hannibal barca": """✨ TL;DR – Best Artifact for Hannibal Barca
⭐ Best Artifact: The War Colossus
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "herald": """✨ TL;DR – Best Artifact for Herald
⭐ Best Artifact: Figurehead of War Dragon
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "frederick": """✨ TL;DR – Best Artifact for Frederick
⭐ Best Artifact: Crown of Flame
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "loki": """✨ TL;DR – Best Artifact for Loki
⭐ Best Artifact: Inferno Crown
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "hammurabi": """✨ TL;DR – Best Artifact for Hammurabi
⭐ Best Artifact: The Totem of Order
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "himiko": """✨ TL;DR – Best Artifact for Himiko
⭐ Best Artifact: The Golden Seal
⚔️ Best Main Stat: Magical Attack %
⚡ Best Passive Roll: Annihilation
🔁 Alternative Passive: Destruction""",
    "empress wu": """✨ TL;DR – Best Artifact for Empress Wu
⭐ Best Artifact: Locana Buddha
⚔️ Best Main Stat: Magical Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "baldwin iv": """✨ TL;DR – Best Artifact for Baldwin IV
⭐ Best Artifact: The Silver Mask of Baldwin
⚔️ Best Main Stat: HP %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "merlin": """✨ TL;DR – Best Artifact for Merlin
⭐ Best Artifact: Dragon’s Prophecy
⚔️ Best Main Stat: Magical Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "cleopatra": """✨ TL;DR – Best Artifact for Cleopatra
⭐ Best Artifact: The Eternal Serpent
⚔️ Best Main Stat: Magical Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "bjorn": """✨ TL;DR – Best Artifact for Bjorn
⭐ Best Artifact: Source of Terror
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "king arthur": """✨ TL;DR – Best Artifact for King Arthur
⭐ Best Artifact: Scabbard of Avalon
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "el cid": """✨ TL;DR – Best Artifact for El Cid
⭐ Best Artifact: The Song of the Cid
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "leonidas": """✨ TL;DR – Best Artifact for Leonidas
⭐ Best Artifact: Titan’s Prove
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "julius caesar": """✨ TL;DR – Best Artifact for Julius Caesar
⭐ Best Artifact: Julian Calendar
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "charles": """✨ TL;DR – Best Artifact for Charles
⭐ Best Artifact: Grasps of Glory
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "ragnar": """✨ TL;DR – Best Artifact for Ragnar
⭐ Best Artifact: War Helm
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "trajan": """✨ TL;DR – Best Artifact for Trajan
⭐ Best Artifact: Trajan’s Column
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "tokugawa": """✨ TL;DR – Best Artifact for Tokugawa
⭐ Best Artifact: Golden Blunderbuss
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "gilgamesh": """✨ TL;DR – Best Artifact for Gilgamesh
⭐ Best Artifact: Uluk Relief
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "elizabeth bathory": """✨ TL;DR – Best Artifact for Elizabeth Bathory
⭐ Best Artifact: Vampire’s Glass
⚔️ Best Main Stat: Magical Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "yoshitsune": """✨ TL;DR – Best Artifact for Yoshitsune
⭐ Best Artifact: Scroll of the Tiger
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "yi seong-gye": """✨ TL;DR – Best Artifact for Yi Seong‑gye
⭐ Best Artifact: The Code of Gyeongguk
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "ashoka": """✨ TL;DR – Best Artifact for Ashoka
⭐ Best Artifact: The Legendary Pillar
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "genghis khan": """✨ TL;DR – Best Artifact for Genghis Khan
⭐ Best Artifact: Great Code of Genghis Khan
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "arash": """✨ TL;DR – Best Artifact for Arash
⭐ Best Artifact: Champion’s Arrow
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "atalanta": """✨ TL;DR – Best Artifact for Atalanta
⭐ Best Artifact: Protection of the Moon
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "seondeok": """✨ TL;DR – Best Artifact for Seondeok
⭐ Best Artifact: Endless Artwork
⚔️ Best Main Stat: Magical Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "margaret i": """✨ TL;DR – Best Artifact for Margaret I
⭐ Best Artifact: Alliance Seal
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
    "nebuchadnezzar ii": """✨ TL;DR – Best Artifact for Nebuchadnezzar II
⭐ Best Artifact: The Ishtar Gate
⚔️ Best Main Stat: Attack %
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown""",
}

# =====================================================
# AI COMPLETION FOR UNKNOWN FIELDS
# =====================================================
def ai_fill_unknowns(hero_name: str, build_text: str):
    if "Unknown" not in build_text:
        return build_text

    prompt = f"""
You are an expert in the game Infinity Kingdom. Only use actual in-game data.
The hero is "{hero_name}".
Here is the current TL;DR build:

{build_text}

Please fill in the Unknown fields (⭐ Best Artifact for example for Genghis Khan is it Iron Fist Or Annihilation /⚡ Best Passive Roll (cavalry attack % etc doesn't exist in artifacts stats please make sure it's correct / 🔁 Alternative Passive (cavalry attack % etc doesn't exist in artifacts stats please make sure it's correct / ⚔️ Best Main Stat (for mages like Merlin, Himiko it's Crit % and 2nd/alternative passive is % magic damage so please check thsi also.) with accurate Infinity Kingdom mobile game..
Do NOT invent artifacts. Only provide valid stats or passives. Respond ONLY with the updated TL;DR build in the exact same format.
If unknown, leave it as 'Unknown'.
"""

    try:
        response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.0,
    max_tokens=200
)
        content = response.choices[0].message.content.strip()
        return content if content else build_text
    except Exception as e:
        print("[ERROR] AI failed to fill unknowns:", repr(e))
        traceback.print_exc()
        return build_text

# =====================================================
# GET BUILD FUNCTION
# =====================================================
def get_hero_build(name: str):
    name_lower = name.lower()
    build = HERO_BUILDS.get(name_lower)
    if not build:
        return f"""✨ TL;DR – Best Artifact for {name.title()}
⭐ Best Artifact: Unknown
⚔️ Best Main Stat: Unknown
⚡ Best Passive Roll: Unknown
🔁 Alternative Passive: Unknown"""
    
    build_filled = ai_fill_unknowns(name, build)
    return build_filled

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

    try:
        await interaction.response.defer()
    except Exception as e:
        print("[WARNING] Defer failed:", repr(e))
        return

    try:
        build_text = await asyncio.to_thread(get_hero_build, name)
    except Exception as e:
        print("[ERROR] Failed to get build:", repr(e))
        await interaction.followup.send("Error fetching artifact build.")
        return

    embed = discord.Embed(
        title=f"✨ TL;DR – Best Artifact for {name.title()}",
        description=build_text,
        color=discord.Color.gold()
    )

    await interaction.followup.send(embed=embed)

# =====================================================
# RUN BOT
# =====================================================
bot.run(discord_token)
