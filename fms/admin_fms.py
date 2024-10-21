from aiogram.fsm.state import State, StatesGroup
    
class DelModer(StatesGroup):
    ch_name = State()
    confirm = State()