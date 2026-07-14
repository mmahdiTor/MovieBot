from pyrogram import Client, filters

import config


# ادمین‌هایی که منتظر دریافت پیام ارسال همگانی هستند
waiting_broadcast = set()


@Client.on_message(filters.regex("^📢 ارسال همگانی$"))
async def broadcast_start(client, message):

    if message.from_user.id not in config.ADMINS:
        return

    waiting_broadcast.add(message.from_user.id)

    await message.reply_text(
        "📩 پیام مورد نظر برای ارسال همگانی را بفرستید."
    )

@Client.on_message(filters.private,filters.chat(config.ADMINS))
async def broadcast_handler(client, message):

    user_id = message.from_user.id

    # فقط ادمین‌ها
    if user_id not in config.ADMINS:
        return

    # اگر منتظر پیام همگانی نیست
    if user_id not in waiting_broadcast:
        return

    # حذف حالت انتظار
    waiting_broadcast.remove(user_id)


    db = client.db

    users = db.get_users()

    if not users:
        return await message.reply_text(
            "❌ هیچ کاربری در دیتابیس وجود ندارد."
        )


    success = 0
    failed = 0


    status = await message.reply_text(
        "📢 شروع ارسال همگانی..."
    )


    for user in users:

        user_id = user[0]

        try:

            await client.copy_message(
                chat_id=user_id,
                from_chat_id=message.chat.id,
                message_id=message.id
            )

            success += 1


        except Exception as e:

            print(
                f"Broadcast Error ({user_id}): {e}"
            )

            failed += 1


    await status.edit_text(
        f"""
📢 ارسال همگانی تمام شد

✅ موفق: {success}

❌ ناموفق: {failed}
"""
    )