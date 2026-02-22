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


from discord.ext import commands
import aiosqlite

from config import ROLES, OWNER_ID, DB_PATH
from cogs.ui_theme import base_embed, error_embed


# STAFF CHECK DECORATOR
def is_staff():
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID:
            return True

        user_role_ids = {role.id for role in ctx.author.roles}

        staff_role_ids = {
            ROLES["lead_admin"],
            ROLES["admin"],
            ROLES["mod"],
            ROLES["main_staff"],
            ROLES["business_staff"],
            ROLES["staff"]
        }

        return bool(user_role_ids & staff_role_ids)

    return commands.check(predicate)

# 👁️ STAFF COG
class StaffCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔍 DEBUG ROLE VIEW
    @commands.command()
    async def myroles(self, ctx):
        roles = [role.id for role in ctx.author.roles]
        await ctx.send(f"Your role IDs: {roles}")

    # 📊 STOCK COMMAND
    @commands.command()
    @is_staff()
    async def stock(self, ctx):
        async with aiosqlite.connect(DB_PATH) as db:
            rows = await (await db.execute(
                "SELECT item, quantity FROM stock"
            )).fetchall()

        stock_text = "\n".join(
            [f"**{item}** → `{qty}`" for item, qty in rows]
        )

        embed = base_embed("📊 CURRENT STORAGE STOCK", stock_text)

        await ctx.send(embed=embed)

    # ❌ PERMISSION ERROR HANDLER
    @stock.error
    async def stock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=error_embed("You are not authorized to use this command."))


async def setup(bot):
    await bot.add_cog(StaffCheck(bot))
