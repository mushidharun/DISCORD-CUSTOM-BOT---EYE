# =========================================================
#  ZETRA DISCORD BUSINESS BOT – COMMERCIAL EDITION
#  COPYRIGHT OWNER : MUSHI DHARUN (ZETRA)
#  PRICE : DM ME DIRECTLY OR CONTACT IN MY SERVER
#  SERVER : https://discord.gg/uxMjPz749k
#
#  This software is proprietary and confidential.
#  Unauthorized copying, modification, resale,
#  redistribution, or sharing is strictly prohibited.
# =========================================================


import discord
from discord.ext import commands, tasks
import asyncio
from config import TOKEN

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

# 👁️ STATUS LOOP
@tasks.loop(seconds=30)
async def status_loop():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="ZETRA IS WATCHING YOU 👁️"
        )
    )


# 🔁 READY EVENT
@bot.event
async def on_ready():
    print("===================================")
    print(f"BLUE EYE ONLINE 👁️ {bot.user}")
    print(f"ID: {bot.user.id}")
    print(f"Servers: {len(bot.guilds)}")
    print("ZETRA IS WATCHING YOU 👁️")
    print("===================================")

    # Start status loop once
    if not status_loop.is_running():
        status_loop.start()

    # Sync slash commands safely
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print(f"Slash sync error: {e}")


# ❌ COMMAND ERROR HANDLER (SAFE)
@bot.event
async def on_command_error(ctx, error):
    # Ignore command not found
    if isinstance(error, commands.CommandNotFound):
        return

    print(f"Command error: {error}")

    try:
        await ctx.send("⚠️ Command error occurred. Check console.")
    except:
        pass

# 📦 LOAD COGS
async def load_cogs():
    cogs = [
        "cogs.staff_check",
        "cogs.database",
        "cogs.storage_ui",
        "cogs.buy_ui",
        "cogs.sell_ui",
        "cogs.grind_ui",
        "cogs.boss_report",
        "cogs.auto_backup",
        "cogs.leaderboard",
        "cogs.level",
        "cogs.file_backup",
        "cogs.orders_ui"
    ]

    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"Loaded → {cog}")
        except Exception as e:
            print(f"Failed → {cog} | {e}")

# 🏁 MAIN
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

# 🧪 TEST COMMAND
@bot.command()
async def ping(ctx):
    await ctx.send("Pong 👁️")


asyncio.run(main())
