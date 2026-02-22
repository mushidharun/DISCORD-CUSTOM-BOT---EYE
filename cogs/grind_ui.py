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


class GrindModal(discord.ui.Modal):
    def __init__(self, item):
        super().__init__(title=f"⚙️ GRIND • {item}")
        self.item = item

        self.qty = discord.ui.TextInput(label="Quantity Produced", required=True)
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

            new_qty = current + qty

            await db.execute(
                "UPDATE stock SET quantity = ? WHERE item = ?",
                (new_qty, self.item)
            )
            await db.commit()

        await add_activity(user.id)

        log_channel = interaction.guild.get_channel(CHANNELS["grinding"])

        embed = base_embed("⚙️ GRINDING LOG")
        embed.add_field(name="👤 Staff", value=user.mention)
        embed.add_field(name="📦 Item Produced", value=f"`{self.item}`")
        embed.add_field(name="🔢 Quantity", value=f"`{qty}`")
        embed.add_field(name="📊 Stock After", value=f"`{new_qty}`")

        await log_channel.send(embed=embed)

        await interaction.followup.send(
            embed=success_embed("Grinding log recorded"), ephemeral=True
        )


class GrindSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=item) for item in ITEMS]
        super().__init__(placeholder="Select item produced", options=options, custom_id="grind_select")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(GrindModal(self.values[0]))


class GrindView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GrindSelect())


class GrindUI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(GrindView())

    @commands.command()
    @is_staff()
    async def grind(self, ctx):
        embed = base_embed(
            "⚙️ BANGALORE AQUA&CO. • GRINDING PANEL",
            "Select the item you produced."
        )
        await replace_panel(ctx, embed, GrindView())


async def setup(bot):
    await bot.add_cog(GrindUI(bot))