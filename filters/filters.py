from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAddDelete(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        task = message.text[:3]
        return task in ['VK ', 'TG ', 'KW ']

class IsDayTime(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        day_time = message.text
        space = day_time.find(' ')
        day = day_time[:space].lower()
        time = day_time[space+1:]
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

        return (day in days) and (time[:2].isdigit() and time[2]==':' and time[3:].isdigit())