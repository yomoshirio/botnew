from states import user
from aiosqlite import connect
import requests, json, os
from aiogram import types
from datetime import datetime
from random import randint

from utils import config, misc, ProxyLine
from data import User, messages as mes


class Proxy():
    def __init__(self) -> None:
        self.sql_path = './data/database.db'
        self.days_list = [5, 10, 20, 30, 60, 90, 120, 150, 180, 
                    210, 240, 270, 300, 330, 360]
        self.proxy_count = [1, 2, 3, 4, 5, 10]
        self.country = misc.country
        self.city = misc.city

    def country_name(self, proxy_type, country_code):
        lists = self.country.get(proxy_type)
        name = lists.get(country_code)

        return name
    
    def city_name(self, country, city):
        index = self.city.get(country)
        name = index.get(int(city))

        return name

    def proxy_type_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(text='🌀 IPv4', callback_data='proxy_type:ipv4'),
            types.InlineKeyboardButton(text='🌐 IPv6', callback_data='proxy_type:ipv6'),
            types.InlineKeyboardButton(text='♻️ IPv4 Shared', callback_data='proxy_type:ipv4_shared'),
        )
        markup.add(
            types.InlineKeyboardButton(text='Выйти', callback_data='to_catalog')
        )

        return markup

    def proxy_time_menu(self, proxy_type):
        markup = types.InlineKeyboardMarkup(row_width=3)
        x1 = 0
        x2 = 1
        x3 = 2

        for i in range(6):
            try:
                markup.add(
                    types.InlineKeyboardButton(text = f'{self.days_list[x1]} дней', 
                                callback_data = f'proxy_time:{proxy_type}:{self.days_list[x1]}'),
                    types.InlineKeyboardButton(text = f'{self.days_list[x2]} дней', 
                                callback_data = f'proxy_time:{proxy_type}:{self.days_list[x2]}'),
                    types.InlineKeyboardButton(text = f'{self.days_list[x3]} дней', 
                                callback_data = f'proxy_time:{proxy_type}:{self.days_list[x3]}')
                )
                x1 += 3
                x2 += 3
                x3 += 3
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text = f'{self.days_list[x1]} дней', 
                                callback_data = f'proxy_time:{proxy_type}:{self.days_list[x1]}'),
                    )
                    break
                except:pass
        markup.add(
            types.InlineKeyboardButton(text = '🔙 Каталог', callback_data = 'to_catalog')
        )

        return markup

    def proxy_country_menu(self, proxy_type, proxy_time):
        country = list(self.country.get(proxy_type).keys())

        markup = types.InlineKeyboardMarkup(row_width=3)
        x1 = 0
        x2 = 1
        x3 = 2

        for i in range(len(country)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x1])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x1]}'),
                    types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x2])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x2]}'),
                    types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x3])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x3]}'),
                )
                x1 += 3
                x2 += 3
                x3 += 3
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x1])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x1]}'),
                        types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x2])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x2]}'),
                    )
                    break
                except IndexError:
                    try:
                        markup.add(
                            types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x1])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x1]}'),
                        )
                        break
                    except:pass
        markup.add(
            types.InlineKeyboardButton(text='🔙 Меню', callback_data='to_catalog')
        )

        return markup
    
    def proxy_city_menu(self, proxy_type, proxy_time, proxy_country):
        city = list(self.city.get(proxy_country).keys())

        markup = types.InlineKeyboardMarkup(row_width=3)
        x1 = 0
        x2 = 1
        x3 = 2

        for i in range(len(city)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x1])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x1]}'),
                    types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x2])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x2]}'),
                    types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x3])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x3]}'),
                )
                x1 += 3
                x2 += 3
                x3 += 3
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x1])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x1]}'),
                        types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x2])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x2]}'),
                    )
                    break
                except IndexError:
                    try:
                        markup.add(
                            types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x1])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x1]}'),
                        )
                        break
                    except:pass
        markup.add(
            types.InlineKeyboardButton(text='⛩ Любой город', 
                                    callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:0')
        )
        markup.add(
            types.InlineKeyboardButton(text='🔙 Меню', callback_data='to_catalog')
        )

        return markup

    def proxy_count_menu(self, proxy_type, proxy_time, proxy_country):
        markup = types.InlineKeyboardMarkup(row_width=3)
        x1 = 0
        x2 = 1
        x3 = 2

        for i in range(len(self.proxy_count)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text = f'🧿 {self.proxy_count[x1]} Шт.', 
                                callback_data = f'proxy_сount:{proxy_type}:{proxy_time}:{proxy_country}:{self.proxy_count[x1]}'),
                    types.InlineKeyboardButton(text = f'🧿 {self.proxy_count[x2]} Шт.', 
                                callback_data = f'proxy_сount:{proxy_type}:{proxy_time}:{proxy_country}:{self.proxy_count[x2]}'),
                    types.InlineKeyboardButton(text = f'🧿 {self.proxy_count[x3]} Шт.', 
                                callback_data = f'proxy_сount:{proxy_type}:{proxy_time}:{proxy_country}:{self.proxy_count[x3]}')
                )
                x1 += 3
                x2 += 3
                x3 += 3
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text = f'🧿 {self.proxy_count[x1]} Шт.', 
                                callback_data = f'proxy_сount:{proxy_type}:{proxy_time}:{proxy_country}:{self.proxy_count[x1]}'),
                    )
                    break
                except:pass
        markup.add(
            types.InlineKeyboardButton(text = '🔙 Каталог', callback_data = 'to_catalog')
        )

        return markup

    async def get_prices(self, proxy_type, proxy_time, proxy_country, proxy_count):
        prices = await ProxyLine().get_price_proxy(proxy_type, proxy_country, proxy_count, proxy_time)
        price = prices / 100 * int(config.config("proxy_percent")) + prices

        return price
    
    async def proxy_buy_info(self, proxy_type, proxy_time, proxy_country, proxy_count):
        price = await self.get_prices(proxy_type, proxy_time, proxy_country, proxy_count)
        if price != 0:
            text = f"""
<b>🧿 Вы выбрали:</b>

<b>💈 Тип:</b> {proxy_type}
<b>💈 Время:</b> {proxy_time} дней
<b>💈 Страна:</b> {self.country_name(proxy_type, proxy_country)}

<b>🔰 Количество:</b> {proxy_count} шт

<b>♻️ Цена:</b> {price} RUB

<b>✅ Для подтверждения покупки, нажмите кнопку «Купить» и ожидайте выдачу proxy.</b>
"""
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton(text=f'♻️ Купить | {price} RUB',
                                           callback_data=f'proxy_buy:{proxy_type}:{proxy_time}:{proxy_country}:{proxy_count}:{price}'),
                types.InlineKeyboardButton(text=f'🔝 Meню', callback_data = 'to_catalog'),
            )
        else:
            text = 'Технические неполадки, попробуйте чуть чуть позже'
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton(text=f'🔝 Meню', callback_data = 'to_catalog'),
            )

        return text, markup
    
    async def buy_proxy(self, bot, user_id, proxy_type, proxy_time, proxy_country, proxy_count, proxy_price, msg_id):
        await bot.delete_message(chat_id=user_id, message_id=msg_id)
        balance = await ProxyLine().get_balance()
        if float(User(user_id).balance) >= float(proxy_price):
            if float(balance) >= float(proxy_price):
                order = await ProxyLine().new_order_proxy(proxy_type, proxy_country, proxy_count, proxy_time)
                if order[0] != 'NO_BALANCE':
                    await User(user_id).update_balance(-float(proxy_price))
                    await User(user_id).up_purchases(1)
                    msg = ''

                    for i in order:
                        text = f"""
<b>♻️ Тип прокси:</b> {i[4]} | {proxy_type}
<b>🌎 Страна:</b> {self.country_name(proxy_type, proxy_country)} 

<b>👨🏻‍💻 Логин:</b> <code>{i[7]}</code> | <b>Пароль:</b> <code>{i[8]}</code>

<b>🕰 Дата:</b> 
-покупки - {i[5]}  
-окончания - {i[6]}

<b>🌐 Proxy:</b> ip - <code>{i[0]}</code> | ID: {i[3]}

<b>🌀 Port:</b>
-http - <code>{i[9]}</code> |socks5 - <code>{i[10]}</code>

<b>🌐 Interval IP:</b> {i[11] if proxy_type == 'ipv6' else ''}
"""                 
                        msg += text

                        await self.write_history(user_id, proxy_type, text)
                    file_name = f'proxy_{randint(1111, 9999)}'

                    with open(file=f'./utils/docs/{file_name}.txt', mode='w+', encoding='UTF-8') as docs:
                        docs.write(msg)

                    with open(file=f'./utils/docs/{file_name}.txt', mode='rb') as docs:
                        await bot.send_message(chat_id=user_id, text=mes.access_purchase)
                    
                        await bot.send_document(chat_id=user_id, document=docs, caption='Ваши прокси  (^_^)')

                    product = open(f'./utils/docs/{file_name}.txt', 'rb')
                    text = f'Куплен товар!\n Пользователь: @{User(user_id).username} | {user_id}'
                    await bot.send_document(chat_id=config.config("admin_group"), document=product, caption=text)

                    os.remove(f'./utils/docs/{file_name}.txt')
                else:
                    await bot.send_message(chat_id=user_id, text='Технические неполадки!')
            else:
                await bot.send_message(chat_id=user_id, text='Технические неполадки!')
                await bot.send_message(chat_id=config.config("admin_group"), 
                    text=f'Пополни баланс проксилайн!\n Текущий баланс: {balance}| Цена покупки: {proxy_price}')
        
        else:
            await bot.send_message(chat_id=user_id, text='Пополните свой баланс!')
                

    async def write_history(self, user_id, proxy_type, text):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT COUNT(*) FROM purchase_history')
            count = await select.fetchone()
            proxy = [count[0] + 1, user_id, 'Proxy', proxy_type, text, datetime.now()]
            await db.execute('INSERT INTO purchase_history VALUES (?,?,?,?,?,?)', proxy)
            await db.commit()

