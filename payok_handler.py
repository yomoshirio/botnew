from aiohttp import ClientSession
from data.functions import User
from hashlib import md5
import json

pid = '847'
key = 'b7cf4e6379951922eeceace2ae707e02'
api_id = 632
api_key = '0A9F96891FA50C8E99FEB07A7A665DE9-9A0E3CE5E08D3D026B848A8049019379-C3EB5F6CC0D2BD46F5BB0A31F00B1C45'

async def gen_pay_link(amount: float, payment_name: str, desc: str):
    _sign = md5(f"{amount}|{payment_name}|{pid}|RUB|{desc}|{key}".encode("utf-8")).hexdigest()
    #print(f"{amount}|{payment_name}|{pid}|RUB|{desc}|{key}")
    return f"https://payok.io/pay?amount={amount}&payment={payment_name}&desc={desc}&shop={pid}&sign={_sign}"

async def get_last_pay() -> dict:
    async with ClientSession() as session:
        async with session.post('https://payok.io/api/transaction', data={'API_ID': api_id, 'API_KEY': api_key, "shop": int(pid)}) as resp:
            txt = await resp.text()
            txxt = json.loads(txt)
            return txxt

async def is_valid_transaction(user_id: int, amount: float, comment: str) -> bool:
    resp = await get_last_pay()
    if resp['status'] == 'success':
        for i in resp.keys():
            if i == 'status': pass 
            else:
                user = int(resp[i]['payment_id'].split('_')[0]) if 'repl' not in resp[i]['payment_id'] else None
                status = all([bool(user == user_id), bool(amount == float(resp[i]['amount_profit'])), bool(str(comment) == str(resp[i]['description'])), bool(int(resp[i]['transaction_status']) == 1)])
                if status == True:
                    return True
                else:
                    pass
