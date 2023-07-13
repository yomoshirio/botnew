from aiogram.dispatcher.filters.state import State, StatesGroup

class CreateCatalog(StatesGroup):
    name = State()

class CreateSubCatalog(StatesGroup):
    category = State()
    name = State()

class CreateProduct(StatesGroup):
    subcategory_id = State()
    name = State()
    price = State()
    description = State()

class AdminDownloadProduct(StatesGroup):
    product_id = State()
    file = State()
    confirm = State()