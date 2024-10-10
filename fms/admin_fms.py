from aiogram.fsm.state import State, StatesGroup

class Group(StatesGroup):
    ch_name = State()

class GroupRand(Group):
    ch_conf = State()

class AddModer(StatesGroup):
    ch_name = State()
    
class DelModer(StatesGroup):
    ch_name = State()
    confirm = State()