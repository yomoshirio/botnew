from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardButton as ib
from utils import config
import asyncio
from payok_handler import gen_pay_link
from data import add_select_groups


def menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row(ib('🛒 Каталог', callback_data='to_catalog'), ib('💳 Пополнить', callback_data='payments'))
    markup.row(ib('💻 Кабинет', callback_data='cabinet'), ib('🤝 Партнёры', callback_data='referral'))
    markup.row(ib('ℹ️ Информация', callback_data='info'), ib('🎁 Промокод', callback_data='promocode'))

    
    return markup

def back_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('⬅Назад', callback_data='to_menu'))
    return markup

def help_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
                InlineKeyboardButton(
					text='😎 Админ', url=f'https://t.me/aaa'),
                InlineKeyboardButton(
					text='💬 Chat', url=f'https://t.me/aaa'),
			],
			[
				InlineKeyboardButton(
					text='📰 News', url='https://t.me/aaa'),
                InlineKeyboardButton(
                    text='🎉 Отзывы', url='https://t.me/aaa')
			],
			[
                InlineKeyboardButton(
                    text='☁️ Cloud', url='https://t.me/aaa'),
				InlineKeyboardButton(
					text='📕 Правила', callback_data='rules')
			],

			[
				InlineKeyboardButton(text = '⬅Назад', callback_data = 'to_menu'),
			],
		]
	)

	return markup

"""
def projects_markup():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='📣 Канал', url='https://t.me/+zuxTK1iyxjNiNjUy'),
                InlineKeyboardButton(
                    text='💭 Чатик', url='https://t.me/+BEaXPwdObw5kMTMy'),
            ]
        ]
    )

    return markup

"""

def cabinet_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			#[
			#	InlineKeyboardButton(text = '💳 Пополнить', callback_data = 'payments'),
            #    InlineKeyboardButton(text = '🎁 Промокод', callback_data = 'promocode'),
			#],
            #[
            #    InlineKeyboardButton(text = '🧑🏻‍🔧 Партнерская программа', callback_data = 'referral'),
            #],
            [
                InlineKeyboardButton(text = '🛒 Мои покупки', callback_data = 'my_purchases'),
                InlineKeyboardButton(text = '🌐 Крипто курс', callback_data = 'crypto_curs')
            ],
            [
                InlineKeyboardButton(text = "💬 Доступ в чат покупателей", callback_data="pclient")
            ],
            [
                InlineKeyboardButton('⬅Назад', callback_data='to_menu')
            ]
		]
	)

	return markup

def payment_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
                InlineKeyboardButton(text = '💳 QIWI', callback_data = 'pay_qiwi'),
                InlineKeyboardButton(text = '💳 BANKER', callback_data = 'pay_btc')
			],
            [
				InlineKeyboardButton(text = '💳 CARD | QIWI | ЮMONEY | BTC', callback_data = 'pay_payok')
			],
            [
                InlineKeyboardButton(text = '🌐 Криптовалюты @CryptoBot', callback_data = 'pay_CB')
            ],
            [
              InlineKeyboardButton(text = '🔘 WebMoney WMZ', callback_data = 'pay_WM'),
              InlineKeyboardButton(text = '🐶 DOGE', callback_data = 'pay_DOGE')
            ],
			[
				InlineKeyboardButton(text = '⬅Назад', callback_data = 'to_menu'),
			],
		]
	)

	return markup

def close_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '💢 Понятно', callback_data = 'to_close'),
			],
		]
	)

	return markup

def pay_qiwi_markup(url):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='💳 Произвести оплату', url=url)
            ]
        ]
    )

    return markup


spisok = add_select_groups()
url_id = [url_id[2] for url_id in spisok]
url = [url[1] for url in spisok]
text_url = [text_url[0] for text_url in spisok]
kbsub = InlineKeyboardMarkup()
for i in range(len(spisok)):   
    kbsub.row(InlineKeyboardButton(text=text_url[i], url=url[i]))
kbsub.row(InlineKeyboardButton("☑️ Проверить", callback_data='subbed'))


kbcancel = InlineKeyboardMarkup().row(InlineKeyboardButton("💢 Отменить активацию", callback_data="promocancel"))

def ws_markup():
    markup = InlineKeyboardMarkup()
    markup.row(ib("📬 Отзывы", url="https://t.me/end_soft"), ib("📜 Новости", url="https://t.me/end_soft"))
    markup.row(InlineKeyboardButton('⬅Назад', callback_data='to_menu'))
    return markup

def gen_cb_kb(prod_id: str):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('📝 Оставить отзыв', callback_data=f'lr:{prod_id}'))
    return markup

def gen_ref_kb(user_id: str):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('📣 Поделиться ссылкой', switch_inline_query=f'ad:{user_id}'))
    markup.add(InlineKeyboardButton(text = '⬅Назад', callback_data = 'to_menu'))
    return markup

def gen_confirm_kb():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('☑️ Отправить', callback_data='lr_confirm'))
    markup.add(InlineKeyboardButton('❌ Отменить', callback_data='lr_deny'))
    return markup

def gen_nb_kb(user_id: int, ref_id: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('🤖 Я не бот', callback_data=f'not_bot:{user_id}_{ref_id}'))
    return markup

async def payok_kb(amount: float, payment_name: str, desc: str):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('💳 Произвести оплату', url=await gen_pay_link(amount=amount, desc=desc, payment_name=payment_name)))
    markup.add(InlineKeyboardButton('🔎 Проверить оплату', callback_data='payok_check'))
    markup.add(InlineKeyboardButton('💢 Отменить пополнение', callback_data='dpayok'))
    return markup
