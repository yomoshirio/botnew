from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils import config
from data import get_user, User
from channels import is_user_subscribed
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.types import Message, CallbackQuery


no_channels: str = """
Подпишись на следующие группы, чтобы продолжить работу с ботом
"""

async def get_channel_subscribe_keyboard(channels: list) -> InlineKeyboardMarkup:
    channel_subscribe_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        channel_subscribe_keyboard.add(InlineKeyboardButton(channel[0], url=channel[1]))
    channel_subscribe_keyboard.add(InlineKeyboardButton("Проверить", callback_data='check_channels'))
    return channel_subscribe_keyboard

class IsGroup(BoundFilter):

    async def check(self, message: types.Message):
        return message.chat.type in (types.ChatType.GROUP,
                                     types.ChatType.SUPERGROUP)


class IsPrivate(BoundFilter):

    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return str(message.from_user.id) in config.config("admin_id")

class IsBan(BoundFilter):
    async def check(self, message: types.Message):
        if await get_user(message.from_user.id):
            return bool(User(message.from_user.id).ban != 'yes')
        else:
            return await get_user(message.from_user.id)



class IsSubscribed(BoundFilter):
    async def check(self, message: Message | CallbackQuery):
        is_subscribed, channels = await is_user_subscribed(message.bot, message.from_user.id)
        if is_subscribed:
            return True
        else:
            try:
                await message.answer(no_channels, reply_markup=await get_channel_subscribe_keyboard(channels))
            except Exception as e:
                await message.message.answer(no_channels, reply_markup=await get_channel_subscribe_keyboard(channels))
            raise CancelHandler()
