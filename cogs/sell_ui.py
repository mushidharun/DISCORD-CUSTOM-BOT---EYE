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

from cogs.staff_check import is_staff
from cogs.activity import add_activity
from cogs.ui_theme import base_embed, success_embed, error_embed
from cogs.panel_manager import replace_panel
from config import CHANNELS, ITEMS, DB_PATH


class SellModal(discord.ui.Modal):
    def __init__(self, item):
        super().__init__(title=f"💰 SELL • {item}")
        self.item = item

        self.qty = discord.ui.TextInput(label="Quantity", required=True)
        self.price = discord.ui.TextInput(label="Total Price", required=True)
        self.sold_to = discord.ui.TextInput(label="Sold To", required=True)

        self.add_item(self.qty)
        self.add_item(self.price)
        self.add_item(self.sold_to)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        user = interaction.user

        try:
            qty = int(self.qty.value)
            if qty <= 0:
                raise ValueError
            price = self.price.value
            sold_to = self.sold_to.value
        except:
            return await interaction.followup.send(
                embed=error_embed("Invalid input"), ephemeral=True
            )

        async with aiosqlite.connect(DB_PATH) as db:
            current = (
                await (
                    await db.execute(
                        "SELECT quantity FROM stock WHERE item = ?",
                        (self.item,)
                    )
                ).fetchone()
            )[0]

            if qty > current:
                return await interaction.followup.send(
                    embed=error_embed("Not enough stock"), ephemeral=True
                )

            new_qty = current - qty

            await db.execute(
                "UPDATE stock SET quantity = ? WHERE item = ?",
                (new_qty, self.item)
            )

            await db.execute(
                """INSERT INTO profit (type, item, quantity, price, staff_id)
                   VALUES (?, ?, ?, ?, ?)""",
                ("sell", self.item, qty, price, user.id)
            )

            await db.commit()

        await add_activity(user.id)

        log_channel = interaction.guild.get_channel(CHANNELS["selling"])

        embed = base_embed("💰 SELLING BILL")
        embed.add_field(name="👤 Staff", value=user.mention)
        embed.add_field(name="📦 Item", value=f"`{self.item}`")
        embed.add_field(name="🔢 Quantity", value=f"`{qty}`")
        embed.add_field(name="💰 Price", value=f"`{price}`")
        embed.add_field(name="🧑 Sold To", value=f"`{sold_to}`")
        embed.add_field(name="📊 Stock After", value=f"`{new_qty}`")

        await log_channel.send(embed=embed)

        await interaction.followup.send(
            embed=success_embed("Selling log recorded"), ephemeral=True
        )


class SellSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=item) for item in ITEMS]
        super().__init__(placeholder="Select item to sell", options=options, custom_id="sell_select")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SellModal(self.values[0]))


class SellView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SellSelect())


class SellUI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(SellView())

    @commands.command()
    @is_staff()
    async def sell(self, ctx):
        embed = base_embed(
            "💰 BANGALORE AQUA&CO. • SELLING PANEL",
            "Select an item to create a selling bill."
        )
        await replace_panel(ctx, embed, SellView())


async def setup(bot):
    await bot.add_cog(SellUI(bot))