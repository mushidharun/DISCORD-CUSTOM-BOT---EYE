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
import aiosqlite

from config import BACKUP_CHANNEL, DB_PATH, AUTO_BACKUP_INTERVAL_MIN
from cogs.ui_theme import base_embed

# guild_id -> message_id
last_backup_message = {}


class AutoBackup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not self.backup_loop.is_running():
            self.backup_loop.start()

    def cog_unload(self):
        self.backup_loop.cancel()

    # ⏱️ AUTO BACKUP LOOP
    @tasks.loop(minutes=AUTO_BACKUP_INTERVAL_MIN)
    async def backup_loop(self):
        await self.bot.wait_until_ready()

        async with aiosqlite.connect(DB_PATH) as db:
            # 📦 STOCK
            stock_rows = await (
                await db.execute("SELECT item, quantity FROM stock")
            ).fetchall()

            total_items = sum(qty for _, qty in stock_rows)

            # 💰 PROFIT
            profit_rows = await (
                await db.execute("SELECT type, price FROM profit")
            ).fetchall()

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

        # 🎨 PROFIT STATUS
        if net_profit > 0:
            profit_status = "🟢 Profit"
        elif net_profit < 0:
            profit_status = "🔴 Loss"
        else:
            profit_status = "🟡 Break-even"

        embed = base_embed("⏱️ AUTO BACKUP • BUSINESS SNAPSHOT")

        if stock_rows:
            stock_text = "\n".join(
                [f"**{item}** → `{qty}`" for item, qty in stock_rows]
            )
        else:
            stock_text = "No stock data."

        embed.add_field(name="📦 Storage", value=stock_text, inline=False)
        embed.add_field(name="📊 Total Items", value=f"`{total_items}`")
        embed.add_field(name="💸 Total Buying", value=f"`{total_buy}`")
        embed.add_field(name="💰 Total Selling", value=f"`{total_sell}`")
        embed.add_field(
            name=f"📈 Net Profit • {profit_status}",
            value=f"`{net_profit}`",
            inline=False
        )

        embed.set_footer(text="Auto backup • Live dashboard 👁️")

        # 🔁 SEND ONE MESSAGE PER GUILD
        for guild in self.bot.guilds:
            channel = guild.get_channel(BACKUP_CHANNEL)
            if not channel:
                continue

            try:
                # Delete previous backup message safely
                old_msg_id = last_backup_message.get(guild.id)

                if old_msg_id:
                    try:
                        old_msg = await channel.fetch_message(old_msg_id)
                        await old_msg.delete()
                    except:
                        pass

                # Send new backup
                new_msg = await channel.send(embed=embed)

                # Store new message ID
                last_backup_message[guild.id] = new_msg.id

            except discord.Forbidden:
                print(f"[AutoBackup] Missing permissions in {guild.name}")
            except discord.HTTPException as e:
                print(f"[AutoBackup] HTTP error in {guild.name}: {e}")


async def setup(bot):
    await bot.add_cog(AutoBackup(bot))
