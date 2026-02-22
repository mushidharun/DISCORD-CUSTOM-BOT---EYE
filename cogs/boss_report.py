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

from config import OWNER_ID, DB_PATH
from cogs.ui_theme import boss_embed, error_embed


class BossReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def report(self, ctx):
        # 👑 Boss only
        if ctx.author.id != OWNER_ID:
            return await ctx.send(
                embed=error_embed(
                    "Access denied",
                    "Only the Business Boss can use this command 👑"
                )
            )

        async with aiosqlite.connect(DB_PATH) as db:

            # 📦 STOCK DATA
            stock_rows = await (
                await db.execute("SELECT item, quantity FROM stock")
            ).fetchall()

            total_items = sum(qty for _, qty in stock_rows)

            # 💰 PROFIT DATA
            profit_rows = await (
                await db.execute("SELECT type, price FROM profit")
            ).fetchall()

        # 💰 CALCULATE PROFITS SAFELY
        total_buy = 0
        total_sell = 0

        for type_, price in profit_rows:
            try:
                value = int(price)
            except:
                value = 0

            if type_ == "buy":
                total_buy += value
            elif type_ == "sell":
                total_sell += value

        net_profit = total_sell - total_buy

        # 🎨 PROFIT COLOR INDICATOR
        if net_profit > 0:
            profit_status = "🟢 Profit"
        elif net_profit < 0:
            profit_status = "🔴 Loss"
        else:
            profit_status = "🟡 Break-even"

        # 👑 EMBED
        embed = boss_embed("👑 BANGALORE AQUA&CO. • EXECUTIVE REPORT")

        # 📦 STORAGE SECTION
        if stock_rows:
            stock_text = "\n".join(
                [f"**{item}** → `{qty}`" for item, qty in stock_rows]
            )
        else:
            stock_text = "No stock data available."

        embed.add_field(
            name="📦 Storage Overview",
            value=stock_text,
            inline=False
        )

        embed.add_field(
            name="📊 Total Items in Storage",
            value=f"`{total_items}`"
        )

        # 💰 PROFIT SECTION
        embed.add_field(name="💸 Total Buying", value=f"`{total_buy}`")
        embed.add_field(name="💰 Total Selling", value=f"`{total_sell}`")
        embed.add_field(
            name=f"📈 Net Profit • {profit_status}",
            value=f"`{net_profit}`",
            inline=False
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(BossReport(bot))
