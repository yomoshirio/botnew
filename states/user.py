from aiogram.dispatcher.filters.state import State, StatesGroup

class ActivatePromo(StatesGroup):
    promo = State()

class BuyCheating(StatesGroup):
    service = State()
    type = State()
    order = State()
    count = State()
    link = State()
    confirm = State()
