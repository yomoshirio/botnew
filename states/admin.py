from aiogram.dispatcher.filters.state import State, StatesGroup

class AdmSearch(StatesGroup):
    user_id = State()

class AdmGiveBalance(StatesGroup):
    user_id = State()
    amount = State()

class EmailText(StatesGroup):
    text = State()
    action = State()

class EmailPhoto(StatesGroup):
    photo = State()
    text = State()
    action = State()

class CreatePromo(StatesGroup):
    name = State()
    money = State()
    amount = State()

class QiwiChange(StatesGroup):
    number = State()
    token = State()

class HuiChange(StatesGroup):
    persent = State()
    nakrutka = State()

class PercentChange(StatesGroup):
    percent = State()



class UrlChange(StatesGroup):
    text = State()
    url = State()
    url_id = State()


class UrlDelete(StatesGroup):
    url = State()