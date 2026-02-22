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

from cogs.staff_check import is_staff
from cogs.activity import add_activity
from cogs.ui_theme import base_embed, success_embed, error_embed
from cogs.panel_manager import replace_panel
from config import CHANNELS


class OrderModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="🧾 NEW ORDER")

        self.item = discord.ui.TextInput(label="Item", required=True)
        self.qty = discord.ui.TextInput(label="Quantity", required=True)
        self.customer = discord.ui.TextInput(label="Customer Name", required=True)

        self.add_item(self.item)
        self.add_item(self.qty)
        self.add_item(self.customer)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        user = interaction.user

        try:
            qty = int(self.qty.value)
            if qty <= 0:
                raise ValueError
        except:
            return await interaction.followup.send(
                embed=error_embed("Invalid quantity"), ephemeral=True
            )

        await add_activity(user.id)

        embed = base_embed("🧾 NEW ORDER RECEIVED")
        embed.add_field(name="👤 Staff", value=user.mention)
        embed.add_field(name="📦 Item", value=f"`{self.item.value}`")
        embed.add_field(name="🔢 Quantity", value=f"`{qty}`")
        embed.add_field(name="🧑 Customer", value=f"`{self.customer.value}`")

        channel = interaction.guild.get_channel(CHANNELS["orders"])
        await channel.send(embed=embed)

        await interaction.followup.send(
            embed=success_embed("Order logged successfully"), ephemeral=True
        )


class OrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Order", style=discord.ButtonStyle.green, custom_id="order_create")
    async def create_order(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(OrderModal())


class OrdersUI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(OrderView())

    @commands.command()
    @is_staff()
    async def orders(self, ctx):
        embed = base_embed(
            "🧾 BANGALORE AQUA&CO. • ORDER PANEL",
            "Create and manage business orders using the button below."
        )
        await replace_panel(ctx, embed, OrderView())


async def setup(bot):
    await bot.add_cog(OrdersUI(bot))