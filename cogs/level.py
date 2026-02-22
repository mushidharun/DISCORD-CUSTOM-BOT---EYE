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
import aiosqlite

from cogs.ui_theme import base_embed, error_embed
from config import LEVEL_UP_BASE, DB_PATH


class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        async with aiosqlite.connect(DB_PATH) as db:
            row = await (
                await db.execute(
                    "SELECT xp, level FROM levels WHERE user_id = ?",
                    (member.id,)
                )
            ).fetchone()

        if not row:
            return await ctx.send(
                embed=error_embed("No level data", "This worker has no XP yet.")
            )

        xp, level = row

        # 📊 XP CALCULATION
        xp_needed = max(level * LEVEL_UP_BASE, 1)
        progress_ratio = min(xp / xp_needed, 1)

        filled = int(progress_ratio * 10)
        progress_bar = "█" * filled + "░" * (10 - filled)

        embed = base_embed("🎖️ WORKER LEVEL CARD")

        embed.add_field(name="👤 Staff", value=member.mention)
        embed.add_field(name="⭐ Level", value=f"`{level}`")
        embed.add_field(name="⚡ XP", value=f"`{xp}/{xp_needed}`")
        embed.add_field(
            name="📊 Progress",
            value=f"`{progress_bar}` ({int(progress_ratio*100)}%)",
            inline=False
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Level(bot))
