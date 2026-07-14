import asyncio

import config


async def send_movie(client, chat_id: int, message_id: int) -> bool:

    try:
        # بررسی وجود پیام
        msg = await client.get_messages(
            config.MOVIE_CHANNEL,
            message_id
        )

        # اگر پیام وجود نداشت
        if getattr(msg, "empty", False):
            return False

        # ارسال فایل
        sent = await client.copy_message(
            chat_id=chat_id,
            from_chat_id=config.MOVIE_CHANNEL,
            message_id=message_id
        )

        # پیام موفقیت
        await client.send_message(
            chat_id,
            f"""✅ فایل با موفقیت برای شما ارسال شد.

⏳ این فایل تا {config.AUTO_DELETE_TIME} ثانیه دیگر به‌صورت خودکار حذف خواهد شد.

📌 لطفاً برای جلوگیری از حذف، آن را در Saved Messages خود ذخیره کنید."""
        )

        # حذف خودکار فایل
        async def delete_later():

            await asyncio.sleep(config.AUTO_DELETE_TIME)

            try:
                await client.delete_messages(
                    chat_id=chat_id,
                    message_ids=sent.id
                )

            except Exception as e:
                print(f"[DELETE ERROR] {e}")

        asyncio.create_task(delete_later())

        return True

    except Exception as e:
        print(f"[SEND MOVIE ERROR] {e}")
        return False