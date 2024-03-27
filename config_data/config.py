"""Инициализация токенов и ID админа, дальнейшая передача их в Бота"""

from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]

@dataclass
class Config:
    tg_bot: TgBot

# Читаем .env и возвращаем заполненный Config
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMINS_IDS')))
        )
    )