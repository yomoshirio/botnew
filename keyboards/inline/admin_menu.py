from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '📊 Статистика', callback_data = 'admin_stats'),
                InlineKeyboardButton(text = '🍭 Промокоды', callback_data = 'admin_promo')
			],
            [
                InlineKeyboardButton(text = '🔎 Поиск пользователя', callback_data = 'admin_search'),
				InlineKeyboardButton(text='🔒 Смена киви', callback_data='change_qiwi')
            ],
            [
                InlineKeyboardButton(text = '💬 Рассылка', callback_data = 'admin_sending'),
                InlineKeyboardButton(text = '📦 Каталоги', callback_data = 'admin_catalogs')
            ],
            [
				InlineKeyboardButton(text = '🔗 Создать ссылку на товар', callback_data='showlinks')

			],
			[
			InlineKeyboardButton(text = '🔗 Создать ссылку на чат', callback_data='creareurl')
			],
			[
			InlineKeyboardButton(text = '🔗 Удалить ссылку на чат', callback_data='deleteurl')
			],
			[
			InlineKeyboardButton(text = '🔗 Показать все ссылки на чаты', callback_data='showurls')
			],

		]
	)

	return markup

def admin_user_menu(user_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
                InlineKeyboardButton(text = '💳 Изменить баланс', callback_data = f'adm_give_balance:{user_id}'),
			],
			[
				InlineKeyboardButton(text = '❌ Забанить', callback_data = f'adm_ban:{user_id}'),
				InlineKeyboardButton(text = '✅ Разбанить', callback_data = f'adm_unban:{user_id}')
			],
			[
				InlineKeyboardButton(text='✉️ Отправить сообщение', callback_data = f'adm_send:{user_id}'),
			],
		]
	)

	return markup

def adm_sending():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '📖 Рассылка текст', callback_data = 'email_sending_text'),
			],
			[
				InlineKeyboardButton(text = '🎆 Рассылка с фото', callback_data = 'email_sending_photo'),
			]
		]
	)

	return markup

def adm_catalog_markup():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '🎛 Категории', callback_data = 'admin_catalog'),
			],
			[
				InlineKeyboardButton(text = '🗂 Под категории', callback_data = 'admin_subcatalog'),
			],
			[
				InlineKeyboardButton(text = '🛒 Товар', callback_data = 'admin_product'),
			]
		]
	)

	return markup

def adm_catalog_edit():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '🗃 Активные каталоги', callback_data = 'adm_act_catalog'),
			],
			[
				InlineKeyboardButton(text = '➕ Создать каталог', callback_data = 'adm_create_catalog'),
			]
		]
	)

	return markup

def adm_catalog_info(catalog_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '🗂 Создать подкаталог', callback_data = f'create_subcatalog:{catalog_id}'),
			],
			[
				InlineKeyboardButton(text = '❌ Удалить каталог', callback_data = f'delete_category:{catalog_id}'),
			]
		]
	)

	return markup


def adm_subcatalog_edit():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '🗂 Активные подкаталоги', callback_data = 'adm_act_subcatalog'),
			],
			[
				InlineKeyboardButton(text = '➕ Создать подкаталог', callback_data = 'adm_create_subcatalog'),
			]
		]
	)

	return markup

def adm_subcatalog_info(catalog_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '➕ Создать товар', callback_data = f'create_product:{catalog_id}'),
			],
			[
				InlineKeyboardButton(text = '❌ Удалить подкаталог', callback_data = f'delete_subcatalo:{catalog_id}'),
			]
		]
	)

	return markup

def adm_product_edit():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '📦 Активные товары', callback_data = 'adm_act_product'),
			],
			[
				InlineKeyboardButton(text = '➕ Создать товар', callback_data = 'adm_create_product'),
			]
		]
	)

	return markup

def adm_product_info(product_id):
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text = '📥 Загрузить товар', callback_data = f'download_product:{product_id}'),
			],
			[
				InlineKeyboardButton(text = '❌ Удалить товар', callback_data = f'delete_product:{product_id}'),
			]
		]
	)

	return markup

def adm_promo_info():
	markup = InlineKeyboardMarkup(
		inline_keyboard = [
			[
				InlineKeyboardButton(text='🍭 Активные промо', callback_data='activ_promo'),
				InlineKeyboardButton(text='📝 Создать промо', callback_data='create_promo'),
			],
			[ 
				InlineKeyboardButton(text='💢 Закрыть', callback_data='to_close')
			]
		]
	)

	return markup
