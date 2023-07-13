from aiogram import types

shop_menu_btn = [
    '🛒 Главное меню',
    '🖥 Кабинет',
    '📜 Информация',
]


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        shop_menu_btn[0],
        #shop_menu_btn[1],
        #shop_menu_btn[2],
    )
    
    markup.add("📩 Sakura sms", "🔓 Hyper Store")
    
    return markup
