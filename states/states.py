from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Создаем класса, наследуемый от StatesGroup для группы состояний в FSM
class FSMMain(StatesGroup):

    add = State()
    delete = State()
    create = State()