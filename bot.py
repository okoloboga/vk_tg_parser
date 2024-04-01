import asyncio
import logging
import pandas as pd
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers import other, tasks, deafult


# Инициализация логгера
logger = logging.getLogger(__name__)


async def main():
    # Конфигурирование логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()
    dp = Dispatcher()

    # инициализируем бот в диспетчере
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')


    async def message_sender(bot: Bot):
        tg_frame = pd.read_csv('tg_channels.csv').values.tolist()
        vk_frame = pd.read_csv('vk_publics.csv').values.tolist()
        for line in tg_frame:
            await asyncio.sleep(3)
            await bot.send_message(chat_id='-1002089059378', text=f'Канал: {line[1]}\n'
                                                                  f'Ссылка на пост: https://t.me/{line[2]}/{line[4]}\n'
                                                                  f'Автор поста: {line[5]}\n'
                                                                  f'Дата публикации: {line[-1]}\n\n'
                                                                  f'{line[6]}')
        for line in vk_frame:
            await asyncio.sleep(3)
            await bot.send_message(chat_id='-1002089059378', text=f'Сообщество: {line[2]}\n'
                                                                  f'Ссылка на пост: {line[3]}\n'
                                                                  f'Дата публикации: {line[-1]}\n\n'
                                                                  f'{line[5]}')

    scheduler = AsyncIOScheduler()
    scheduler.add_job(message_sender, 'interval', minutes=367, kwargs={'bot': bot})
    scheduler.start()

    # Настройка главного меню бота
    await set_main_menu(bot)

    # Регистрация роутеров в диспетчере
    dp.include_router(deafult.router)
    dp.include_router(tasks.router)
    dp.include_router(other.router)

    # Пропускаем накопившиеся апдейты и запскаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

