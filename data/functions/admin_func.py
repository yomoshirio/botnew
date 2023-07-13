import sqlite3
from aiogram import types
from aiosqlite import connect
import random
import datetime

from utils.proxyline import ProxyLine
from utils.cheating_api import SMMPanelAPI


async def admin_stats():
    conn = sqlite3.connect("./data/database.db")
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM users')
    row = cursor.fetchall()

    d = datetime.timedelta(days=1)
    h = datetime.timedelta(hours=1)
    date = datetime.datetime.now()

    amount_user_all = 0
    amount_user_day = 0
    amount_user_hour = 0

    for i in row:
        amount_user_all += 1

        if date - datetime.datetime.fromisoformat(i[6]) <= d:
            amount_user_day += 1
        if date - datetime.datetime.fromisoformat(i[6]) <= h:
            amount_user_hour += 1

    cursor.execute(f'SELECT * FROM deposit_logs')
    row = cursor.fetchall()

    qiwi = 0
    all_qiwi = 0
    banker = 0
    all_banker = 0
    chatex = 0
    all_chatex = 0
    for i in row:
        if i[1] == 'qiwi':
            if date - datetime.datetime.fromisoformat(i[3]) <= d:
                qiwi += i[2]

            all_qiwi += i[2]

        elif i[1] == 'banker':
            if date - datetime.datetime.fromisoformat(i[3]) <= d:
                banker += i[2]

            all_banker += i[2]
        elif i[1] == 'chatex':
            if date - datetime.datetime.fromisoformat(i[3]) <= d:
                chatex += i[2]

            all_chatex += i[2]

    cursor.execute('SELECT SUM(purchases) FROM users')
    row = cursor.fetchall()[0][0]

    all_purchases = row

    proxy = await ProxyLine().get_balance()
    cheat = await SMMPanelAPI().get_balance()


    msg = f"""
<b>👤 Информация о пользователях:</b>
➖➖➖➖➖➖
◾️ <b>За все время:</b> <code>{amount_user_all}</code>
◾️ <b>За день:</b> <code>{amount_user_day}</code>
◾️ <b>За час:</b> <code>{amount_user_hour}</code>

<b>⏳ Пополнений за 24 часа</b>
➖➖➖➖➖➖
◾️ <b>QIWI:</b> <code>{qiwi} ₽</code>
◾️ <b>Banker:</b> <code>{banker} ₽</code>

<b>☑️ Ниже приведены данные за все время</b>
➖➖➖➖➖➖
◾️ <b>Пополнения QIWI:</b> <code>{all_qiwi} ₽</code>
◾️ <b>Пополнения BANKER:</b> <code>{all_banker} ₽</code>
◾️ <b>Продаж в магазине:</b> <code>{all_purchases} шт</code>

🔎 <b>Балансы сайтов api поставщиков</b>
➖➖➖➖➖➖
◾️ <b>Баланс ProxyLine:</b> <code>{proxy}</code> <b>RUB</b>
◾️ <b>Баланс SOC-Proof:</b> <code>{cheat}</code> <b>RUB</b>
"""

    return msg


def get_users_list():
    conn = sqlite3.connect("./data/database.db")
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT * FROM users')
    users = cursor.fetchall()

    return users

class AdmPromo():
    def __init__(self) -> None:
        self.sql_path = "./data/database.db"

    async def add_promo(self, name, money, amount):
        async with connect(self.sql_path) as db:
            promo = [random.randint(111, 999), name, amount, money, "0,"]
            await db.execute(f'INSERT INTO promocode VALUES (?,?,?,?,?)', promo)
            await db.commit()

    async def activ_promo_menu(self):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM promocode')
            info = await select.fetchall()
            markup = types.InlineKeyboardMarkup()
        for i in info:
                markup.add(types.InlineKeyboardButton(text=f'🎁 {i[1]}| Kol: {i[3]} | {i[2]} ₽',callback_data=f'adm_promo:{i[0]}'))

        return markup

    async def get_info_promo(self, promo_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM promocode WHERE id = ?', [promo_id])
            info = await select.fetchone()
    
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add( 
                types.InlineKeyboardButton(text='Удалить', callback_data=f'promo_delete:{promo_id}'),
                types.InlineKeyboardButton(text='Выйти', callback_data='to_close'),
            )

        msg = f"""
<b>🕹 ID PROMO:</b> {info[0]}

<b>🕹 Название:</b> {info[1]}

<b>🔗 Активаций:</b> {info[3]}

<b>💰 Награда:</b> {info[2]} RUB

        """

        return msg, markup

    async def delete_promocode(self, promo_id):
        async with connect(self.sql_path) as db:
            await db.execute('DELETE FROM promocode WHERE id = ?', [promo_id])
            await db.commit()




async def add_new_group(text, urlpath, urlid):
    conn = sqlite3.connect("./data/database.db")
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO urlpaths(text, urlpath, urlid) VALUES (?,?,?)', [str(text), str(urlpath), str(urlid)])
    conn.commit()


def add_select_groups():
    conn = sqlite3.connect("./data/database.db")
    cursor = conn.cursor()
    urls = cursor.execute(f'SELECT * FROM urlpaths')
    urls = cursor.fetchall()


    return urls


async def delete_groups(urlpath):
    conn = sqlite3.connect("./data/database.db")
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM urlpaths WHERE urlpath = ?', [str(urlpath), ])
    conn.commit()


