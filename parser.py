import schedule

from environs import Env
from services.main_funcs import main_parsing

def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return env('PHONE')

main_parsing(load_config())
schedule.every(1).day.at("00:00", "Europe/Moscow").do(lambda: main_parsing())

while True:
    try:
        schedule.run_pending()
    except TypeError:
        pass