from datetime import datetime
import asyncio

from pyrogram import Client, filters

import config

from force_sub import check_force_sub
from keyboards.inline import force_sub_keyboard
from services.sender import send_movie
from plugins.encode import simple_decode


@Client.on_message(filters.command("start"))
async def start(client, message):

    db = client.db
    user = message.from_user

    db.add_user(user)

    if db.is_banned(user.id):
        return await message.reply_text(
            "⛔ شما بن هستید"
        )


    # گرفتن پارامتر start
    start_param = None

    if len(message.command) > 1:

        start_param = message.command[1]

        # ذخیره پارامتر
        db.save_start_param(
            user.id,
            start_param
        )


    # بررسی عضویت اجباری
    is_subscribed = await check_force_sub(
        client,
        user.id
    )

    if not is_subscribed:

        return await message.reply_text(
            "❌ برای استفاده از ربات ابتدا در کانال‌ها عضو شوید.",
            reply_markup=force_sub_keyboard()
        )


    # ارسال فایل‌ها
    if start_param:

        message_ids = simple_decode(
            start_param
        )


        db.clear_start_param(
            user.id
        )


        if not message_ids:

            return await message.reply_text(
                "❌ لینک نامعتبر است."
            )


        result = await send_movie(
            client,
            message.chat.id,
            message_ids
        )


        # فایل‌های پیدا نشده
        if result["not_found"]:

            await message.reply_text(
                "❌ فایل‌های زیر پیدا نشد:\n\n"
                +
                "\n".join(
                    result["not_found"]
                )
            )


        # فایل ارسال شده
        if result["sent"]:


            await client.send_message(
                message.chat.id,
                f"""✅ فایل‌ها با موفقیت برای شما ارسال شد.

⏳ این فایل‌ها تا {config.AUTO_DELETE_TIME} ثانیه دیگر به‌صورت خودکار حذف خواهند شد.

📌 لطفاً برای جلوگیری از حذف، آن‌ها را در Saved Messages خود ذخیره کنید."""
            )


            # حذف خودکار همه فایل‌ها با هم
            async def delete_later():

                await asyncio.sleep(
                    config.AUTO_DELETE_TIME
                )

                try:

                    await client.delete_messages(
                        chat_id=message.chat.id,
                        message_ids=result["sent"]
                    )

                except Exception as e:

                    print(
                        f"[DELETE ERROR] {e}"
                    )


            asyncio.create_task(
                delete_later()
            )


        return


    # پیام خوش آمدگویی

    text = f"""
👋 سلام {user.mention}

به ربات خوش اومدی ❤️

📅 {datetime.now().strftime('%Y/%m/%d')}
🕒 {datetime.now().strftime('%H:%M')}
"""


    await message.reply_text(
        text
    )