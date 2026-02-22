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


import aiosqlite
from discord.ext import commands

from config import ITEMS, DB_PATH


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.setup_db())

    async def setup_db(self):
        await self.bot.wait_until_ready()

        async with aiosqlite.connect(DB_PATH) as db:

            # ⚡ PERFORMANCE PRAGMAS
            await db.execute("PRAGMA journal_mode=WAL;")
            await db.execute("PRAGMA synchronous=NORMAL;")
            await db.execute("PRAGMA foreign_keys=ON;")
            await db.execute("PRAGMA busy_timeout=30000;")

            # ---------- STOCK TABLE ----------
            await db.execute("""
                CREATE TABLE IF NOT EXISTS stock (
                    item TEXT PRIMARY KEY,
                    quantity INTEGER NOT NULL DEFAULT 0
                )
            """)

            # ---------- STAFF ACTIVITY ----------
            await db.execute("""
                CREATE TABLE IF NOT EXISTS staff_activity (
                    user_id INTEGER PRIMARY KEY,
                    actions INTEGER NOT NULL DEFAULT 0
                )
            """)

            # ---------- LEVEL SYSTEM ----------
            await db.execute("""
                CREATE TABLE IF NOT EXISTS levels (
                    user_id INTEGER PRIMARY KEY,
                    xp INTEGER NOT NULL DEFAULT 0,
                    level INTEGER NOT NULL DEFAULT 1
                )
            """)

            # ---------- PROFIT TABLE ----------
            await db.execute("""
                CREATE TABLE IF NOT EXISTS profit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    item TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price TEXT NOT NULL,
                    staff_id INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # ---------- INDEXES FOR PERFORMANCE ----------
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_activity_actions ON staff_activity(actions DESC)"
            )

            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_levels_level ON levels(level DESC)"
            )

            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_profit_staff ON profit(staff_id)"
            )

            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_profit_type ON profit(type)"
            )

            # ---------- AUTO INSERT ITEMS ----------
            for item in ITEMS:
                await db.execute(
                    "INSERT OR IGNORE INTO stock (item, quantity) VALUES (?, ?)",
                    (item, 0)
                )

            await db.commit()

        print("===================================")
        print("Database ready 👁️")
        print("WAL mode enabled ⚡")
        print("Stock + Activity + Levels + Profit")
        print("Indexes loaded 🚀")
        print("===================================")


async def setup(bot):
    await bot.add_cog(Database(bot))
