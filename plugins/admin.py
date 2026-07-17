import asyncio

from pyrogram import Client, filters
from pyrogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaDocument
)

import config
from plugins.encode import simple_encode


# ===================== وضعیت ها =====================

admin_state = {}

upload_groups = {}


# ===================== پنل =====================

@Client.on_message(filters.command("admin"))
async def admin_panel(client, message):

    if message.from_user.id not in config.ADMINS:
        return

    keyboard = ReplyKeyboardMarkup(
        [
            ["📤 آپلود فیلم", "📦 ساخت لینک"],
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
        f"👥 تعداد کاربران:\n\n{count}"
    )


# ===================== شروع آپلود =====================

@Client.on_message(filters.regex("^📤 آپلود فیلم$"))
async def upload_start(client, message):

    if message.from_user.id not in config.ADMINS:
        return

    admin_state[message.from_user.id] = "upload"

    await message.reply_text(
        "🎬 عکس، ویدیو، فایل یا آلبوم را ارسال کنید."
    )


# ===================== ساخت لینک =====================

@Client.on_message(filters.regex("^📦 ساخت لینک$"))
async def create_link_start(client, message):

    if message.from_user.id not in config.ADMINS:
        return

    admin_state[message.from_user.id] = "link"

    await message.reply_text(
        "📨 Message ID را ارسال کنید.\n\n"
        "مثال:\n"
        "`374`\n\n"
        "یا\n\n"
        "`374-371-500`"
    )


# ===================== ارسال همگانی =====================

@Client.on_message(filters.regex("^📢 ارسال همگانی$"))
async def broadcast_start(client, message):

    if message.from_user.id not in config.ADMINS:
        return

    admin_state[message.from_user.id] = "broadcast"

    await message.reply_text(
        "📩 پیام موردنظر برای ارسال همگانی را ارسال کنید."
    )


# ===================== هندلر متن =====================

@Client.on_message(filters.text & filters.chat(config.ADMINS))
async def admin_text_handler(client, message):

    if message.from_user.id not in config.ADMINS:
        return

    state = admin_state.get(message.from_user.id)

    if not state:
        return


    # ===================== ساخت لینک =====================

    if state == "link":

        admin_state.pop(message.from_user.id)

        ids = message.text.strip()

        encoded = simple_encode(ids)

        bot_username = (await client.get_me()).username

        return await message.reply_text(
            f"""✅ لینک ساخته شد.

🔗 لینک:

https://t.me/{bot_username}?start={encoded}
"""
        )


    # ===================== ارسال همگانی =====================

    if state == "broadcast":

        admin_state.pop(message.from_user.id)

        db = client.db

        users = db.get_users()

        if not users:

            return await message.reply_text(
                "❌ هیچ کاربری وجود ندارد."
            )

        success = 0
        failed = 0

        status = await message.reply_text(
            "📢 شروع ارسال..."
        )

        for user in users:

            try:

                await client.copy_message(
                    chat_id=user[0],
                    from_chat_id=message.chat.id,
                    message_id=message.id
                )

                success += 1

            except Exception as e:

                print(f"Broadcast Error ({user[0]}): {e}")

                failed += 1

        return await status.edit_text(
            f"""
📢 ارسال همگانی تمام شد

✅ موفق: {success}

❌ ناموفق: {failed}
"""
        )


# ===================== دریافت مدیا =====================
# ===================== دریافت مدیا =====================

@Client.on_message(filters.media)
async def upload_media(client, message):

    user_id = message.from_user.id

    if user_id not in config.ADMINS:
        return

    if admin_state.get(user_id) != "upload":
        return

    caption = """در کانال ما جویین باشید :
https://t.me/Zeerrop"""

    # ==========================================
    # Media Group
    # ==========================================

    if message.media_group_id:

        if user_id not in upload_groups:
            upload_groups[user_id] = []

        upload_groups[user_id].append(message)

        await asyncio.sleep(2)

        if user_id not in upload_groups:
            return

        if message.id != upload_groups[user_id][-1].id:
            return

        files = upload_groups.pop(user_id)
        admin_state.pop(user_id, None)

        media = []

        for index, item in enumerate(files):

            cap = caption if index == 0 else None

            if item.photo:

                media.append(
                    InputMediaPhoto(
                        media=item.photo.file_id,
                        caption=cap
                    )
                )

            elif item.video:

                media.append(
                    InputMediaVideo(
                        media=item.video.file_id,
                        caption=cap
                    )
                )

            elif item.document:

                media.append(
                    InputMediaDocument(
                        media=item.document.file_id,
                        caption=cap
                    )
                )

        if not media:
            return await message.reply_text(
                "❌ فایل قابل ذخیره نیست."
            )

        try:

            sent_messages = await client.send_media_group(
                chat_id=config.MOVIE_CHANNEL,
                media=media
            )

        except Exception as e:

            return await message.reply_text(
                f"❌ خطا:\n{e}"
            )

        ids = [str(x.id) for x in sent_messages]

        encoded = simple_encode("-".join(ids))

        bot_username = (await client.get_me()).username

        return await message.reply_text(
            f"""✅ پکیج {len(ids)} فایلی ذخیره شد.

🆔 ID ها

`{' - '.join(ids)}`

🔗 لینک

https://t.me/{bot_username}?start={encoded}
"""
        )

    # ==========================================
    # فایل تکی
    # ==========================================

    admin_state.pop(user_id, None)

    sent = None

    try:

        if message.photo:

            sent = await client.send_photo(
                chat_id=config.MOVIE_CHANNEL,
                photo=message.photo.file_id,
                caption=caption
            )

        elif message.video:

            sent = await client.send_video(
                chat_id=config.MOVIE_CHANNEL,
                video=message.video.file_id,
                caption=caption
            )

        elif message.document:

            sent = await client.send_document(
                chat_id=config.MOVIE_CHANNEL,
                document=message.document.file_id,
                caption=caption
            )

    except Exception as e:

        return await message.reply_text(
            f"❌ خطا:\n{e}"
        )

    if not sent:

        return await message.reply_text(
            "❌ این نوع فایل پشتیبانی نمی‌شود."
        )

    encoded = simple_encode(str(sent.id))

    bot_username = (await client.get_me()).username

    await message.reply_text(
        f"""✅ فایل ذخیره شد.

🆔 Message ID: `{sent.id}`

🔗 لینک

https://t.me/{bot_username}?start={encoded}
"""
    )