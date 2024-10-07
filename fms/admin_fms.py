from aiogram.fsm.state import State, StatesGroup

class Group(StatesGroup):
    ch_group_name = State()

class GroupRand(Group):
    ch_rand_conf = State()

class AddModer(StatesGroup):
    ch_moder_name = State()