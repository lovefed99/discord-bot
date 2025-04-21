import asyncio
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

# Flask 保活
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    try:
        app.run(host='0.0.0.0', port=8080)
    except OSError:
        print("⚠️  Port 8080 被佔用，改用 8081")
        app.run(host='0.0.0.0', port=8081)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Discord Bot 設定
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot 已上線：{bot.user}")

keep_alive()
bot.run(os.getenv("BOT_TOKEN"))
