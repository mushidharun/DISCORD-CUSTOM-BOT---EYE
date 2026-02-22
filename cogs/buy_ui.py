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
from config import CHANNELS, DB_PATH

ITEM = "PURE IRON"


class BuyModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="🧾 BUY • PURE IRON")

        self.qty = discord.ui.TextInput(label="Quantity", required=True)
        self.price = discord.ui.TextInput(label="Total Price", required=True)

        self.add_item(self.qty)
        self.add_item(self.price)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        user = interaction.user

        try:
            qty = int(self.qty.value)
            if qty <= 0:
                raise ValueError
            price = self.price.value
        except:
            return await interaction.followup.send(
                embed=error_embed("Invalid input"), ephemeral=True
            )

        async with aiosqlite.connect(DB_PATH) as db:
            current = (
                await (
                    await db.execute(
                        "SELECT quantity FROM stock WHERE item = ?",
                        (ITEM,)
                    )
                ).fetchone()
            )[0]

            new_qty = current + qty

            await db.execute(
                "UPDATE stock SET quantity = ? WHERE item = ?",
                (new_qty, ITEM)
            )

            await db.execute(
                """INSERT INTO profit (type, item, quantity, price, staff_id)
                   VALUES (?, ?, ?, ?, ?)""",
                ("buy", ITEM, qty, price, user.id)
            )

            await db.commit()

        await add_activity(user.id)

        log_channel = interaction.guild.get_channel(CHANNELS["buying"])

        log_embed = base_embed("🧾 BUYING BILL • PURE IRON")
        log_embed.add_field(name="👤 Staff", value=user.mention)
        log_embed.add_field(name="🔢 Quantity", value=f"`{qty}`")
        log_embed.add_field(name="💰 Price", value=f"`{price}`")
        log_embed.add_field(name="📊 Stock After", value=f"`{new_qty}`")

        await log_channel.send(embed=log_embed)

        await interaction.followup.send(
            embed=success_embed("Buying log recorded"), ephemeral=True
        )


class BuyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Buy PURE IRON", style=discord.ButtonStyle.green, custom_id="buy_pure_iron")
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BuyModal())


class BuyUI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(BuyView())

    @commands.command()
    @is_staff()
    async def buy(self, ctx):
        embed = base_embed(
            "🧾 BANGALORE AQUA&CO. • BUYING PANEL",
            "Purchase PURE IRON and add it to storage."
        )
        await replace_panel(ctx, embed, BuyView())


async def setup(bot):
    await bot.add_cog(BuyUI(bot))