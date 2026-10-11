import os
import threading
import discord
from discord.ext import commands
from flask import Flask

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True  # مهم جداً لمراقبة الرومات الصوتية
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# آي دي روم الـ AFK الخاص بك
AFK_CHANNEL_ID = 1557168763189596270


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
  print("Bot is ready and online!")


@bot.event
async def on_voice_state_update(member, before, after):
  # التأكد أن العضو دخل روم الـ AFK ولم يكن فيه من قبل
  if after.channel and after.channel.id == AFK_CHANNEL_ID:
    if before.channel is None or before.channel.id != AFK_CHANNEL_ID:
      try:
        # تطبيق الميوت والديَفن مباشرة
        await member.edit(mute=True, deafen=True, reason="Entered AFK room")
        print(f"Muted and deafened {member.name} in AFK room.")
      except Exception as e:
        print(f"Failed to mute {member.name}: {e}")


# --- سيرفر الـ Flask الوهمي (Keep-Alive) ---
app = Flask("")


@app.route("/")
def home():
  return "I am alive and the AFK bot is running!"


def run():
  # Render يتطلب استخدام المنفذ 8080
  app.run(host="0.0.0.0", port=8080)


def keep_alive():
  t = threading.Thread(target=run)
  t.daemon = True
  t.start()


# تشغيل السيرفر والبوت مباشرة
if __name__ == "__main__":
  keep_alive()
  bot.run("MTU1ODg2ODIyMDExMzQ1NzIwMw.G253sa.wfuWNtPIPoSMKtBqu4BPqUCKZsbjlaHd89_xP0")
