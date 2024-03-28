import asyncio
import json

from pathlib import Path
from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, FSInputFile
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
@router.message(F.text==LEXICON['parse_now'], StateFilter(default_state))
async def process_parse_now_button(message: Message, bot: Bot):
    await message.answer(text=LEXICON['in_process'])
    await asyncio.sleep(5)
    tg_channels = FSInputFile('tg_channels.xlsx')
    vk_publics = FSInputFile('vk_publics.xlsx')
    await bot.send_document(chat_id='1872453368', document=tg_channels)
    await bot.send_document(chat_id='1872453368', document=vk_publics,
                            reply_markup=main_kb)


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





