from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter

router = Router()

# Обработка любых сообщений не предусмотренных логикой бота
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.answer(f'Я пока не так хорошо разговариваю на Вашем...')