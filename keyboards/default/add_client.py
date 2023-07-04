from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



add_client_markup = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="Mijoz qo‘shish")
        ]
    ],
    resize_keyboard=True
)

confirm_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Tasdiqlayman"),
            KeyboardButton(text="Bekor qilish")
        ]
    ],
    resize_keyboard=True
)