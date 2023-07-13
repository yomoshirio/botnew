from aiogram import executor
import asyncio

from loader import vip
import handlers, middlewares
from utils import logger, QiwiPay

async def startup(dp):
	asyncio.create_task(QiwiPay().wait_pays_qiwi(dp.bot, 10))

if __name__ == '__main__':
	logger.debug('SHOP| Started')
	executor.start_polling(vip, on_startup=startup)
