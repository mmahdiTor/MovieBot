from datetime import datetime

from pyrogram import Client, filters

from force_sub import check_force_sub
from keyboards.inline import force_sub_keyboard
from services.sender import send_movie


@Client.on_message(filters.command("start"))
async def start(client, message):

    db = client.db
    user = message.from_user

    db.add_user(user)

    if db.is_banned(user.id):
        return await message.reply_text("⛔ شما بن هستید")

    # گرفتن پارامتر
    start_param = None

    if len(message.command) > 1:
        start_param = message.command[1]

        # ذخیره در دیتابیس
        db.save_start_param(user.id, start_param)

    # بررسی عضویت
    is_subscribed = await check_force_sub(client, user.id)

    if not is_subscribed:

        return await message.reply_text(
            "❌ برای استفاده از ربات ابتدا در کانال‌ها عضو شوید.",
            reply_markup=force_sub_keyboard()
        )

    # ارسال فایل
    if start_param:

        ok = await send_movie(
            client,
            message.chat.id,
            int(start_param)
        )

        db.clear_start_param(user.id)

        if not ok:
            return await message.reply_text("❌ فایل پیدا نشد")

        return

    # خوش آمدگویی
    text = f"""
👋 سلام {user.mention}

به ربات خوش اومدی ❤️

📅 {datetime.now().strftime('%Y/%m/%d')}
🕒 {datetime.now().strftime('%H:%M')}
"""

    await message.reply_text(text)