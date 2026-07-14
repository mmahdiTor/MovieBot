from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config


def force_sub_keyboard(start_param=None):

    keyboard = []

    for channel in config.FORCE_SUB_CHANNELS:

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📢 {channel.replace('@','')}",
                    url=f"https://t.me/{channel.replace('@','')}"
                )
            ]
        )

    callback = "check_join"

    if start_param:

        callback += f":{start_param}"

    keyboard.append(
        [
            InlineKeyboardButton(
                text="✅ عضو شدم",
                callback_data=callback
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)