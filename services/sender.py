from pyrogram import Client

import config


async def send_movie(
    client: Client,
    chat_id: int,
    message_ids: list[int]
) -> dict:


    sent_messages = []
    not_found = []


    try:

        messages = []


        # گرفتن پیام‌ها
        for message_id in message_ids:

            try:

                msg = await client.get_messages(
                    config.MOVIE_CHANNEL,
                    message_id
                )


                if getattr(msg, "empty", False):

                    not_found.append(
                        str(message_id)
                    )

                    continue


                messages.append(msg)


            except Exception as e:

                print(
                    f"[GET MESSAGE ERROR] {e}"
                )

                not_found.append(
                    str(message_id)
                )


        if not messages:

            return {
                "sent": [],
                "not_found": not_found
            }



        # بررسی Media Group

        media_group_ids = set(
            msg.media_group_id
            for msg in messages
            if msg.media_group_id
        )


        # اگر همه یک آلبوم باشند
        if len(media_group_ids) == 1:


            try:

                copied = await client.copy_media_group(
                    chat_id,
                    config.MOVIE_CHANNEL,
                    messages[0].id
                )


                for msg in copied:

                    sent_messages.append(
                        msg.id
                    )


            except Exception as e:

                print(
                    f"[MEDIA GROUP ERROR] {e}"
                )


                # fallback
                for msg in messages:

                    sent = await msg.copy(
                        chat_id
                    )

                    sent_messages.append(
                        sent.id
                    )


        else:


            # فایل‌های معمولی
            for msg in messages:

                sent = await msg.copy(
                    chat_id
                )

                sent_messages.append(
                    sent.id
                )



        return {
            "sent": sent_messages,
            "not_found": not_found
        }



    except Exception as e:

        print(
            f"[SEND MOVIE ERROR] {e}"
        )

        return {
            "sent": [],
            "not_found": message_ids
        }