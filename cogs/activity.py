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

from config import XP_PER_ACTION, LEVEL_UP_BASE, DB_PATH


async def add_activity(user_id: int, xp_gain: int = None):
    xp_gain = xp_gain or XP_PER_ACTION

    async with aiosqlite.connect(DB_PATH) as db:

        # ---------- ACTIVITY UPSERT ----------
        await db.execute("""
            INSERT INTO staff_activity (user_id, actions)
            VALUES (?, 1)
            ON CONFLICT(user_id)
            DO UPDATE SET actions = actions + 1
        """, (user_id,))

        # ---------- FETCH LEVEL DATA ----------
        row = await (
            await db.execute(
                "SELECT xp, level FROM levels WHERE user_id = ?",
                (user_id,)
            )
        ).fetchone()

        if row:
            xp, level = row
        else:
            xp, level = 0, 1

        # ---------- ADD XP ----------
        xp += xp_gain
        leveled_up = False

        xp_needed = level * LEVEL_UP_BASE

        # ---------- LEVEL UP LOOP ----------
        while xp >= xp_needed:
            xp -= xp_needed
            level += 1
            leveled_up = True
            xp_needed = level * LEVEL_UP_BASE

        # ---------- UPSERT LEVEL ----------
        await db.execute("""
            INSERT INTO levels (user_id, xp, level)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET xp = excluded.xp,
                          level = excluded.level
        """, (user_id, xp, level))

        await db.commit()

    return leveled_up, level, xp
