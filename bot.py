# bot.py

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import config
from database import add_user, get_all_user_ids

ADMINS = config.ADMIN if isinstance(config.ADMIN, (list, tuple)) else [config.ADMIN]

app = Client(
    "wolverine-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)


# /start command
@app.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    user_id = message.from_user.id
    add_user(user_id)
    await message.reply_text("👋 Welcome! आप इस bot से जुड़े रहेंगे।")


# /broadcast command
@app.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_handler(client, message):
    user_ids = get_all_user_ids()
    if not user_ids:
        await message.reply_text("❌ कोई भी user database में नहीं मिला।")
        return

    sent = 0
    failed = 0

    # अगर admin ने किसी message पर reply करके broadcast किया है (media भी भेजेगा)
    if message.reply_to_message:
        target_msg = message.reply_to_message
        for uid in user_ids:
            try:
                await client.forward_messages(uid, message.chat.id, target_msg.id)
                sent += 1
                await asyncio.sleep(0.05)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await client.forward_messages(uid, message.chat.id, target_msg.id)
                    sent += 1
                except Exception:
                    failed += 1
            except Exception:
                failed += 1
        await message.reply_text(f"📢 Broadcast पूरा हुआ!\n✅ Sent: {sent}\n🚫 Failed: {failed}")
        return

    # अगर सिर्फ text लिखा गया है
    if len(message.command) < 2:
        await message.reply_text("Usage: `/broadcast आपका मेसेज` या फिर किसी message पर reply करके `/broadcast` चलाओ।")
        return

    text = message.text.split(None, 1)[1]
    for uid in user_ids:
        try:
            await client.send_message(uid, text)
            sent += 1
            await asyncio.sleep(0.05)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.send_message(uid, text)
                sent += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1

    await message.reply_text(f"📢 Broadcast पूरा हुआ!\n✅ Sent: {sent}\n🚫 Failed: {failed}")


print("🤖 Wolverine Bot started...")
app.run()
