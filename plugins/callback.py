from pyrogram import Client, filters

from force_sub import check_force_sub
from services.sender import send_movie


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

        ok = await send_movie(
            client,
            callback.message.chat.id,
            int(start_param)
        )

        db.clear_start_param(user.id)

        if not ok:
            return await callback.message.reply_text(
                "❌ فایل پیدا نشد"
            )

        return await callback.answer("✅ فایل ارسال شد")

    await callback.message.reply_text(
        f"👋 خوش اومدی {user.mention}"
    )

    await callback.answer("✅ عضویت تایید شد")