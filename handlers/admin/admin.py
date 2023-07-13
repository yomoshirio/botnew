from aiogram import types

from loader import bot, vip
from filters import IsAdmin, IsPrivate
from keyboards import inline as menu

@vip.message_handler(IsAdmin(), IsPrivate(), commands=['admin', 'a', 'panel'])
async def admin_handler(msg: types.Message):
    await msg.answer('👑 <b>Админ панель Cloud shop</b>', reply_markup = menu.admin_markup())

