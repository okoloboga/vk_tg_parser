import asyncio
import pandas as pd

from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from keyboards.base_kb import main_kb
from lexicon.lexicon import LEXICON

router = Router()


# Обработка команды СТАРТ вне состояний
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Просмотреть/добавить <b>сообщества</b> для парсинга\n\n'
                              'Настроить <b>расписание</b> парсинга\n\n'
                              'Собрать данные <b>сейчас</b>',
                         reply_markup=main_kb)


# Обработка нажатия кнопки ВЫСЛАТЬ ДАННЫЕ
@router.message(F.text == LEXICON['send_now'], StateFilter(default_state))
async def process_parse_now_button(message: Message, bot: Bot):
    tg_frame = pd.read_csv('tg_channels.csv').values.tolist()
    vk_frame = pd.read_csv('vk_publics.csv').values.tolist()
    for line in tg_frame:
        await bot.send_message(chat_id='-1002089059378', text=f'Канал: {line[1]}\n'
                                                              f'Ссылка на пост: https://t.me/{line[2]}/{line[4]}\n\n'
                                                              f'{line[6]}')
    for line in vk_frame:
        await bot.send_message(chat_id='-1002089059378', text=f'Сообщество: {line[2]}\n'
                                                              f'Ссылка на пост: {line[3]}\n\n'
                                                              f'{line[5]}')
    await message.answer(text=LEXICON['complete'])


# Обработка /cancel вне состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего!',
                         reply_markup=main_kb)


# Обработка команды СТАРТ в состояниях
@router.message(CommandStart(), ~StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Закончи или отмени\n'
                              'действие /cancel',
                         reply_markup=main_kb)


# Обработка /cancel вне состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text='Отменять нечего!',
                         reply_markup=main_kb)
    await state.clear()


# Обработка /cancel в состояниях
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text='Отменено!',
                         reply_markup=main_kb)
    await state.clear()
