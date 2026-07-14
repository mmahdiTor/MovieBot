from pyrogram.errors import UserNotParticipant

import config


async def check_force_sub(client, user_id):

    valid_status = (
        "member",
        "administrator",
        "owner"
    )

    for channel in config.FORCE_SUB_CHANNELS:

        try:

            member = await client.get_chat_member(
                channel,
                user_id
            )

            status = str(member.status).lower()

            if not any(x in status for x in valid_status):
                return False

        except UserNotParticipant:
            return False

        except Exception as e:

            print(f"[ForceSub] {e}")

            return False

    return True