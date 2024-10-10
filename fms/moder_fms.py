from aiogram.fsm.state import State, StatesGroup

class AddQuiz(StatesGroup):
    ch_name = State()

class DelQuiz(StatesGroup):
    ch_name = State()
    confirm = State()

class ChQuiz(StatesGroup):
    ch_name = State()
    ch_action = State()
    add_q = State()
    add_q_time = State()
    add_answ = State()
    add_answ_color = State()
    del_q = State()
    del_q_confirm = State()
    ch_q = State()
    ch_time = State()

class StQuiz(StatesGroup):
    ch_name = State()