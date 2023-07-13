from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import vip, bot
from states import AdmSearch, AdmGiveBalance, UrlChange, UrlDelete
from data import User, get_user
from data import add_new_group, add_select_groups, delete_groups
from keyboards import inline as menu

@vip.callback_query_handler(text='admin_search')
async def adm_search(call: types.CallbackQuery):
    await AdmSearch.user_id.set()
    await bot.send_message(chat_id = call.from_user.id, 
                text = 'Введите user_id пользователя:')



@vip.callback_query_handler(text='creareurl')
async def create(call: types.CallbackQuery):
    await UrlChange.text.set()
    await bot.send_message(chat_id = call.from_user.id, 
                text = 'Введите текст')


@vip.message_handler(state = UrlChange.text)
async def create2(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = msg.parse_entities()
        await UrlChange.url.set()
        await bot.send_message(chat_id = msg.from_user.id, 
                    text = 'Введите url')




@vip.message_handler(state = UrlChange.url)
async def create3(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = msg.parse_entities()
        await UrlChange.url_id.set()
        await bot.send_message(chat_id = msg.from_user.id, 
                    text = 'Введите id')



@vip.message_handler(state = UrlChange.url_id)
async def create4(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url_id'] = msg.parse_entities()
        try:
            await add_new_group(data['text'], data['url'], data['url_id'])
            await msg.answer('Ссылка успешно добавлена!')
            await state.finish()
        except:
            await msg.answer('Такая ссылка уже существует!')
            await state.finish()
            


@vip.callback_query_handler(text='deleteurl')
async def delete(call: types.CallbackQuery):
    await UrlDelete.url.set()
    await bot.send_message(chat_id = call.from_user.id, 
                text = 'Введите url')


@vip.message_handler(state = UrlDelete.url) 
async def delete2(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = msg.parse_entities()
        await delete_groups(data['url'])
        await msg.answer('Ссылка успешно удалена!')
        await state.finish()



@vip.callback_query_handler(text='showurls')
async def showurls(call: types.CallbackQuery):
    spisok = add_select_groups()
    url_id = [url_id[2] for url_id in spisok]
    url = [url[1] for url in spisok]
    text_url = [text_url[0] for text_url in spisok]
    for i in range(len(spisok)):    
        await bot.send_message(chat_id = call.from_user.id, 
                    text = f'Text: {text_url[i]} Url: {url[i]} ID: {url_id[i]}')





@vip.message_handler(state = AdmSearch.user_id)
async def adm_search2(msg: types.Message, state: FSMContext):
    try:
        if await get_user(msg.text) == True:
            user = User(msg.text)
            await bot.send_message(chat_id = msg.from_user.id,
                    text = f'<b>👤 Пользователь:</b> @{user.username}\n\n'
                           f'<b>💳 Баланс:</b> <code>{user.balance}</code> <b>RUB</b>\n\n'
                           f'<b>⚙️ Статус:</b> <code>{user.status}</code>\n\n'
                           f'<b>♻️ Количество покупок:</b> <code>{user.purchases}</code>\n\n'
                           f'<b>💢 Бан:</b> <code>{user.ban}</code> (yes - значит в бане)\n\n'
                           f'<b>🕰 Дата регистрации:</b> <code>{user.date[:10]}</code>',
                    reply_markup = menu.admin_user_menu(msg.text))
        else:
            await msg.answer('💢 Я не нашел такого пользователя')
        await state.finish()
    except:
        await state.finish()
        await msg.answer('💢 Ошибка, чето наебнулось')


@vip.message_handler(state = AdmGiveBalance.amount)
async def adm_give_balance(msg: types.Message, state: FSMContext):
    try:
        if msg.text.isdigit() == True:
            amount = float(msg.text)
            async with state.proxy() as data:
                    user_id = data['user_id']
            await User(user_id).up_balance(amount)
            await bot.send_message(chat_id = msg.from_user.id,
                    text = '💳 <b>Баланс успешно изменен</b>', reply_markup = menu.close_markup())
        else:
            await msg.answer('Ввводи число!')
        await state.finish()
    except:
        await state.finish()
        await msg.answer('💢 Ошибка')

