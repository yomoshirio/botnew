from aiosqlite import connect
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime


from data import cheat_message
from utils import misc

class SMMPanel():
    def __init__(self) -> None:
        self.sql_path = './data/database.db'
        self.cheat = misc.cheat
        self.base = {
            'tg': 'Telegram',
            'vk': 'Vkontakte',
            'tt': 'TikTok',
            'yt': 'YouTube',
            'ig': 'Instagram'
        }

    def cheat_service_name(self, service):
        name = self.base.get(service)

        return name

    def cheat_type_name(self, cheat_types):
        types = {
            'subscriptions': 'Подписки',
            'views': 'Просмотры',
            'like': 'Лайки',
            'reactions': 'Реакции',
            'autoviews': 'Автопросмотры',
            'comments': 'Комментарии',
            'other': 'Другое'
        }
        name = types.get(cheat_types)

        return name

    def cheat_order_name(self, service, cheat_type, order):
        orders = self.cheat.get(f'{service}').get(cheat_type)
        order_name = orders.get(order).get('name')

        return order_name

    async def cheating_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=2)

        category = list(self.cheat.keys())

        x1 = 0
        x2 = 1

        for i in range(len(category)):
            try:
                markup.add(
                    types.InlineKeyboardButton(
                        text=f'{self.cheat_service_name(category[x1])}', callback_data=f'cheat_serivce:{category[x1]}'),
                    types.InlineKeyboardButton(
                        text=f'{self.cheat_service_name(category[x2])}', callback_data=f'cheat_serivce:{category[x2]}')
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(
                            text=f'{self.cheat_service_name(category[x1])}', callback_data=f'cheat_serivce:{category[x1]}'),
                    )
                    break
                except:pass

        markup.add(
                types.InlineKeyboardButton(text = '🔙 Назад', callback_data = 'to_catalog'),
        )

        return markup

    async def cheat_type_menu(self, service):
        cheat_types = list(self.cheat.get(f'{service}').keys())

        markup = types.InlineKeyboardMarkup(row_width=2)

        x1 = 0
        x2 = 1

        for i in range(len(cheat_types)):
            try:
                markup.add(
                    types.InlineKeyboardButton(
                        text=f'{self.cheat_type_name(cheat_types[x1])}', callback_data=f'cheat_type:{service}:{cheat_types[x1]}'),
                    types.InlineKeyboardButton(
                        text=f'{self.cheat_type_name(cheat_types[x2])}', callback_data=f'cheat_type:{service}:{cheat_types[x2]}')
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(
                            text=f'{self.cheat_type_name(cheat_types[x1])}', callback_data=f'cheat_type:{service}:{cheat_types[x1]}'),
                    )
                    break
                except:pass

        markup.add(
                types.InlineKeyboardButton(text='🔙 Назад', callback_data=f'catalog:cheating'),
        )

        return markup

    async def cheat_order_menu(self, service, cheat_type):
        orders = list(self.cheat.get(f'{service}').get(cheat_type))

        markup = types.InlineKeyboardMarkup(row_width=2)

        x1 = 0
        x2 = 1

        for i in range(len(orders)):
            try:
                markup.add(
                    types.InlineKeyboardButton(
                        text=f'{self.cheat_order_name(service, cheat_type, orders[x1])}', callback_data=f'cheat_order:{service}:{cheat_type}:{orders[x1]}'),
                    types.InlineKeyboardButton(
                        text=f'{self.cheat_order_name(service, cheat_type, orders[x2])}', callback_data=f'cheat_order:{service}:{cheat_type}:{orders[x2]}')
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(
                            text=f'{self.cheat_order_name(service, cheat_type, orders[x1])}', callback_data=f'cheat_order:{service}:{cheat_type}:{orders[x1]}'),
                    )
                    break
                except:pass

        markup.add(
                types.InlineKeyboardButton(text='🔙 Назад', callback_data=f'cheat_serivce:{service}'),
        )

        return markup

    async def cheat_messages(self, service, cheat_type, order):
        orders = self.cheat.get(f'{service}').get(cheat_type)
        order_info = orders.get(order)

        msg = cheat_message.format(
            service=self.cheat_service_name(service),
            name=self.cheat_order_name(service, cheat_type, order),
            description=order_info.get('description'),
            min=order_info.get('min'),
            max=order_info.get('max'),
        )

        return msg

    async def cheat_buy_menu(self, service, cheat_type, order, amount=None, price=None, update=None):
        orders = self.cheat.get(f'{service}').get(cheat_type)
        order_info = orders.get(order)

        if amount == None and price == None:
            amount = order_info.get('min')
            price = float(order_info.get('price')) * int(amount)

        elif update != None:
            amount += update
            price = float(order_info.get('price')) * amount

        markup = InlineKeyboardMarkup(
		    inline_keyboard = [
			    [
                    InlineKeyboardButton(text='🔻', callback_data=f'cheat_buy_update:{service}:{cheat_type}:{order}:{amount}:{price}:-100'),
                    InlineKeyboardButton(text=f'{amount} шт', callback_data='amount_product'),
                    InlineKeyboardButton(text='🔺', callback_data=f'cheat_buy_update:{service}:{cheat_type}:{order}:{amount}:{price}:100'),
			    ],
                [
                    InlineKeyboardButton(text=f'Купить за {price} руб', callback_data=f'cheat_buy:{service}:{cheat_type}:{order}:{amount}:{price}')
			    ],
                [
                    InlineKeyboardButton(text='🔻Ввести вручную🔺', callback_data=f'cheat_count:{service}:{cheat_type}:{order}')
                ],
                [
                    InlineKeyboardButton(text='« Назад', callback_data=f'cheat_type:{service}:{cheat_type}'),
                ]
		    ]
	    )


        return markup

    async def cheat_logs(self, user_id, service, service_name, cheat_type, order_id, order_name, link, count, price):
        async with connect(self.sql_path) as db:
            logs = [user_id, service, service_name, cheat_type, order_id, order_name, count, price, link, datetime.now()]
            await db.execute('INSERT INTO cheat_logs VALUES (?,?,?,?,?,?,?,?,?,?)', logs)
            await db.commit()