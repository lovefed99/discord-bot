import asyncio
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import requests
import os

# ========== Flask 保活伺服器 ==========
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    try:
        app.run(host='0.0.0.0', port=8080)
    except OSError:
        print("❗ Port 8080 被佔用，改用 8081")
        app.run(host='0.0.0.0', port=8081)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ========== 自我 Ping 機制 ==========
async def self_ping():
    while True:
        try:
            requests.get("http://127.0.0.1:8080/")
            print("🔁 已自動 ping 自己一次")
        except Exception as e:
            print(f"⚠️ 自動 ping 失敗：{e}")
        await asyncio.sleep(300)  # 每 5 分鐘 ping 一次

# ========== Discord Bot 設定 ==========
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot 已上線：{bot.user}")
    bot.loop.create_task(self_ping())  # 啟動自我 ping 任務

@bot.event
async def on_member_update(before, after):
    guild = after.guild
    role_sakura = discord.utils.get(guild.roles, name="櫻花貓貓")
    role_meat = discord.utils.get(guild.roles, name="鮮肉貓貓")
    role_ghost = discord.utils.get(guild.roles, name="幽靈貓貓")
    notify_channel = discord.utils.get(guild.text_channels, name="身分組領取區")

    if not role_sakura or not role_meat or not role_ghost:
        print("⚠️ 找不到其中一個身分組，請檢查拼字")
        return

    before_roles = set(before.roles)
    after_roles = set(after.roles)
    added_roles = after_roles - before_roles

    if role_sakura in added_roles or role_meat in added_roles:
        if role_ghost in after.roles:
            await after.remove_roles(role_ghost)
            print(f"✅ {after.name} 的『幽靈貓貓』已被移除")

            if notify_channel:
                content = "```ini\n[通知] 恭喜 {} 已正式脫離幽靈貓貓身份！\n```".format(after.display_name)
                msg = await notify_channel.send(content)
                await asyncio.sleep(86400)
                await msg.delete()
            else:
                print("⚠️ 找不到『身分組領取區』頻道，無法發送通知")

@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    trigger_channels = {
        "建立【OW】頻道點我": "【OW】",
        "建立【LOL】頻道點我": "【LOL】",
        "建立【APEX】頻道點我": "【APEX】",
        "建立【Valorant】頻道點我": "【Valorant】"
    }

    if after.channel and after.channel.name in trigger_channels:
        prefix = trigger_channels[after.channel.name]
        new_channel = await guild.create_voice_channel(
            name=f"{prefix}{member.display_name}",
            category=after.channel.category
        )
        await member.move_to(new_channel)
        print(f"🎧 為 {member.display_name} 建立語音房：{new_channel.name}")

        while True:
            await asyncio.sleep(10)
            if len(new_channel.members) == 0:
                await new_channel.delete()
                print(f"🗑️ 自動刪除空房：{new_channel.name}")
                break
import os
bot.run(os.environ['MTM2MzkxODI1NDYxOTIzNDQ3NQ.GcoKiC.7_lxXhBwV7o4ANoDAD0uWKUm5LNkWeetQcf10Ms'])  # 注意 BOT_TOKEN 要跟 Render 環境變數名稱一致
