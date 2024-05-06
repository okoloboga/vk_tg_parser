import schedule
import logging

from environs import Env
from services.main_funcs import main_parsing

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return [env('API_ID'), env('API_HASH'), env('PHONE')]


schedule.every(1).hour.do(lambda: main_parsing(*load_config()))

while True:
    try:
        schedule.run_pending()
    except TypeError as e:
        logger.error('TypeError: ', e)