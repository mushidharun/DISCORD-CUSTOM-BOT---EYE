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

import os

TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID: int = 0

DB_PATH: str = "database.db"

ROLES: dict = {
    "lead_admin": 0,
    "admin": 0,
    "mod": 0,
    "main_staff": 0,
    "business_staff": 0,
    "staff": 0,
    "member": 0
}

CHANNELS: dict = {
    "buying": 0,
    "selling": 0,
    "storage": 0,
    "grinding": 0,
    "orders": 0
}

BACKUP_CHANNEL: int = 0
AUTO_BACKUP_INTERVAL_MIN: int = 5

ITEMS: list = [
    "RAW WATER",
    "NORMAL WATER",
    "PURE WATER",
    "PURE IRON"
]

XP_PER_ACTION: int = 5
LEVEL_UP_BASE: int = 100

DB_TIMEOUT: int = 30