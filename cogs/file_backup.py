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
from discord.ext import commands
import os
from datetime import datetime

from config import OWNER_ID, DB_PATH
from cogs.ui_theme import boss_embed, error_embed


class FileBackup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def backupfile(self, ctx):
        # 👑 Boss only
        if ctx.author.id != OWNER_ID:
            return await ctx.send(
                embed=error_embed("Access denied", "Boss only command 👑")
            )

        # 📂 Check DB exists
        if not os.path.exists(DB_PATH):
            return await ctx.send(
                embed=error_embed("Backup failed", "Database file not found.")
            )

        # 🕒 Timestamped filename
        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"backup_{timestamp}.db"

        try:
            file = discord.File(DB_PATH, filename=backup_name)

            embed = boss_embed("📂 DATABASE BACKUP READY")
            embed.description = "Download the latest business database snapshot."

            await ctx.send(embed=embed, file=file)

        except Exception as e:
            await ctx.send(
                embed=error_embed("Backup failed", f"Error: {e}")
            )


async def setup(bot):
    await bot.add_cog(FileBackup(bot))
