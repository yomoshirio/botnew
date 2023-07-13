from aiogram import types
from hashlib import md5
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import os
from requests import get

from loader import bot, vip
from filters import IsBan
from keyboards import defaut as key, inline as menu
from data import get_user, User, messages as mes, amount_referals, get_user_sum
from utils import config, Catalog, SubCatalog, Product, Proxy, QiwiPay, \
    SMMPanel
from states import ActivatePromo, BuyCheating
from random import randint
from payok_handler import *

@vip.inline_handler(Text(startswith='product'))
async def inline_product_handler(q: InlineQuery):
    try:
        product_id = q.query.split(':')[1]
        products = await Product().get_amount_products(product_id)
        product = await Product().get_product(product_id)
        text = f'''<b>📦 Название товара:</b> <code>{product[2]}</code>
<b>💳 Стоимость товара</b>: <code>{product[3]}</code>₽
<b>♻️ Количество:</b> <code>{products}</code>

<b>📜 Описание:</b> <i>{product[4]}</i>
'''
        input_content = InputTextMessageContent(text, parse_mode='HTML')
        result_id: str = md5(q.query.encode()).hexdigest()
        markup = InlineKeyboardMarkup().row(InlineKeyboardButton(text='🗝 Открыть товар', url=f'https://t.me/CloudShopV4RoBot?start={product_id}'))
        item = InlineQueryResultArticle(id=result_id, title=f"Отправить товар", thumb_url='https://i.imgur.com/zE0fUT3.jpg', input_message_content=input_content, reply_markup=markup)
        await bot.answer_inline_query(q.id, [item], is_personal=True, cache_time=5)
    except (TypeError, IndexError):
        pass

@vip.inline_handler(Text(startswith='ad'))
async def inline_ad_handler(q: InlineQuery):
    text = f'''<b>🛍 Cloud shop является магазином электронных товаров 

🔸Кошельки, киви, юмани! 
🔸Купоны, промокоды! 
🔸Аккаунты, соц сетей!
🔸Скрипты и паки ботов! 
🔸 Услуги накрутки 
🔸Множество другого товара! 

🤖 Cloud shop: <a href="https://t.me/CloudShopV4RoBot?start={q.query.split(":")[1]}"> @end_soft</a></b>
'''
    result_id: str = md5(q.query.encode()).hexdigest()
    markup = InlineKeyboardMarkup().row(InlineKeyboardButton(text='📌 Вступить в бота', url=f'https://t.me/CloudShopV4RoBot?start={q.query.split(":")[1]}'))
    item = InlineQueryResultPhoto(id=result_id, title=f"Отправить пост", photo_url='https://i.imgur.com/ouJD24f.jpg', thumb_url='https://i.imgur.com/ouJD24f.jpg', caption=text, reply_markup=markup)
    await bot.answer_inline_query(q.id, [item], is_personal=True, cache_time=5)

@vip.message_handler(state='sendreview')
async def sendreview(m: types.Message, state: FSMContext):
    txt = f'''<b>☑️ Отзыв готов проверьте его перед отправкой:

💬 Сообщение:</b> <code>{m.text}</code>'''
    await m.answer(text=txt, parse_mode="HTML", reply_markup=menu.gen_confirm_kb())
    await state.set_state('rconfirm')
    await state.update_data(rtext=m.text)

