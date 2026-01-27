import discord
from discord.ext import commands
import os

from flask import Flask
from threading import Thread

from immortals import IMMORTALS
from artifacts import ARTIFACTS

# ================== WEB SERVER (RENDER NEEDS PORT) ==================
app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

# ================== TOKEN ==================
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("❌ TOKEN not found! Set it in Render Environment Variables.")

# ================== INTENTS ==================
intents = discord.Intents.default()
intents.message_content = True

# ================== BOT SETUP ==================
bot = commands.Bot(command_prefix="!", intents=intents)

# ================== READY EVENT ==================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ================== MESSAGE HANDLER ==================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower().strip()

    if content.startswith("best artifact for"):
        name = content.replace("best artifact for", "").strip()

        if name in IMMORTALS:
            data = IMMORTALS[name]
            response = (
                f"🛡️ **Best artifact for {name.title()}**\n\n"
                f"🏆 **Best:**\n{data['best']}\n\n"
                f"🟡 **Good to have for now:**\n{data['good']}"
            )
            await message.channel.send(response)
        else:
            available = ", ".join(i.title() for i in IMMORTALS.keys())
            await message.channel.send(
                f"❌ Immortal **{name}** not found.\nAvailable: {available}"
            )

    await bot.process_commands(message)

# ================== RUN BOT ==================
bot.run(TOKEN)
