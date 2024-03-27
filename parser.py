import schedule
from services.main_funcs import main_parsing

main_parsing()
schedule.every(1).day.at("00:00", "Europe/Moscow").do(lambda: main_parsing())

while True:
    try:
        schedule.run_pending()
    except TypeError:
        pass