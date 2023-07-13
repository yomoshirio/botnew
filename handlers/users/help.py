from middlewares.throttling import rate_limit
from aiogram import types

from loader import vip
from filters import IsPrivate

@rate_limit(limit=1)
@vip.message_handler(IsPrivate(), commands=['help'])
async def start_handler(msg: types.Message):
	await msg.answer(f"""Меня зовут CLOUD, со мной все хорошо, просто меня изнасиловали ):""")
