from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import vip, bot
from filters import IsPrivate
from keyboards import defaut as menu


# Обработка всех колбэков которые потеряли стейты после перезапуска скрипта
@vip.callback_query_handler(text="...", state="*")
async def processing_missed_callback(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

# Обработка всех неизвестных сообщений
@vip.message_handler(IsPrivate())
async def processing_missed_messages(message: types.Message):
    await message.answer("<b>💢 Данной команды в боте не существует!</b>\n"
                         "❗️ Напишите /start для обновления", reply_markup=menu.main_menu())
