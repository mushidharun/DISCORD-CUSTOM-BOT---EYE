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
from config import DB_PATH


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leaderboard(self, ctx):
        async with aiosqlite.connect(DB_PATH) as db:
            rows = await (
                await db.execute("""
                    SELECT user_id, actions
                    FROM staff_activity
                    ORDER BY actions DESC
                    LIMIT 10
                """)
            ).fetchall()

        if not rows:
            return await ctx.send(
                embed=error_embed(
                    "No activity data",
                    "No staff actions recorded yet."
                )
            )

        embed = base_embed("🏆 STAFF ACTIVITY LEADERBOARD")

        medals = ["🥇", "🥈", "🥉"]

        desc = ""

        for i, (user_id, actions) in enumerate(rows, start=1):
            member = ctx.guild.get_member(user_id)

            name = member.mention if member else f"`User {user_id}`"
            icon = medals[i - 1] if i <= 3 else f"`#{i}`"

            desc += f"{icon} {name} • **{actions} actions**\n"

        embed.description = desc

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
