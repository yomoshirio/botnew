from aiogram import types

admin_sending_btn = [
    '✅ Начать',
    '💢 Отмена',
]


def admin_sending():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        admin_sending_btn[0],
        admin_sending_btn[1],
    )

    return markup