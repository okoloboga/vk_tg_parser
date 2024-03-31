import schedule
import time

from environs import Env
from services.main_funcs import main_parsing


def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return env('PHONE')


main_parsing(load_config())
schedule.every(6).hours.do(lambda: main_parsing(load_config()))

while True:
    try:
        schedule.run_pending()
    except TypeError:
        pass