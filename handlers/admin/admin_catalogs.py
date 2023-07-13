from aiogram import types
from aiogram.dispatcher import FSMContext
from random import randint

from loader import vip, bot
from keyboards import inline as menu
from states import CreateCatalog, CreateSubCatalog, CreateProduct, AdminDownloadProduct
from utils import Catalog, SubCatalog, Product

@vip.callback_query_handler(text='admin_catalogs')
async def adm_catalogs(call: types.CallbackQuery):
    await bot.send_message(chat_id = call.from_user.id, 
                text = 'Выберите то, что хотите изменить', reply_markup = menu.adm_catalog_markup())

@vip.callback_query_handler(text = 'admin_catalog')
async def adm_catalog(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(chat_id = call.from_user.id,
                    text = 'Выберите каталог', reply_markup = menu.adm_catalog_edit())

@vip.callback_query_handler(text = 'adm_act_catalog')
async def adm_catalog_act(call: types.CallbackQuery):
    markup = await Catalog().adm_catalog_menu()
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(chat_id = call.from_user.id,
                    text = '🎛 Выберите каталог', reply_markup = markup)

@vip.callback_query_handler(text = 'adm_create_catalog')
async def adm_catalog_create(call: types.CallbackQuery):
    await CreateCatalog.name.set()
    await call.message.answer('📝 <b>Введите название нового каталога</b>')

@vip.message_handler(state = CreateCatalog.name)
async def adm_catalog_create_2(msg: types.Message, state: FSMContext):
    await state.finish()
    await Catalog().create_catalog(msg.text)
    await msg.answer(f'✅ <b>Каталог: "{msg.text}", успешно создан</b>')

@vip.callback_query_handler(text = 'admin_subcatalog')
async def adm_subcatalog(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(chat_id = call.from_user.id,
                    text = '🎛 <b>Выберите каталог</b>', reply_markup = menu.adm_subcatalog_edit())

@vip.callback_query_handler(text = 'adm_act_subcatalog')
async def adm_subcatalog_act(call: types.CallbackQuery):
    markup = await SubCatalog().adm_subcatalog_menu()
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(chat_id = call.from_user.id,
                    text = '🗂 Выберите подкаталог', reply_markup = markup)

@vip.callback_query_handler(text = 'adm_create_subcatalog')
async def adm_subcatalog_create(call: types.CallbackQuery):
    await CreateSubCatalog.category.set()
    markup = await Catalog().adm_catalog_menu()
    await call.message.answer('🎛 <b>Выберите категорию, в которой нужно создать подкаталог:</b>', reply_markup = markup)

@vip.callback_query_handler(text = 'admin_product')
async def admin_product(call: types.CallbackQuery):
    await call.message.answer('🔎 Выбери действие', reply_markup = menu.adm_product_edit())

@vip.callback_query_handler(text = 'adm_act_product')
async def admin_product_act(call: types.CallbackQuery):
    markup = await Product().adm_product_menu()
    await call.message.answer('📦 Активные товары', reply_markup = markup)

@vip.message_handler(commands=['adm_create'])
async def admin_handler(msg: types.Message):
    await msg.answer('👑 <b>Админ панель Cloud shop</b>', reply_markup=menu.admin_markup())

@vip.callback_query_handler(text = 'adm_create_product')
async def adm_create_product(call: types.CallbackQuery):
    await CreateProduct.subcategory_id.set()
    markup = await SubCatalog().adm_subcatalog_menu()
    await call.message.answer('🔎 Выберите подкаталог, в котором создать товар', reply_markup = markup)

@vip.callback_query_handler(state = CreateSubCatalog.category)
async def adm_create_subcatalog_2(call: types.CallbackQuery, state: FSMContext):
    category_id = call.data.split(":")[1]
    async with state.proxy() as data:
        data['category'] = category_id
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('💬 Введите название подкаталога:')
    await CreateSubCatalog.next()

@vip.message_handler(state = CreateSubCatalog.name)
async def adm_subcatalog_create_3(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        category_id = data['category']
    await SubCatalog().create_subcatalog(category_id, msg.text)
    await msg.answer(f'🗂 Подкатегория "{msg.text}" успено создана')
    await state.finish()

@vip.callback_query_handler(state = CreateProduct.subcategory_id)
async def adm_product_create(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
    category_id = call.data.split(":")[1]
    async with state.proxy() as data:
        data['subcategory_id'] = category_id
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('📦 <b>Введите название товара</b>')
    await CreateProduct.next()

@vip.message_handler(state = CreateProduct.name)
async def adm_product_create_2(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await msg.answer('💰 <b>Введите цену на товар за 1 единицу:</b>')
    await CreateProduct.next()

@vip.message_handler(state = CreateProduct.price)
async def adm_product_create_3(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = msg.text
    await msg.answer('📖 <b>Введите описание к товару:</b>')
    await CreateProduct.next()

@vip.message_handler(state = CreateProduct.description)
async def adm_product_create_4(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        subcatalog = data['subcategory_id']
        name = data['name']
        price = data['price']
    await Product().create_product(subcatalog, name, price, msg.text)
    await msg.answer(f'☑️ <b>Товар {name} успешно создан</b>', reply_markup = menu.close_markup())
    await state.finish()


@vip.message_handler(state = AdminDownloadProduct.file, content_types = ['document'])
async def admin_download_product(msg: types.Message, state: FSMContext):
    file = f'utils/docs/down_{randint(111, 999)}.txt'
    await msg.document.download(file)
    async with state.proxy() as data:
        data['file'] = file

    await msg.answer('🤖 Для подтверждения загрузки, отправь «+»')
    await AdminDownloadProduct.next()

@vip.message_handler(state = AdminDownloadProduct.confirm)
async def admin_download_product_2(msg: types.Message, state: FSMContext):
    if msg.text == '+':
        async with state.proxy() as data:
            product_id = data['product_id']
            file = data['file']

        info = await Product().upload_product(product_id, file)
        await msg.answer(f'✅ Загружено: {info[0]}\n ❌Ошибок: {info[1]}')
        await state.finish()
    else:
        await state.finish()
        await msg.answer('Отменено!')