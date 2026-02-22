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
from datetime import datetime, timedelta

# DEFAULT ICON
DEFAULT_ICON = "https://cdn.discordapp.com/attachments/1472864702668210360/1472864714089300010/2222222.png"

# 🕒 IST TIME
def get_ist_time():
    ist = datetime.utcnow() + timedelta(hours=5, minutes=30)
    return ist.strftime("%H:%M IST")

# 🔷 BASE EMBED (SAFE)
def base_embed(title: str, description: str = None, color: discord.Colour = None):
    color = color or discord.Color.blue()

    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    embed.set_thumbnail(url=DEFAULT_ICON)
    embed.set_footer(text=f"BANGALORE AQUA&CO. • {get_ist_time()} 👁️")

    return embed

# ✅ SUCCESS
def success_embed(title: str, description: str = None):
    return base_embed(title, description, discord.Color.green())

# ❌ ERROR
def error_embed(title: str, description: str = None):
    return base_embed(title, description, discord.Color.red())


# ⚠️ WARNING
def warning_embed(title: str, description: str = None):
    return base_embed(title, description, discord.Color.orange())

# 👑 BOSS
def boss_embed(title: str, description: str = None):
    return base_embed(title, description, discord.Color.gold())
