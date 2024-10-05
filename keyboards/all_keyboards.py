from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins

def main_kb(user_telegram_id: int):
    buttons = ["👤 Мой профиль"]
    return generate_kb(user_telegram_id, buttons)

def home_page_kb(user_telegram_id: int):
    buttons = ["🔙 Назад"]
    return generate_kb(user_telegram_id, buttons)

def generate_kb(user_telegram_id: int, buttons: list) -> ReplyKeyboardMarkup:
    kb_list = []
    for button in buttons:
        kb_list.append([KeyboardButton(text=button)])
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )