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
    app.run(host="0.0.0.0", port=PORT, use_reloader=False)

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
    for extension in ["bestartifact", "damage", "helpmeow", "meowwiki"]:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(f"Error loading {extension}: {e}")

# =====================================================
# SETUP HOOK
# =====================================================
@bot.event
async def setup_hook():
    await load_extensions()
    await bot.tree.sync()
    print(f"{bot.user} is online and all commands are synced!")

# =====================================================
# RUN BOT
# =====================================================
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is missing!")

bot.run(DISCORD_TOKEN)
