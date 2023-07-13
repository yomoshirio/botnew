from aiogram import types
from aiogram.dispatcher import FSMContext
import re 

from loader import vip, bot
from states import ActivatePromo, BuyCheating
from keyboards import inline as menu
from data import User, get_promo, activate_promo, delete_promo
from utils import config, SMMPanelAPI, SMMPanel

@vip.message_handler(state=BuyCheating.count)
async def cheat_link_states(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            service = data['service']
            cheat_type = data['type']
            order = data['order']
        orders = SMMPanel().cheat.get(f'{service}').get(cheat_type)
        order_info = orders.get(order)
        if int(msg.text) >= int(order_info.get('min')) and int(msg.text) <= int(order_info.get('max')):
            async with state.proxy() as data:
                data['count'] = msg.text
            price = float(order_info.get('price')) * int(msg.text)
            text = f"""
<b>📛 Важно!
Вводить правильно ссылку на нужный вам вид услуги! При неправильном вводе - у вас пропадают деньги!</b>

<b>💈 Cервис:</b> {SMMPanel().cheat_service_name(service)} {SMMPanel().cheat_type_name(cheat_type)}
<b>🧿 Название:</b> {order_info.get('name')}
<b>🧿 Количество:</b> {msg.text}
<b>💳 Цена:</b> {price} RUB
            """
            await msg.answer(text=text)
            await msg.answer(text='<b>🔗 <b>Введите ссылку:</b></b>')
            await BuyCheating.next()
        else:
            await msg.answer(f'🚫 Не правильное количество!\nДоступно: от {order_info.get("min")} до {order_info.get("max")}')
            await state.finish()
    else:
        await msg.answer(f'Количество нужно вводить в числах!')
        await state.finish()

@vip.message_handler(state=BuyCheating.link)
async def cheat_link_states(msg: types.Message, state: FSMContext):
    link = re.search("(?P<url>https?://[^\s]+)", msg.text)
    if link != None:
        link = link.group()
        async with state.proxy() as data:
            data['link'] = link
            service = data['service']
            cheat_type = data['type']
            order = data['order']
            count = data['count']
        
        orders = SMMPanel().cheat.get(f'{service}').get(cheat_type)
        order_info = orders.get(order)
        price = float(order_info.get('price')) * int(count)
        await msg.answer(f'''<b>☑️ Подтвердите заказ</b> 

<i>🔗 Ссылка:</i> <code>{link}</code>
<i>📌 Количество:</i> <code>{count}</code>
<i>💸 Цена:</i> <code>{price}</code>₽

<b>Для заказа отправьте «+» боту!</b>''')
        await BuyCheating.next()
    else:
        await state.finish()
        await msg.answer('<b>❌ Это не ссылка!</b>')

@vip.message_handler(state=BuyCheating.confirm)
async def cheat_confirm(msg: types.Message, state: FSMContext):
    if msg.text.startswith("+"):
        async with state.proxy() as data:
            service = data['service']
            cheat_type = data['type']
            order = data['order']
            count = data['count']
            link = data['link']
        orders = SMMPanel().cheat.get(f'{service}').get(cheat_type)
        order_info = orders.get(order)
        price = float(order_info.get('price')) * int(count)
        if price <= float(User(msg.from_user.id).balance):
            order = await SMMPanelAPI().add_order(service_id=order, link=link, count=count)
            if order != 'no_order':
                await User(msg.from_user.id).update_balance(-price)
                await msg.answer(f"""
<b>⭐️ Ваш заказ успешно начал выполнение</b> 

<i>🔧 Услуга:</i> <code>{order_info.get('name')}</code>
<i>📎 Количество:</i> <code>{count}</code>
<i>💸 Цена покупки:</i> <code>{price}</code>₽
            """, reply_markup=menu.close_markup())
                
                await bot.send_message(chat_id=config.config('admin_group'),
                            text=f"""
<b>⭐️ Куплена накрутка!

◽️ Cервис:</b> <code>{SMMPanel().cheat_service_name(service)} | {SMMPanel().cheat_type_name(cheat_type)}</code>
<b>◽️ Название:</b> <code>{order_info.get('name')}</code>
<b>◽️ Количество:</b> <code>{count}</code>
<b>◽️ Цена:</b> <code>{price} RUB</code>
<b>◽️ Покупатель:</b> @{User(msg.from_user.id).username}
<b>◽️ Ссылка:</b> <code>{link}</code>
                            """, disable_notification=True)
                await SMMPanel().cheat_logs(msg.from_user.id, service, SMMPanel().cheat_service_name(service), 
                        cheat_type, order, order_info.get('name'), link, count, price)
            else:
                await msg.answer('❗️ <b>Tехнические неполадки, попробуйте позже или напишите в поддержку</b>\n\n⚠️ Возможно на эту ссылку уже стоит заказ - нужно подождать')
        else:
            await msg.answer('<b>💰 <b>Пополните баланс!</b></b>')
    else:
        await msg.answer('🚫 <b>Действие отменено!</b>')
    await state.finish()


@vip.message_handler(state=ActivatePromo.promo)
async def user_promo(msg: types.Message, state: FSMContext):
    i = await get_promo(msg.text)
    if i != None:
        if int(i[3]) > 0:
            if str(msg.from_user.id) not in i[4].split(','):
                await activate_promo(msg.from_user.id, msg.text)
                await User(msg.from_user.id).update_balance(float(i[2]))

                await msg.answer(f'🤑 <b>Вам начисленно + {i[2]}₽</b>')
                await bot.send_message(chat_id=config.config('admin_group'),
                                    text=f'<b>🎁 Активация промокода:</b>\n\n'
                                         f'<b>Пользователь:</b> {msg.from_user.get_mention(as_html=True)} | {msg.from_user.id}\n\n'
                                         f'<b>Промокод:</b> {msg.text} | <b>Сумма:</b> {i[2]} RUB')
            else:
                await msg.answer(f'Вы уже активировали этот промокод')
        else:
            await delete_promo(msg.text)
            await msg.answer(f'😭 <b>Промокод закончился</b>')
    else:
        await msg.answer(f'😬 <b>Нет такого промокода</b>')
    await state.finish()