from filters.filters import IsBan
from aiogram import types
import re

from loader import bot, vip
from filters import IsPrivate
from data import messages as mes, User
from keyboards import defaut as key, inline as menu
from utils import config, Catalog, BTCPayment, SMMPanelAPI
from handlers.users.start import check_sub

@vip.message_handler(IsPrivate(), IsBan(), text=key.shop_menu_btn[0], state="*")
async def message_three(msg: types.Message):
    if await check_sub(msg):
        photo = 'https://i.imgur.com/kePY9XC.jpg'
        text = f'<b>💳 Баланс:</b> {User(msg.from_user.id).balance} RUB'
        await msg.answer_photo(photo=photo, caption=text, reply_markup=menu.menu_markup())
    """
    else:
        await msg.answer('<b>❗️Вы не подписались на канал</b>', parse_mode='HTML', reply_markup=menu.kbsub)"""

@vip.message_handler(text="📩 Sakura sms")
async def smss(msg: types.Message):
    txt = """<b>📩 Самые лучшие виртуальные номера 

◽️Смс приходят быстро 
◽️Множество стран 
◽️Огромное количество сервисов 
◽️Реферальная система передача баланса и многое другое 

👉 @aaa 
👉 @aaa 
👉 @aaa</b>"""
    await msg.answer_photo("https://i.imgur.com/cUKTzb1.jpg", txt)

@vip.message_handler(text="🔓 Hyper Store")
async def smmm(msg: types.Message):
    txt = """<b>🔓 Ищешь где купить Telegram аккаунт? 
</b>
<i>— Мы продаем самые свежие Telegram аккаунты всего по 30₽! Автоматическая покупка! </i>

<b>🔗 Ссылка: </b><b>@aaa</b>"""
    await msg.answer_photo("https://imgur.com/a/Ftin2Vd.jpg", txt)


@vip.message_handler(IsPrivate(), IsBan(), lambda message: re.search(r'BTC_CHANGE_BOT\?start=', message.text) \
    or re.search(r'Chatex_bot\?start=', message.text) or re.search(r'ETH_CHANGE_BOT\?start=', message.text) or re.search(r'CryptoBot\?start=', message.text)) 
async def crypto_handler(msg: types.Message):
    await msg.answer('<b>⏳ Чек отправлен на обработку! Занимает не более 10 секунд!</b>')
    await BTCPayment().receipt_parser(bot, msg.from_user.id, msg.text)