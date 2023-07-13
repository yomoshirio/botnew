import sqlite3
from aiogram import types
from aiosqlite import connect
from datetime import datetime, date
from utils import Product

class User():
    def __init__(self, user_id):
        self.sql_path = './data/database.db'
        conn = sqlite3.connect(self.sql_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE user_id = ?', [user_id])
        user = cursor.fetchone()

        self.user_id = user[0]
        self.username = user[1]
        self.status = user[2]
        self.balance = user[3]
        self.purchases = user[4]
        self.who_invite = user[5]
        self.date = user[6]
        self.ban = user[7]

    async def update_balance(self, value):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE users SET balance = ? WHERE user_id = ?', [float(self.balance) + float(value), self.user_id])
            await db.commit()
    
        return True

    async def up_ban(self, value):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE users SET ban = ? WHERE user_id = ?', [value, self.user_id])
            await db.commit()
        
        return True

    async def up_balance(self, value):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE users SET balance = ? WHERE user_id = ?', [value, self.user_id])
            await db.commit()
        
        return True

    async def up_purchases(self, value):
        async with connect(self.sql_path) as db:
            await db.execute('UPDATE users SET purchases = ? WHERE user_id = ?', [self.purchases + value, self.user_id])
            await db.commit()
        
        return True

    def get_days(self):
        join_time = self.date[:10].split('-')
        pars_time = date(int(join_time[0]), int(join_time[1]), int(join_time[2]))
        today = date.today()
        delta = today - pars_time
        day = str(delta).split()[0]
        if day.split(':')[0] == '0':
            day = 1
        
        return day

    async def referals_profit(self, amount):
        logs = [self.user_id, amount, datetime.now()]
        async with connect(self.sql_path) as db:
            await db.execute('INSERT INTO refferal_logs VALUES (?,?,?)', logs)
            await db.commit()
        
        return True

    async def purchases_history(self):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM purchase_history WHERE user_id = ?', [self.user_id])
            info = await select.fetchall()
        product = list(info)
        markup = types.InlineKeyboardMarkup(row_width=2)
        x1 = 0
        x2 = 1

        for i in range(len(product)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text = f'{product[x1][3]}', callback_data = f'user_purchase:{product[x1][0]}'),
                    types.InlineKeyboardButton(text = f'{product[x2][3]}', callback_data = f'user_purchase:{product[x2][0]}')
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text = f'{product[x1][3]}', callback_data = f'user_purchase:{product[x1][0]}'),
                    )
                    break
                except:pass
        markup.add(
            types.InlineKeyboardButton(text = '💢 Закрыть', callback_data = 'to_close')
        )
        return markup
    
            
async def register_user(user_id: int, referrer_id: int, username: str):
    if await get_user(user_id) == False:
        if referrer_id != '' and referrer_id != 0:
            async with connect('./data/database.db') as db:
                users = [user_id, username, 'User', 0, 0, referrer_id, datetime.now(), 'no']
                await db.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?,?)', users)
                await db.commit()
            return True
        else:
            async with connect('./data/database.db') as db:
                users = [user_id, username, 'User', 0, 0, 0, datetime.now(), 'no']
                await db.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?,?)', users)
                await db.commit()
            return True
    else:
        return False

async def first_join(user_id, username, code):
    status, invite = False, 0
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT * FROM users WHERE user_id = ?', [user_id])
        row = await select.fetchall()

        who_invite = code[7:]

        if who_invite == '':
            who_invite = 0
        
        select_invite = await db.execute('SELECT * FROM users WHERE user_id = ?', [who_invite])
        invite = await select_invite.fetchall()
        if len(list(invite)) == 0:
            who_invite = 0

        if len(list(row)) == 0:
            users = [user_id, username, 'User', 0, 0, who_invite, datetime.now(), 'no']
            await db.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?,?)', users)
            await db.commit()

            status, invite = True, who_invite

    return status, invite


async def get_user(user_id) -> bool:
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT * FROM users WHERE user_id = ?', [user_id])
        row = await select.fetchall()

        if len(list(row)) > 0:
            status = True
        else:
            status = False

    return status

async def amount_referals(user_id):
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT * FROM users WHERE who_invite = ?', [user_id])
        check = await select.fetchall()
    
    referals = len(list(check))

    return referals


async def get_promo(promo):
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT * FROM promocode WHERE name = ?', [promo])
        promocode = await select.fetchone()
    
    return promocode 


async def activate_promo(user_id, promo: str):
    info = await get_promo(promo)
    async with connect('./data/database.db') as db:

        users = f"{info[4]}{user_id},"
        await db.execute('UPDATE promocode SET activation = activation - 1, users = ? WHERE name = ?', [users, promo])
        await db.commit()

async def delete_promo(promocode):
    async with connect('./data/database.db') as db:
        await db.execute('DELETE FROM promocode WHERE name = ?', [promocode])
        await db.commit()

async def get_user_sum(user_id) -> int:
    all_sum = 0.0
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT sum FROM deposit_logs WHERE user_id = ?', [user_id])
        rows = await select.fetchall()
    rows = list(rows)
    if rows == []:
        return 0
    else:
        for i in rows:
            all_sum += float(i[0])
    return float(all_sum)