from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

import config

# وضعیت ادمین
admin_state = {}


# ===================== پنل =====================

@Client.on_message(filters.command("admin"))
async def admin_panel(client, message):

    if message.from_user.id not in config.ADMINS:
        return

    keyboard = ReplyKeyboardMarkup(
        [
            ["📤 آپلود فیلم"],
            ["📢 ارسال همگانی", "👥 تعداد کاربران"],
            ["🚫 بن کاربر", "✅ آنبن کاربر"],
            ["❌ بستن پنل"]
        ],
        resize_keyboard=True
    )

    await message.reply_text(
        "⚙️ پنل مدیریت",
        reply_markup=keyboard
    )


# ===================== بستن پنل =====================

@Client.on_message(filters.regex("^❌ بستن پنل$"))
async def close_panel(client, message):

    if message.from_user.id not in config.ADMINS:
        return

    admin_state.pop(message.from_user.id, None)

    await message.reply_text(
        "✅ پنل بسته شد.",
        reply_markup=ReplyKeyboardRemove()
    )


# ===================== تعداد کاربران =====================

@Client.on_message(filters.regex("^👥 تعداد کاربران$"))
async def users_count(client, message):

    if message.from_user.id not in config.ADMINS:
        return

    count = client.db.users_count()

    await message.reply_text(
        f"👥 تعداد کاربران ربات:\n\n{count}"
    )


# ===================== شروع آپلود =====================

@Client.on_message(filters.regex("^📤 آپلود فیلم$"))
async def upload_start(client, message):

    if message.from_user.id not in config.ADMINS:
        return

    admin_state[message.from_user.id] = "upload"

    await message.reply_text(
        "🎬 ویدیو را ارسال کنید."
    )


# ===================== دریافت ویدیو =====================
@Client.on_message(filters.video)
async def upload_video(client, message):

    if message.from_user.id not in config.ADMINS:
        return

    if admin_state.get(message.from_user.id) != "upload":
        print("s")
        return

    admin_state.pop(message.from_user.id)

    sent = await client.send_video(
        chat_id=config.MOVIE_CHANNEL,
        video=message.video.file_id,
        caption="""
در کانال ما جویین باشید :
https://t.me/Ccuckkold
"""
    )

    bot_username = (await client.get_me()).username

    await message.reply_text(
        f"""✅ ویدیو ذخیره شد.

🆔 Message ID: `{sent.id}`

🔗 لینک:

https://t.me/{bot_username}?start={sent.id}
"""
    )
