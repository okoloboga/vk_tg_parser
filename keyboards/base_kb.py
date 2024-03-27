from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON


"""Главное меню"""
button_tasks = KeyboardButton(text=LEXICON['tasks'])
#button_schedule = KeyboardButton(text=LEXICON['schedule'])
button_parse_now = KeyboardButton(text=LEXICON['parse_now'])

main_kb_builder = ReplyKeyboardBuilder()
main_kb_builder.row(button_tasks, width=1)
#main_kb_builder.row(button_schedule, width=1)
main_kb_builder.row(button_parse_now, width=1)

main_kb: ReplyKeyboardMarkup = main_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)

"""Добавить/Удалить адрес сообщества"""
button_add = KeyboardButton(text=LEXICON['add'])
button_delete = KeyboardButton(text=LEXICON['delete'])

add_public_kb_builder = ReplyKeyboardBuilder()
add_public_kb_builder.row(button_add, button_delete, width=2)

add_public_kb: ReplyKeyboardMarkup = add_public_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
