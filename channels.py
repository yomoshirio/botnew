from aiogram import Bot
from tortoise import fields
from tortoise.models import Model




async def is_user_subscribed(bot: Bot, user_id: int) -> tuple[bool, list[str]]:
    all_channels: ['-1001568992871']
    success_channels: list = list()
    flag: bool = True
    for channel in all_channels:
        try:
            chat_member = await bot.get_chat_member(channel.tg_id, user_id)
            if chat_member.status == 'left':
                flag = False
                success_channels.append((channel.name, channel.url))
            else:
                pass
        except Exception as e:
            flag = False
            success_channels.append((channel.name, channel.url))

    return flag, success_channels



