from telethon import TelegramClient
import asyncio, re, requests, datetime, json
from aiosqlite import connect
from random import randint
from telethon import TelegramClient, events

from data import User, get_user
from utils import config

'''Аккаунт телеграм'''
api_id = 3851067
api_hash = '52aeab594ce82ed432f42f3c18f9af03'

client = TelegramClient(session="./utils/payments/VIPMarket", api_id=api_id, api_hash=api_hash, app_version="10 P (28)",
                        device_model="Iphone", system_version='6.12.0')

client.start()


class BTCPayment():
    def __init__(self):
        self.banker = 'BTC_CHANGE_BOT'
        self.chatex = 'Chatex_bot'
        self.eth_banker = 'ETH_CHANGE_BOT'
        self.cryptobot = 'CryptoBot'
        self.sql_path = './data/database.db'

    def btc_curs(self):
        '''Курс бтк актуальный '''
        response = requests.get(url='https://blockchain.info/ticker')
        amount = float(response.json()['RUB']['15m'])

        return amount

    def curs_eth(self):
        response = requests.get(url='https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,RUB')
        data = json.loads(response.text)
        USD = data.get('USD')

        return USD

    async def receipt_parser(self, bot, user_id: int, cheque: str):
        '''Проверка, чей чек был отпрвлен, банкир или чатекс '''
        try:
            code = re.findall(r'c_\S+', cheque)[0]
        except IndexError:
            print("[BTC] CryptoBot check DETECTED")
        if 'BTC_CHANGE_BOT' in cheque:
            await self.banker_btc(bot, user_id, code)
        if 'CryptoBot' in cheque:
            code = cheque.split('?start=')[1]
            await self.cryptobot_pay(bot, user_id, code)
        else:
            await self.chatex_btc(bot, user_id, code)

    async def banker_btc(self, bot, user_id: int, cheque: str):
        await client.send_message(self.banker, f'/start {cheque}')
        msg_bot = await self.get_last_message_banker()

        if 'Вы получили' in msg_bot:
            btc = msg_bot.replace('(', '').replace(')', '').split(' ')
            amount = round(float(btc[2]) * self.btc_curs())
            money = await self.referals(user_id, amount)
            await User(user_id).update_balance(money)

            await self.deposit_logs(user_id, 'banker', amount)
            txxt = f"""<b>💰 Новый депозит 

◽️Сумма: {amount} RUB
◽️Способ пополнения: BANKER
◽️Пользователь: @{User(user_id).username}
◽️ID: {user_id}
◽️Баланс пользователя: {User(user_id).balance} RUB
</b>
"""
            await bot.send_message(chat_id=user_id, text=f'<b>✅ Баланс пополнен на сумму {money} ₽</b>')
            await bot.send_message(chat_id=config.config('admin_group'), text=txxt)

        else:
            await bot.send_message(chat_id=user_id, text=f'<b>❌ Не получилось активировать чек!</b>\nПричина:\n{msg_bot}')


    async def cryptobot_pay(self, bot, user_id: int, cheque: str):
        await client.send_message(self.cryptobot, f'/start {cheque}')
        msg_bot = await self.get_last_message_cryptobot()
        print(f'[BTC]: BOT MESSAGE: \n{msg_bot}')

        if 'Получение' in msg_bot:
            crypto = msg_bot.replace('(', '').replace(')', '').split(' ')
            amount = round(float(crypto[4]))
            money = await self.referals(user_id, amount)
            await User(user_id).update_balance(money)
            txxt = f"""<b>💰 Новый депозит 

◽️Сумма: {amount} RUB
◽️Способ пополнения: @CryptoBot
◽️Пользователь: @{User(user_id).username}
◽️ID: {user_id}
◽️Баланс пользователя: {User(user_id).balance} RUB
</b>
"""

            await self.deposit_logs(user_id, 'banker', amount)
            await bot.send_message(chat_id=user_id, text=f'<b>✅ Баланс пополнен на сумму {money} ₽</b>')
            await bot.send_message(chat_id=config.config('admin_group'),
                                           text=txxt)
            print("[BTC] CryptoBot check PROCESSED")

        else:
            await bot.send_message(chat_id=user_id, text=f'<b>❌ Не получилось активировать чек!</b>\nПричина:\n{msg_bot}')
            print("[BTC] CryptoBot check PROCESS FAILED")


    async def chatex_btc(self, bot, user_id: int, cheque: str):
        await client.send_message(self.chatex, f'/start {cheque}')
        msg_bot = await self.get_last_message_chatex()

        if 'Ваучер на сумму' in msg_bot:
            money = re.findall("\d.\d+ BTC", msg_bot)[0]
            if money.split(" ")[1] == 'BTC':
                btc = re.findall("\d.\d+", money)[0]
                amount = round(float(btc) * self.btc_curs())
                money = await self.referals(user_id, amount)
                await User(user_id).update_balance(money)

                await self.deposit_logs(user_id, 'chatex', amount)
                await bot.send_message(chat_id=user_id, text=f'<b>✅ Баланс пополнен на сумму {money} ₽</b>')
                await bot.send_message(chat_id=config.config('admin_group'),
                                           text=f'<b>♻️ Пришло пополнение Chatex!</b>\n\n'
                                                f'<b>🧑🏻‍🔧 От:</b> @{User(user_id).username} | {user_id}\n\n'
                                                f'<b>💰 Сумма:</b> {amount} RUB')

            else:
                await bot.send_message(chat_id=user_id, text='Упс, чек был не BTC, деньги я схавал:)')

        else:
            await bot.send_message(chat_id=user_id, text=f'<b>❌ Не получилось активировать чек!</b>\nПричина:\n{msg_bot}')

    async def deposit_logs(self, user_id: int, types: str, amount: float):
        async with connect(self.sql_path) as db:
            logs = [user_id, types, amount, datetime.datetime.now()]

            await db.execute('INSERT INTO deposit_logs VALUES (?,?,?,?)', logs)
            await db.commit()
        
    async def referals(self, user_id: int, amount: float):
        user = User(user_id)
        
        if int(user.who_invite) > 0:
            if get_user(user.who_invite) != False:

                percent = config.config("ref_percent")
                ref_money = amount / 100 * float(percent)
                money = amount - ref_money

                referal =  User(user.who_invite)
                await referal.update_balance(ref_money)
                await referal.referals_profit(ref_money)
            else:
                money = amount
        else:
            money = amount

        return money
   
    async def get_last_message_banker(self) -> str:
        while True:
            message = (await client.get_messages(self.banker, limit=1))[0]
            if message.message.startswith("Приветствую,"):
                await asyncio.sleep(0.5)
                continue
            if message.from_id is not None:
                me = await client.get_me()
                if message.from_id.user_id == me.id:
                    await asyncio.sleep(0.5)
                    continue
            else:
                return message.message

    async def get_last_message_chatex(self) -> str:
        while True:
            message = (await client.get_messages(self.chatex, limit=1))[0]
            if message.from_id is not None:
                me = await client.get_me()
                if message.from_id.user_id == me.id:
                    await asyncio.sleep(0.5)
                    continue
            else:
                return message.message

    

    async def get_last_message_cryptobot(self) -> str:
        while True:
            message = (await client.get_messages(self.cryptobot, limit=1))[0]
            if message.message.startswith("Мультивалютный кошелёк"):
                await asyncio.sleep(0.5)
                continue
            if message.from_id is not None:
                me = await client.get_me()
                if message.from_id.user_id == me.id:
                    await asyncio.sleep(0.5)
                    continue
            else:
                return message.message

