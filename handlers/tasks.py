import json

from pathlib import Path
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from keyboards.base_kb import add_public_kb
from states.states import FSMMain
from filters.filters import IsAddDelete

router = Router()


# Переход в Задания, изменение сомтояния, ожидание
@router.message(F.text == LEXICON['tasks'], StateFilter(default_state))
async def process_task_button(message: Message):
    path = Path('database/database.json')
    database = json.loads(path.read_text(encoding='utf-8'))
    await message.answer(text=f"TG: {str(database['tg_channels'])}\n\n"
                              f"VK: {str(database['vk_publics'])}\n\n"
                              f"Ключевые слова: {str(database['keywords'])}\n\n"
                              'Для выхода нажмите /cancel',
                         reply_markup=add_public_kb)


# Меню добавления слова из задания
@router.message(F.text == LEXICON['add'], StateFilter(default_state))
async def process_add_button(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['add_hint'])
    await state.set_state(FSMMain.add)


# Меню удаления слова из задания
@router.message(F.text == LEXICON['delete'], StateFilter(default_state))
async def process_delete_button(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['delete_hint'])
    await state.set_state(FSMMain.delete)


# Обработка ввода команды на добавление
@router.message(IsAddDelete(), StateFilter(FSMMain.add))
async def process_add_command(message: Message, state: FSMContext):
    key = message.text[:2]
    task = message.text[3:]
    path = Path('database/database.json')
    database = json.loads(path.read_text(encoding='utf-8'))
    if key == 'TG':
        if task not in database['tg_channels']:
            database['tg_channels'].append(task)
            path.write_text(json.dumps(database), encoding='utf-8')
            await message.answer(text=LEXICON['complete'],
                                 reply_markup=add_public_kb)
            await state.clear()
        else:
            await message.answer(text=LEXICON['yet_exist'])
    elif key == 'VK':
        if task not in database['vk_publics']:
            database['vk_publics'].append(task)
            path.write_text(json.dumps(database), encoding='utf-8')
            await message.answer(text=LEXICON['complete'],
                                 reply_markup=add_public_kb)
            await state.clear()
        else:
            await message.answer(text=LEXICON['yet_exist'])
    else:
        if task not in database['keywords']:
            database['keywords'].append(task)
            path.write_text(json.dumps(database), encoding='utf-8')
            await message.answer(text=LEXICON['complete'],
                                 reply_markup=add_public_kb)
            await state.clear()
        else:
            await message.answer(text=LEXICON['yet_exist'])


# Обработка ввода команды на удаление
@router.message(IsAddDelete(), StateFilter(FSMMain.delete))
async def process_delete_command(message: Message, state: FSMContext):
    key = message.text[:2]
    task = message.text[3:]
    path = Path('database/database.json')
    database = json.loads(path.read_text(encoding='utf-8'))
    if key == 'TG':
        if task in database['tg_channels']:
            database['tg_channels'].remove(task)
            path.write_text(json.dumps(database), encoding='utf-8')
            await message.answer(text=LEXICON['complete'],
                                 reply_markup=add_public_kb)
            await state.clear()
        else:
            await message.answer(text=LEXICON['no_task'])
    elif key == 'VK':
        if task in database['vk_publics']:
            database['vk_publics'].remove(task)
            path.write_text(json.dumps(database), encoding='utf-8')
            await message.answer(text=LEXICON['complete'],
                                 reply_markup=add_public_kb)
            await state.clear()
        else:
            await message.answer(text=LEXICON['no_task'])
    else:
        if task in database['keywords']:
            database['keywords'].remove(task)
            path.write_text(json.dumps(database), encoding='utf-8')
            await message.answer(text=LEXICON['complete'],
                                 reply_markup=add_public_kb)
            await state.clear()
        else:
            await message.answer(text=LEXICON['no_task'])


# Обработка неверного ввода добавления
@router.message(StateFilter(FSMMain.add))
async def warning_add_command(message: Message):
    await message.answer(text=LEXICON['incorrect'])


# Обработка неверного ввода удаления
@router.message(StateFilter(FSMMain.delete))
async def warning_delete_command(message: Message):
    await message.answer(text=LEXICON['incorrect'])





