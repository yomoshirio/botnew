from aiogram import types
from aiogram.dispatcher import FSMContext
import time
import random

from loader import vip, bot
from utils import config
from data import get_users_list
from states import EmailText, EmailPhoto
from keyboards import inline as menu, defaut as key

@vip.callback_query_handler(text='admin_sending')
async def adm_sending(call: types.CallbackQuery):
    if str(call.from_user.id) in str(config.config('admin_id')):
        await bot.send_message(chat_id = call.from_user.id,
                    text = 'Выберите тип рассылки', reply_markup = menu.adm_sending())

@vip.callback_query_handler(text='email_sending_text')
async def adm_sending_text(call: types.CallbackQuery):
    await EmailText.text.set()
    await call.message.answer('Введите текст рассылки:')

@vip.message_handler(state=EmailText.text)
async def adm_sending_text_1(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = msg.parse_entities()

        await msg.answer(data['text'], parse_mode='html')

        await EmailText.next()
        await bot.send_message(chat_id=msg.from_user.id,
            text='Выбери дальнейшее действие',
            reply_markup=key.admin_sending())


@vip.message_handler(state=EmailText.action)
async def admin_sending_messages_2(msg: types.Message, state: FSMContext):
    chat_id = msg.from_user.id

    if msg.text in key.admin_sending_btn:
        if msg.text == key.admin_sending_btn[0]: # Начать
            users = get_users_list()
            start_time = time.time()
            amount_message = 0
            amount_bad = 0

            async with state.proxy() as data:
                text = data['text']
            await state.finish()
            try:
                await bot.send_message(chat_id=chat_id,
                    text=f'✅ Вы запустили рассылку', reply_markup=key.main_menu())
            except: pass

            for i in range(len(users)):
                try:
                    await bot.send_message(users[i][0], text, parse_mode='html',
                                reply_markup = menu.close_markup())
                    amount_message += 1
                except:
                    amount_bad += 1
            
            sending_time = time.time() - start_time

            try:
                await bot.send_message(chat_id=chat_id,
                    text=f'✅ Рассылка успешно закончена\n'
                    f'📩 Отправлено: {amount_message}\n'
                    f'📮 Не отправлено: {amount_bad}\n'
                    f'🕐 Время выполнения рассылки - {sending_time} секунд')
                await state.finish()              
            except:pass
        elif msg.text == key.admin_sending_btn[1]:
            await bot.send_message(chat_id = msg.from_user.id, 
                text='Рассылка отменена', reply_markup=key.main_menu())
            await state.finish()
            
        else:   
            await bot.send_message(chat_id = msg.from_user.id, 
                text='Неверная команда, повторите попытку', reply_markup=key.main_menu())

@vip.callback_query_handler(text='email_sending_photo')
async def adm_sending_photo(call: types.CallbackQuery):
    await EmailPhoto.photo.set()
    await bot.send_message(chat_id = call.from_user.id,
                text = '<b>Пришлите боту фото, только фото!</b>')


@vip.message_handler(state=EmailPhoto.photo, content_types=['photo'])
async def email_sending_photo_1(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['photo'] = random.randint(111111111, 999999999)

        await msg.photo[-1].download(f'utils/photos/{data["photo"]}.jpg')
        await EmailPhoto.next()
        await msg.answer('Введите текст рассылки')
    except:
        await state.finish()
        await msg.answer('🤬 <b>Чето наебнулось</b>')


@vip.message_handler(state=EmailPhoto.text)
async def email_sending_photo_2(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = msg.parse_entities()

            with open(f'utils/photos/{data["photo"]}.jpg', 'rb') as photo:

                await msg.answer_photo(photo, data['text'], parse_mode='html')

            await EmailPhoto.next()
            await msg.answer('Выбери дальнейшее действие', reply_markup=key.admin_sending())
    except:
        await state.finish()
        await msg.answer('ошибочка...')

@vip.message_handler(state=EmailPhoto.action)
async def email_sending_photo_3(msg: types.Message, state: FSMContext):
    chat_id = msg.from_user.id
    try:
        if msg.text in key.admin_sending_btn:
            if msg.text == key.admin_sending_btn[0]: # Начать
                users = get_users_list()
                start_time = time.time()
                amount_message = 0
                amount_bad = 0

                async with state.proxy() as data:
                    photo_name = data["photo"]
                    text = data["text"]
                await state.finish()
                try:
                    await bot.send_message(chat_id=chat_id,
                        text=f'✅ Вы запустили рассылку',reply_markup=key.main_menu())
                except: pass

                for i in range(len(users)):
                    try:
                        with open(f'utils/photos/{photo_name}.jpg', 'rb') as photo:
                            await bot.send_photo(chat_id=users[i][0],
                                photo=photo, caption=text)
                        amount_message += 1
                    except:
                        amount_bad += 1
                
                sending_time = time.time() - start_time

                try:
                    await bot.send_message(chat_id=chat_id,
                        text=f'✅ Рассылка успешно закончена\n'
                        f'📩 Отправлено: {amount_message}\n'
                        f'📮 Не отправлено: {amount_bad}\n'
                        f'🕐 Время выполнения рассылки - {sending_time} секунд')              
                except:pass
                
            elif msg.text == key.admin_sending_btn[1]:
                await state.finish()
                await bot.send_message(msg.from_user.id, 
                    text='Рассылка отменена', reply_markup=key.main_menu())
                await bot.send_message(msg.from_user.id, 
                    text='👑 <b>Админ панель Cloud shop</b>', reply_markup=menu.admin_markup())
        else:   
            await bot.send_message(msg.from_user.id, 
                text='Не верная команда, повторите попытку', 
                reply_markup=key.admin_sending())

    except:
        await state.finish()
        await bot.send_message(chat_id=msg.from_user.id,
            text='Ошибка в рассылке')

