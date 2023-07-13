from aiohttp import ClientSession
import asyncio, json, ssl, certifi
from random import randint
from currency_converter import CurrencyConverter
from datetime import date

cur = CurrencyConverter()

from utils import config
class ProxyLine():
    def __init__(self):
        self.api = config.config("proxy_api")
        self.url = 'https://panel.proxyline.net/api'

    async def get_balance(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with ClientSession() as session:
            async with session.get(url=f'{self.url}/balance/?api_key={self.api}', ssl_context=ssl_context) as response:
                if response.status == 200 or response.status == 201:
                    data = await response.text()
                    bal_usd = json.loads(data)['balance']
                    balance = cur.convert(float(bal_usd), 'USD', 'RUB', date=date(2022, 3, 1))
                else:
                    balance = 0
                
        return balance
    
    async def get_price_proxy(self, proxy_type, country, quantity, time):
        url = f'{self.url}/new-order-amount/?api_key={self.api}'
        data = {
            'type': 'dedicated' if proxy_type != 'ipv4_shared' else 'shared',
            'ip_version': 4 if proxy_type != 'ipv6' else 6,
            'country': country,
            'quantity': quantity,
            'period': time,
        }
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with ClientSession() as session:
            async with session.post(url=url, data=data, ssl_context=ssl_context) as response:
                if response.status == 200 or response.status == 201:
                    data = await response.text()
                    print(f"[PROXY] GET PRICE = {data}")
                    amount = json.loads(data)['amount']
                else:
                    amount = 0
        
        return amount

    async def get_city(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        url = f'{self.url}/countries/?api_key={self.api}'
        async with ClientSession() as session:
            async with session.get(url=url, ssl_context=ssl_context) as response:
                if response.status == 200 or response.status == 201:
                    data = await response.text()
                    city = json.loads(data)
                else:
                    city = 0
        
        return city

    async def get_proxy_ips(self, types, country, city, count):
        proxy_type = 4 if types != 'ipv6' else 6
        types_proxy = 'dedicated' if types != 'ipv4_shared' else 'shared'

        url = f'{self.url}/ips/?api_key={self.api}&ip_version={proxy_type}&type={types_proxy}&country={country}'
        data = {
            'city': city,
        }
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with ClientSession() as session:
            async with session.get(url=url, data=data, ssl_context=ssl_context) as response:
                if response.status == 200 or response.status == 201:
                    data = await response.text()
                    data = json.loads(data)
                    ips = []
                    for i in range(int(count)):
                        ips.append(data[i]['id'])
                else:
                    ips = [0]
                
        return ips

    async def new_order_proxy(self, types, country, quantity, time):
        url = f'{self.url}/new-order/?api_key={self.api}'
        data = {
            'type': 'dedicated' if types != 'ipv4_shared' else 'shared',
            'ip_version': 4 if types != 'ipv6' else 6,
            'country': country,
            'quantity': quantity,
            'period': time,
        }
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with ClientSession() as session:
            async with session.post(url=url, data=data, ssl_context=ssl_context) as response:
                info = await response.text()
                if response.status == 200 or response.status == 201:
                    px = json.loads(info)
                    proxy = []
                    for i in range(len(px)):
                        product = [px[i]['ip'], px[i]['country'], px[i]['ip_version'], px[i]['order_id'], px[i]['type'], px[i]['date'],
                                px[i]['date_end'], px[i]['user'], px[i]['password'], px[i]['port_http'], px[i]['port_socks5'], px[i]['internal_ip']]
                        proxy.append(product)

                else:
                    proxy = ['NO_BALANCE']

        return proxy