@vip.callback_query_handler(text='lr_confirm', state='rconfirm')
async def lr_confirm(c: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    txt = f'''<b>🎉 Пользователь оставил отзыв:</b> 

<i>◽️Username: @{c.from_user.username if c.from_user.username else 'Нет'}
◽️Id: {c.from_user.id}
◽️Товар: {data["pname"]}

📝 Сообщение: {data["rtext"]}
</i>
'''
    await bot.send_message(chat_id=config.config("admin_group"), text=txt, parse_mode="HTML")
    await state.finish()
    await c.message.answer(f"<b>🎉 Отзыв был отправлен ожидайте его проверки!</b>", parse_mode="HTML")

@vip.callback_query_handler(text='lr_deny', state='rconfirm')
async def lr_deny(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete()
    await c.message.answer('Отменено.')
    await state.finish()

@vip.message_handler(state='asksend')
async def asksend(m: types.Message, state: FSMContext):
    data = await state.get_data()
    txt = f'''<b>❓ Пользователь задал вопрос:</b>

<i>◽️Товар: {data['pname']}
◽️Username: @{m.from_user.username if m.from_user.username else 'Нет'}
◽️Id: {m.from_user.id}

💭 Сообщение:</i> {m.text}
'''
    await bot.send_message(chat_id=config.config("admin_group"), text=txt, parse_mode="HTML")
    await m.answer('''<b>☑️ Успешно отправили вопрос администратору  

Важно знать:</b> <i>ответ придёт сюда в бота. Не создавайте новых запросов! Ответ происходит в течение 24 часов</i>''', parse_mode="HTML")
    await state.finish()

@vip.callback_query_handler(text='pay_CB', state='*')
async def paycb(call: types.CallbackQuery, state: FSMContext):
    text = f'''<b>🌐 Для пополнения баланса с помощью @CryptoBot создайте чек и отправьте его в этот диалог! 

• Ton (<a href="https://ton.org/">Toncoin</a>) 
• Btc (<a href="https://bitcoin.org/">Bitcoin</a>)
• Bnb (<a href="https://binance.org/">Binance coin</a>)
• Busd (<a href="https://www.binance.com/en/busd">Binance USD</a>)
• Usdc (<a href="https://www.centre.io/usdc">USD Coin</a>)
• Usdt (<a href="https://tether.to/">Tether</a>)

👉🏻 Отправьте чек</b>:
'''
    await call.message.edit_caption(caption=text, reply_markup=menu.close_markup())
    await state.finish()

@vip.callback_query_handler(text='dpayok', state='*')
async def payok_del(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()

@vip.callback_query_handler(text='promocancel', state='*')
async def promo_del(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()

@vip.callback_query_handler(text='payok_check', state='paycheck')
async def validate_payok(c: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    status = await is_valid_transaction(c.from_user.id, data['sumx'], data['desc'])
    if status:
        txxt = f"""<b>💰 Новый депозит 

◽️Сумма: {data['sumx']}
◽️Способ пополнения: PAYOK
◽️Пользователь: @{User(c.from_user.id).username}
◽️ID: {c.from_user.id}
◽️Баланс пользователя: {User(c.from_user.id).balance} RUB
</b>
"""
        await c.answer(f'Платеж найден, зачислено {data["sumx"]} рублей', show_alert=True)
        await User(c.from_user.id).update_balance(data['sumx'])
        await QiwiPay().deposit_logs(c.from_user.id, 'qiwi', data['sumx'])
        await bot.send_message(chat_id=config.config('admin_group'),
                                                text=txxt)
        await c.message.delete()
        await state.finish()
    else:
        await c.answer('Платеж не найден.', show_alert=True)

@vip.callback_query_handler(IsBan())
async def handler_call(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.from_user.id
    message_id = call.message.message_id

    if await get_user(chat_id) == True:
        user = User(chat_id)
        if user.ban == 'no':

            if call.data == 'payments':
                text = '<b>💳 Выберите способ пополнения:</b>'
                await call.message.edit_caption(caption=text, reply_markup=menu.payment_markup())

            if call.data == 'pay_btc':
                text = mes.btc_pay
                await call.message.edit_caption(caption=text, reply_markup=menu.close_markup())

            if call.data == 'pay_CB':
                text = f'''<b>🌐 Для пополнения баланса с помощью @CryptoBot создайте чек и отправьте его в этот диалог! 

• Ton (<a href="https://ton.org/">Toncoin</a>) 
• Btc (<a href="https://bitcoin.org/">Bitcoin</a>)
• Bnb (<a href="https://binance.org/">Binance coin</a>)
• Busd (<a href="https://www.binance.com/en/busd"Binance USD</a>)
• Usdc (<a href="https://www.centre.io/usdc">USD Coin</a>)
• Usdt (<a href="https://tether.to/">Tether</a>)

👉🏻 Отправьте чек</b>:
'''
                await call.message.edit_caption(caption=text, reply_markup=menu.close_markup())
            
            if call.data == 'pay_WM':
                text = f'''🔘 <b>Для совершения пополнения c помощью</b> <a href="https://www.webmoney.ru/">WebMoney</a>, <b>сделайте перевод на указанный кошелёк Wmz, с желаемой суммой пополнения. 

◾️Счет:</b> <code>Z567188509029</code>

<b>📊 Курс WMZ -</b> <code>66.56₽</code> <b>| 1 Штука 

📚 Суммы депозитом меньше в 5 WMZ будут расцениваться как пожертвование проекту.</b>'''
                await call.message.edit_caption(caption=text, reply_markup=menu.close_markup())
            
            if call.data == 'pay_DOGE':
                text = f'''<b>🐶 Для пополнения с помощью Doge coin, следует перевести на определённый адрес криптовалюту Doge. 

◾️Адрес:</b> <code> DC3FBk7q7dqVCziNrycKgQuQhbi4p6woVq</code>
<b>◾️Сумма:</b> <code>Любая</code>

<b>📊 Курс:</b> <code>1 Doge - 0.08624 $ | 5.439 ₽</code>
 
<b>❗️Важно! - Перевод менее 20 Doge, будет рассматриваться как пожертвование проекту!</b>'''
                await call.message.edit_caption(caption=text, reply_markup=menu.close_markup())
            
            if call.data == 'pay_qiwi':
                url, code, phone = await QiwiPay().deposit_qiwi(chat_id)
                text = mes.pay_qiwi.format(number=phone, code=code)
                await call.message.edit_caption(caption=text, reply_markup=menu.pay_qiwi_markup(url=url))
            
            if call.data == 'pay_payok':
                await call.message.edit_caption('Введите сумму: ', reply_markup=menu.close_markup())
                await state.set_state('payment_payok')
            
            if call.data == 'dpayok':
                await call.message.delete()
                await state.finish()

            if call.data == 'promocode':
                await ActivatePromo.promo.set()
                text = '<b>🎁 Введите промокод для его активации:</b>'
                await call.message.answer(text=text, reply_markup=menu.kbcancel)
            

            if call.data == 'referral':
                name = await bot.get_me()
                txxt = """
⭐️ <b><i>Реферальная программа</i></b>

<i>Приглашайте людей в бота по вашей реферальной ссылке и сразу получаете </i><b>1₽</b> <i>за вступления в бота</i>

🔗 <i>Ваша реферальная ссылка:</i> <code>https://t.me/{bot_login}?start={user_id}</code>

◽️<b>Вы пригласили:</b> <code>{referals}</code> <b>чел
◽️Вы заработали:</b> <code>{r_amount}₽</code>

"""
                text = txxt.format(bot_login=name.username,
                                        user_id=chat_id, referals=await amount_referals(chat_id), r_amount=round(float(await amount_referals(chat_id) * 1), 3))
                await call.message.edit_caption(caption=text, reply_markup=menu.gen_ref_kb(chat_id))
            
            if call.data == "why_scam":
                txt = """<b>❗️ В ночь 02.06.2022 года в 0:38 мы получили метку «SCAM».</b> 

<i>Всем вам известно что в нашем боте продаётся такой товар как «Qiwi кошелёк» именно он и стал причиной получения метки на нашего бота. 

Компания brandsecurity.ru занимающейся блокировкой так называемого «пиратского» контента приняла чью то заявку на наш бот. Скорее всего это сделали конкуренты. Так как компания qiwi.com является платёжной системой продажа кошельков запрещена.</i>

<b>Если у вас есть все же сомнения над нашим ботом приглашаем вас в канал отзывов </b><b>(<a href='https://t.me/end_soft'>тыкай</a>)</b>"""
                await call.message.edit_caption(caption=txt, reply_markup=menu.ws_markup())

            if call.data == 'my_purchases':
                markup = await User(chat_id).purchases_history()
                await call.message.edit_caption(caption='Ваши покупки:', reply_markup=markup)
            
            if call.data == 'crypto_curs':
                data = get("https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH,LTC,USDT,DOGE,DOT&tsyms=USD,RUB").json()
                txxt = f'''<b>📈 Валютные котировки:</b>

<b>▪️BTC</b> - {data["BTC"]["USD"]} $ | {data["BTC"]["RUB"]} ₽
<b>▪️ETH</b> - {data["ETH"]["USD"]} $ | {data["ETH"]["RUB"]} ₽
<b>▪️LTC</b> - {data["LTC"]["USD"]} $ | {data["LTC"]["RUB"]} ₽
<b>▪️USDT</b> - {data["USDT"]["USD"]} $ | {data["USDT"]["RUB"]} ₽
<b>▪️DOGE</b> - {data["DOGE"]["USD"]} $ | {data["DOGE"]["RUB"]} ₽
<b>▪️DOT</b> - {data["DOT"]["USD"]} $ | {data["DOT"]["RUB"]} ₽
'''
                await call.message.edit_caption(caption=txxt, reply_markup=menu.back_markup())

            if call.data.split(":")[0] == 'user_purchase':
                text, markup = await Product().info_purchase_history(call.data.split(":")[1])
                await call.message.delete()
                await call.message.answer(text=text, reply_markup=markup)

            if call.data == 'to_close':
                await call.message.delete()
            
            if call.data == 'to_menu':
                text = f'<b>💳 Баланс:</b> {user.balance} RUB'
                await call.message.edit_caption(caption=text, reply_markup=menu.menu_markup())
            
            if call.data == 'cabinet':
                chat_id = call.from_user.id
                text = mes.cabinet.format(user_id=chat_id, login=call.from_user.get_mention(as_html=True), data=User(chat_id).get_days(), balance=User(chat_id).balance)
                await call.message.edit_caption(caption=text, reply_markup=menu.cabinet_markup())
            
            if call.data == 'info':
                chat_id = call.from_user.id
                text = mes.infomation
                
                await call.message.edit_caption(caption=text, reply_markup=menu.help_markup())
                
            if call.data == 'rules_market':
                text = mes.rules
                await call.message.edit_text(text=text, reply_markup=menu.close_markup())
            
            if call.data == "pclient":
                s = await get_user_sum(call.from_user.id)
                if int(s) >= 0:
                    await call.message.edit_caption("""<b>🟩 Вход в чат разрешён! 

📝 Правила:</b>
<i>├ Обман админа - бан 
├ Без тупых вопросов - бан 
├ Спам неадекватное общение - бан 
├ Реклама / упоминание сторонних проектов - бан 
├ Не соблюдение правил магазина - бан 
└ Любой вид скама пользователей чата - бан 

🔗 Ссылка для входа: https://t.me/end_soft</i>""", reply_markup=menu.back_markup())
                else:
                    await call.message.edit_caption("""<b>❌ Вход в чат только для постоянных клиентов 

♦️ Условия входа в чат:</b>
<i>└ Общая сумма пополнений -> 75₽ и более…</i>""",reply_markup=menu.back_markup())
            
            if call.data.split(':')[0] == 'not_bot':
                print(call.data)
                await call.message.delete()
                await call.message.answer('<b>Проверка пройдена!\nНажми /start еще раз.</b>')
                userx = User(str(call.data.split(":")[1]).split("_")[1])
                await userx.update_balance(float(1))
                await bot.send_message(str(call.data.split(":")[1]).split("_")[1], f'<b>💰 Вам начислено</b> <code>1</code>₽ <b>за</b> {call.from_user.get_mention(name="реферала", as_html=True)}')
                await bot.send_message(chat_id=config.config("admin_group"), text=f'''💎 <b>Приглашён новый реферал 

◽️Рефер: {userx.username}
◽️id:</b> <code>{userx.user_id}</code>
➖➖➖➖➖➖
◽️<b>Приглашённый: @{user.username}
◽️Id:</b> <code>{user.user_id}</code>
''')
                
                

            if call.data == 'to_catalog':
                text = f'<b>💳 Баланс:</b> {user.balance} RUB'
                await call.message.edit_caption(caption=text, reply_markup=await Catalog().get_menu())

            if call.data.split(":")[0] == 'catalog':
                text = f'<b>💳 Баланс:</b> {user.balance} RUB\n<b>🛍 Выберите категорию:</b>'
                if call.data.split(":")[1] == 'proxy':
                    text = f'<b>💳 Баланс:</b> {user.balance} RUB\n<b>Выберите тип прокси:</b>'
                    markup = Proxy().proxy_type_menu()
                elif call.data.split(":")[1] == 'cheating':
                    text = f'<b>💳 Баланс:</b> {user.balance} RUB\n<b>Выберите площадку для накрутки:</b>'
                    markup = await SMMPanel().cheating_menu()
                else:
                    markup = await SubCatalog().get_subcategory_menu(call.data.split(":")[1])
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'subcatalog':
                markup = await Product().get_product_menu(call.data.split(":")[1])
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                            reply_markup=markup)

            if call.data.split(":")[0] == 'product':
                info = await Product().get_product(call.data.split(":")[1])
                products = await Product().get_amount_products(call.data.split(":")[1])
                text = mes.product.format(name = info[2], price = info[3],
                            balance = user.balance, description = info[4], amount_product = products)
                markup = await Product().buy_product_markup(call.data.split(":")[1])
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'product_buy':
                products = await Product().get_amount_products(call.data.split(":")[1])
                if int(products) > 0:
                    markup = await Product().get_buy_menu(call.data.split(":")[1])
                    await call.message.edit_reply_markup(reply_markup=markup)
                else:
                    await call.answer('Похоже товара нет в наличии, попробуйте позже...')
            
            if call.data.split(":")[0] == "product_ask":
                Name = await Product().get_product(call.data.split(":")[1])
                txtt = f"""<b>❓Вы можете задать вопрос по поводу товара {Name[2]} 

Важно:</b> <i>не пишите чушь, не пишите по поводу замен, не пишите поводу своих предложений (например рекламы), пишите 1 сообщением выражая свой смысл</i>

<b>📧 Введите текст...</b>"""
                await call.message.edit_caption(txtt, parse_mode="HTML")
                await state.set_state('asksend')
                await state.update_data(pname=Name[2])
            
            if call.data.split(":")[0] == "lr":
                Name = await Product().get_product(call.data.split(":")[1])
                txtt = '''<b>❗️ Важно при написании отзыва опишите:</b>

<i>- Товар 
- Его валидность 
- Понравился ли он вам 
- Отзыв о сервисе Cloud shop

📝 Введите текст отзыва:</i>
'''
                await call.message.edit_text(txtt, parse_mode="HTML")
                await state.set_state('sendreview')
                await state.update_data(pname=Name[2])

            if call.data.split(':')[0] == 'buy_menu_update':
                products = await Product().get_amount_products(call.data.split(":")[1])
                product_id, amount, price, update = call.data.split(":")[1], int(call.data.split(":")[2]), \
                    call.data.split(":")[3], int(call.data.split(":")[4])
                
                if (amount + update) > 0:
                    if (amount + update) <= 25:
                        if products >= amount + update:
                            markup = await Product().get_buy_menu(product_id, amount, price, update)
                            await call.message.edit_reply_markup(reply_markup=markup)
                        else:
                            await call.answer('❕ Такого количества товара больше нет')
                    else:
                        await call.answer('❕ Максимально за раз можно купить 25 шт')
                else:
                    await call.answer('❕ Минимальное количество для покупки 1 шт.')    

            if call.data.split(":")[0] == 'buy_product':
                product_id, amount, price = call.data.split(":")[1], int(call.data.split(":")[2]), float(call.data.split(":")[3])
                info = await Product().get_product(call.data.split(":")[1])
                if price <= float(user.balance):
                    products = await Product().get_amount_products(product_id)
                    if amount <= products:
                        await user.update_balance(-price)
                        await user.up_purchases(1)
                        file_name = await Product().get_products(product_id, amount)
                        with open(file=file_name, mode='rb') as txt:
                            await call.message.answer(text=mes.access_purchase)
                            await call.message.answer_document(document=txt, caption='Ваш товар')
                            await call.message.answer(f'''🎉 <b>Поздравляем с покупкой товара {info[2]}</b>

<i>Предлагаем вам оставить отзыв и получить маленький бонус от администрации! 

Важно: опишите что вы купили, понравился ли вам товар, рабочий ли он на момент покупки! 
</i>
''', reply_markup=menu.gen_cb_kb(call.data.split(":")[1]))

                        text = f'''<b>🛍 Куплен товар 

◽️Пользователь: @{user.username}
◽️ID: {chat_id}
◽️Название товара: {info[2]}
◽️Сумма покупки: {price} руб.
◽️Количество товара: {products} шт.</b>
'''
                        product = open(file_name, 'rb')
                        await bot.send_document(chat_id=config.config("admin_group"), document=product, caption=text)

                        with open(file_name, 'r', encoding='UTF-8') as txt:
                            for i in txt:
                                await Product().write_history(chat_id, product_id, i)
                        os.remove(file_name)

                    else:
                        await call.answer('Товара в таком количестве больше нет!')
                else:
                    await call.answer('Пополните баланс!')

            if call.data.split(":")[0] == 'proxy_type':
                markup = Proxy().proxy_time_menu(call.data.split(":")[1])
                text = '<b>Выберите время аренды прокси:</b>'
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'proxy_time':
                markup = Proxy().proxy_country_menu(call.data.split(":")[1], call.data.split(":")[2])
                text = '<b>Выберите страну аренды прокси:</b>'
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'proxy_country':
                markup = Proxy().proxy_count_menu(call.data.split(":")[1], call.data.split(":")[2], call.data.split(":")[3])
                text = '<b>Выберите количество проксей для покупки:</b>'
                await call.message.edit_caption(caption=text, reply_markup=markup)
            
            if call.data.split(":")[0] == 'proxy_сount':
                text, markup = await Proxy().proxy_buy_info(call.data.split(":")[1], call.data.split(":")[2], 
                                call.data.split(":")[3], call.data.split(":")[4])
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'proxy_buy':
                msg = await call.message.edit_caption(caption='<b>♻️ Подождите...</b>', reply_markup=menu.close_markup())
                await Proxy().buy_proxy(bot, chat_id, call.data.split(":")[1], call.data.split(":")[2], call.data.split(":")[3],
                                    call.data.split(":")[4], call.data.split(":")[5], msg.message_id)

            if call.data.split(":")[0] == 'cheat_serivce':
                text = '<b> Выберите тип накрутки:</b>'
                markup = await SMMPanel().cheat_type_menu(call.data.split(":")[1])
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'cheat_type':
                text = '<b> Выберите нужное вам:</b>'
                markup = await SMMPanel().cheat_order_menu(call.data.split(":")[1], call.data.split(":")[2])
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'cheat_order':
                text = await SMMPanel().cheat_messages(call.data.split(":")[1], call.data.split(":")[2],
                        call.data.split(":")[3])
                markup = await SMMPanel().cheat_buy_menu(call.data.split(":")[1], call.data.split(":")[2],
                        call.data.split(":")[3])
                await call.message.edit_caption(caption=text, reply_markup=markup)

            if call.data.split(":")[0] == 'cheat_buy_update':
                service, cheat_type, order, amount, price, update = call.data.split(":")[1], call.data.split(":")[2], \
                    call.data.split(":")[3], int(call.data.split(":")[4]), float(call.data.split(":")[5]), int(call.data.split(":")[6])
                orders = SMMPanel().cheat.get(f'{service}').get(cheat_type)
                order_info = orders.get(order)
                
                if (amount + update) >= int(order_info.get('min')):
                    if int(order_info.get('max')) >= amount + update:
                        markup = await SMMPanel().cheat_buy_menu(service, cheat_type, order, amount, price, update)
                        await call.message.edit_reply_markup(reply_markup=markup)
                    else:
                        await call.answer(f'❕ Максимально за раз можно купить {order_info.get("max")}')
                else:
                    await call.answer(f'❕ Минимальное количество для покупки {order_info.get("min")}')
                await call.answer()

            if call.data.split(":")[0] == 'cheat_buy':
                text = f'<b>❗️Внимание вводите ссылку на услугу правильно!\nПри неправильном вводе ваша услуга будет отменена без возврата средств.</b>'
                service, cheat_type, order, amount, price = call.data.split(":")[1], call.data.split(":")[2], \
                    call.data.split(":")[3], call.data.split(":")[4], call.data.split(":")[5]
                await BuyCheating.link.set()
                async with state.proxy() as data:
                    data['service'] = service
                    data['type'] = cheat_type
                    data['order'] = order
                    data['count'] = amount
                await call.message.edit_caption(caption=text, reply_markup=menu.close_markup())
                await call.message.answer("<b>🔗 Отправьте ссылку куда будем накручивать:</b>")

            if call.data.split(":")[0] == 'cheat_count':
                await call.message.delete()
                service, cheat_type, order = call.data.split(":")[1], call.data.split(":")[2], \
                    call.data.split(":")[3]
                await BuyCheating.count.set()
                async with state.proxy() as data:
                    data['service'] = service
                    data['type'] = cheat_type
                    data['order'] = order
                await call.message.answer('<b>Введите количество услуги:</b>')


@vip.message_handler(state='payment_payok')
async def payment_payok2(m: types.Message, state: FSMContext):
    try:
        info = f'Пополнение_{randint(111, 999)}'
        markup = await menu.payok_kb(float(m.text), f'{m.from_user.id}_{randint(111, 999)}', info)
        await m.answer(f'''💰 <b>Способ пополнения «Payok.io»</b>

<i>- Qiwi пополнение 
- CARD пополнение 
- Биткоин 
- Мегафон 
- Doge и другие криптовалюты</i> 

💵 <b>Сумма пополнения:</b> <code>{float(m.text)} ₽</code>
''', reply_markup=markup, parse_mode="HTML")
        await state.set_state('paycheck')
        await state.update_data(sumx=float(m.text), desc=info)
    except ValueError:
        await m.answer('Неверный ввод.', reply_markup=menu.close_markup())
        await state.finish()



