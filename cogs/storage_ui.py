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


class QuantityModal(discord.ui.Modal):
    def __init__(self, action, item):
        super().__init__(title=f"{action} • {item}")
        self.action = action
        self.item = item

        self.qty = discord.ui.TextInput(label="Enter Quantity", required=True)
        self.add_item(self.qty)

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

        async with aiosqlite.connect(DB_PATH) as db:
            current = (
                await (
                    await db.execute(
                        "SELECT quantity FROM stock WHERE item = ?",
                        (self.item,)
                    )
                ).fetchone()
            )[0]

            if self.action == "Withdraw" and qty > current:
                return await interaction.followup.send(
                    embed=error_embed("Not enough stock"), ephemeral=True
                )

            new_qty = current + qty if self.action == "Deposit" else current - qty

            await db.execute(
                "UPDATE stock SET quantity = ? WHERE item = ?",
                (new_qty, self.item)
            )
            await db.commit()

        await add_activity(user.id)

        log_channel = interaction.guild.get_channel(CHANNELS["storage"])

        log_embed = base_embed(f"📦 STORAGE {self.action.upper()}")
        log_embed.add_field(name="👤 Staff", value=user.mention)
        log_embed.add_field(name="📦 Item", value=f"`{self.item}`")
        log_embed.add_field(name="🔢 Quantity", value=f"`{qty}`")
        log_embed.add_field(name="📊 Stock After", value=f"`{new_qty}`")

        await log_channel.send(embed=log_embed)

        await interaction.followup.send(
            embed=success_embed(f"{self.action} successful"), ephemeral=True
        )


class ItemSelect(discord.ui.Select):
    def __init__(self, action):
        self.action = action
        options = [discord.SelectOption(label=item) for item in ITEMS]
        super().__init__(placeholder="Select item", options=options, custom_id=f"storage_{action}")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(
            QuantityModal(self.action, self.values[0])
        )


class StorageView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Deposit", style=discord.ButtonStyle.green, emoji="📥", custom_id="storage_deposit")
    async def deposit(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = discord.ui.View(timeout=60)
        view.add_item(ItemSelect("Deposit"))
        await interaction.response.send_message(embed=base_embed("📥 Select item to deposit"), view=view, ephemeral=True)

    @discord.ui.button(label="Withdraw", style=discord.ButtonStyle.red, emoji="📤", custom_id="storage_withdraw")
    async def withdraw(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = discord.ui.View(timeout=60)
        view.add_item(ItemSelect("Withdraw"))
        await interaction.response.send_message(embed=base_embed("📤 Select item to withdraw"), view=view, ephemeral=True)

    @discord.ui.button(label="View Stock", style=discord.ButtonStyle.blurple, emoji="📊", custom_id="storage_view")
    async def stock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        async with aiosqlite.connect(DB_PATH) as db:
            rows = await (
                await db.execute("SELECT item, quantity FROM stock")
            ).fetchall()

        embed = base_embed("📊 CURRENT STORAGE STOCK")
        embed.description = "\n".join([f"**{item}** → `{qty}`" for item, qty in rows])

        await interaction.followup.send(embed=embed, ephemeral=True)


class StorageUI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(StorageView())

    @commands.command()
    @is_staff()
    async def storage(self, ctx):
        embed = base_embed(
            "📦 BANGALORE AQUA&CO. • STORAGE PANEL",
            "Use the buttons below to manage storage."
        )
        await replace_panel(ctx, embed, StorageView())


async def setup(bot):
    await bot.add_cog(StorageUI(bot))