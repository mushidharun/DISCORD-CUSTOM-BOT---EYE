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

from typing import Dict
import discord

# channel_id -> message_id
panel_messages: Dict[int, int] = {}


async def replace_panel(ctx, embed: discord.Embed, view: discord.ui.View):
    channel = ctx.channel

    # 🔎 Try to delete previous panel
    old_message_id = panel_messages.get(channel.id)

    if old_message_id:
        try:
            old_msg = await channel.fetch_message(old_message_id)
            await old_msg.delete()
        except discord.NotFound:
            pass
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass

    # 📩 Send new panel
    new_msg = await channel.send(embed=embed, view=view)

    # 💾 Save new panel message ID
    panel_messages[channel.id] = new_msg.id
