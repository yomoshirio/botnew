from aiohttp import ClientSession
import asyncio, json, ssl, certifi
from random import randint

from utils import config

class SMMPanelAPI():
    def __init__(self) -> None:
        self.api = config.config('cheating_api')
        self.url = 'https://partner.soc-proof.su/api/v2'

    async def get_balance(self) -> float:
        data = {
            'key': self.api,
            'action': 'balance'
        }
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with ClientSession() as session:
            async with session.post(url=self.url, data=data, ssl_context=ssl_context) as response:
                if response.status == 200:
                    info =await response.text()
                    data = json.loads(info)
                    balance, currency = data['balance'], data['currency']
                else:
                    balance = 0
        
        return balance

    async def add_order(self, service_id, link, count):
        data = {
            'key': self.api,
            'action': 'add',
            'service': service_id,
            'link': link,
            'quantity': count,
        }
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with ClientSession() as session:
            async with session.post(url=self.url, data=data, ssl_context=ssl_context) as response:
                if response.status == 200 or response.status == 201:
                    info =await response.text()
                    print(info)
                    data = json.loads(info)
                    if not data.get('error'):
                        order_id = data['order']
                    else:
                        order_id = 'no_order'
                else:
                    order_id = 'no_order'
        
        return order_id

    async def status_order(self, order):
        data = {
            'key': self.api,
            'action': 'status',
            'order': order,
        }
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with ClientSession() as session:
            async with session.post(url=self.url, data=data, ssl_context=ssl_context) as response:
                if response.status == 200:
                    info =await response.text()
                    data = json.loads(info)
                    status = data['status']
                else:
                    status = 'no_connect'

        return status

    async def get_services(self):
        data = {
            'key': self.api,
            'action': 'services',
        }
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with ClientSession() as session:
            async with session.post(url=self.url, data=data, ssl_context=ssl_context) as response:
                if response.status == 200:
                    info = json.loads(await response.text())
                    with open('text.txt', 'w+', encoding='UTF-8') as txt:
                        for i in info:
                            txt.write(str(i) + '\n')



       
