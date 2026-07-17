from pyrogram import Client, filters

from force_sub import check_force_sub
from services.sender import send_movie
from plugins.encode import simple_decode


@Client.on_callback_query(filters.regex("^check_join$"))
async def check_join(client, callback):

    db = client.db
    user = callback.from_user

    is_subscribed = await check_force_sub(client, user.id)

    if not is_subscribed:

        return await callback.answer(
            "❌ هنوز عضو کانال‌ها نیستی",
            show_alert=True
        )

    try:
        await callback.message.delete()
    except:
        pass

    start_param = db.get_start_param(user.id)

    if start_param:

        message_ids = simple_decode(start_param)

        db.clear_start_param(user.id)

        if not message_ids:
            return await callback.message.reply_text(
                "❌ لینک نامعتبر است."
            )

        not_found = []

        for message_id in message_ids:

            ok = await send_movie(
                client,
                callback.message.chat.id,
                message_id
            )

            if not ok:
                not_found.append(str(message_id))

        if not_found:

            return await callback.message.reply_text(
                "❌ فایل(های) زیر پیدا نشد:\n\n"
                + "\n".join(not_found)
            )

        return await callback.answer("✅ فایل‌ها ارسال شدند")

    await callback.message.reply_text(
        f"👋 خوش اومدی {user.mention}"
    )

    await callback.answer("✅ عضویت تایید شد")