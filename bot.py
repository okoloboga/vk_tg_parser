import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers import other, tasks, deafult

# Инициализация логгера
logger = logging.getLogger(__name__)

# Конфигурирование и запуск Бота
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

    # Инициализируем бот в диспетчере
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher()

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