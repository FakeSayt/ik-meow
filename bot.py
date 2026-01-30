import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands
from config import DISCORD_TOKEN, PORT

# =====================================================
# FLASK SERVER (KEEP-ALIVE)
# =====================================================
app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=PORT)

Thread(target=run_web).start()

# =====================================================
# DISCORD BOT SETUP
# =====================================================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# =====================================================
# LOAD EXTENSIONS / COMMANDS
# =====================================================
async def load_extensions():
    """Load all cogs (slash commands)"""
    await bot.load_extension("bestartifact")
    await bot.load_extension("damage")
    await bot.load_extension("helpmeow")

# =====================================================
# ON_READY EVENT
# =====================================================
@bot.event
async def on_ready():
    await load_extensions()

    # Optionally sync slash commands to a specific guild for instant update
    # Replace with your test server ID
    GUILD_ID = None  # e.g., 123456789012345678
    if GUILD_ID:
        guild = discord.Object(id=GUILD_ID)
        await bot.tree.sync(guild=guild)
        print(f"Slash commands synced to guild {GUILD_ID}")
    else:
        # Global sync (may take up to 1 hour to appear)
        await bot.tree.sync()
        print("Global slash commands synced")

    print(f"{bot.user} is online and ready!")

# =====================================================
# RUN BOT
# =====================================================
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is missing!")

bot.run(DISCORD_TOKEN)
