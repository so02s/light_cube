from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, BotCommandScopeChat

from utils.filter import admins, moders
import keyboards.all_keyboards as kb
from aiogram.fsm.context import FSMContext
from fms.moder_fms import AddQuiz, DelQuiz, ChQuiz, StQuiz
from db_hanler import db
from handlers.quiz_handler import start_quiz
from create_bot import bot

router = Router()


@router.message(F.from_user.id.in_(moders), StateFilter(ChQuiz.ch_action), Command("cancel"))
async def cancel_chosen(message: Message, state: FSMContext):
    await message.answer('Вы отменили действие. Вернуться в главное меню можно на /cancel')
    await bot.set_my_commands(kb.commands_change_quiz(), BotCommandScopeChat(chat_id=message.from_user.id))
    await state.set_state(ChQuiz.ch_name)

@router.message(F.from_user.id.in_(moders), Command("cancel"))
async def cancel_chosen(message: Message, state: FSMContext):
    await message.answer('Вы отменили действие')
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=message.from_user.id))
    await state.clear()

# -------- Добавление квиза

@router.message(F.from_user.id.in_(admins) | F.from_user.id.in_(moders), StateFilter(None), Command("add_quiz"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Отмена на /cancel')
    await message.answer('Введите название квиза:')
    await state.set_state(AddQuiz.ch_name)

@router.message(AddQuiz.ch_name)
async def moder_chosen(message: Message, state: FSMContext):
    # TODO проверка на название
    # TODO добавить настройки
    await db.add_quiz(message.text)
    await message.answer(f'Добавлен квиз {message.text}')
    await state.clear()

# -------- Удаление квиза

@router.message(F.from_user.id.in_(admins) | F.from_user.id.in_(moders), StateFilter(None), Command("del_quiz"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Отмена на /cancel')
    quizs = await db.get_quizs()
    await message.answer('Выберете квиз, который хотите удалить:')
    for i, quiz in enumerate(quizs):
        await message.answer(f'{i + 1}. {quiz}')
    await state.set_state(DelQuiz.ch_name)

@router.message(DelQuiz.ch_name)
async def delmoder_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen=message.text)
    await message.answer(message.text)
    await message.answer('Этот квиз вы хотите удалить? Введите "да" или "нет"')
    await state.set_state(DelQuiz.confirm)

@router.message(DelQuiz.confirm)
async def confirm_delmoder(message: Message, state: FSMContext):
    if(message.text.lower() == 'да'):
        name = await state.get_data()
        await db.del_quiz(name["chosen"])
        await message.answer(f'Квиз {name["chosen"]} удален')
        await state.clear()
    elif(message.text.lower() == 'нет'):
        await message.answer('Напишите название квиза, которого хотите удалить:')
        await state.set_state(DelQuiz.ch_name)
    else:
        await message.answer('Я не понимаю')

# -------- Настройка квиза

@router.message(F.from_user.id.in_(admins) | F.from_user.id.in_(moders), StateFilter(None), Command("change_quiz"))
async def ch_quiz(message: Message, state: FSMContext):
    await message.answer('Отмена на /cancel')
    quizs = await db.get_quizs()
    await message.answer('Выберете квиз, который хотите изменить:')
    for i, quiz in enumerate(quizs):
        await message.answer(f'{i + 1}. {quiz}')
    await state.set_state(ChQuiz.ch_name)

# TODO хэндлер для несуществующих квизов
# TODO добавить все state отсюда в cancel для ch_quiz

@router.message(ChQuiz.ch_name)
async def ch_quiz(message: Message, state: FSMContext):
    await state.update_data(chosen=message.text)
    await message.answer('Отмена на /cancel')
    await bot.set_my_commands(kb.commands_change_quiz(), BotCommandScopeChat(chat_id=message.from_user.id))
    await state.set_state(ChQuiz.ch_action)
    

@router.message(ChQuiz.ch_action, Command("add_question"))
async def add_q(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer('Отмена на /cancel')
    await message.answer('Введите вопрос:')
    await state.set_state(ChQuiz.add_q)

@router.message(ChQuiz.add_q)
async def add_q(message: Message, state: FSMContext):
    data = await state.get_data()
    await db.add_question(message.text, data['chosen'])
    await state.update_data(q_name=message.text) # нужно чтобы найти индекс вопроса в бд
    await message.answer('Сколько времени будет на вопрос (формат "мм:сс"):')
    await state.set_state(ChQuiz.add_q_time)

@router.message(ChQuiz.add_q_time)
async def add_q(message: Message, state: FSMContext):
    data = await state.get_data()
    await db.add_question_time(message.text, data['q_name'], data['chosen']) # нужно выбор из строки сделать
    await message.answer('Введите ответ(остановка ввода на /stop):')
    await state.set_state(ChQuiz.add_answ)

@router.message(ChQuiz.add_answ)
async def add_answ(message: Message, state: FSMContext):
    if(message.text == '/stop'):
        await state.set_state(ChQuiz.ch_action)
    else:
        data = await state.get_data()
        await db.add_answ(message.text, data['q_name'])
        await state.update_data(answ=message.text)
        await message.answer('Ответ добавлен')
        await message.answer('Введите цвет ответа (в HEX, только код):')
        await state.set_state(ChQuiz.add_answ_color)

@router.message(ChQuiz.add_answ_color)
async def add_answ(message: Message, state: FSMContext):
    if(message.text == '/stop'):
        await state.set_state(ChQuiz.ch_action)
    else:
        data = await state.get_data()
        await db.add_answ_col(message.text, data['answ'], data['q_name'])
        await message.answer('Цвет добавлен')
        await message.answer('Введите ответ(остановка ввода на /stop):')
        await state.set_state(ChQuiz.add_answ)


@router.message(ChQuiz.ch_action, Command("del_question"))
async def del_q(message: Message, state: FSMContext):
    data = await state.get_data()
    questions = await db.get_question(data['chosen'])
    await message.answer('Выберете вопрос, который хотите удалить:')
    for i, question in enumerate(questions):
        await message.answer(f'{i + 1}. {question}')
    await state.set_state(ChQuiz.del_q)

# TODO проверка на существование вопроса
# TODO выбор из списка по индексу

@router.message(ChQuiz.del_q)
async def del_q(message: Message, state: FSMContext):
    await state.update_data(del_q=message.text) # тут по индексу, переписать
    await message.answer(message.text)
    await message.answer('Этот вопрос вы хотите удалить? Введите "да" или "нет"')
    await state.set_state(ChQuiz.del_q_confirm)

@router.message(ChQuiz.del_q_confirm)
async def del_q(message: Message, state: FSMContext):
    if(message.text.lower() == 'да'):
        data = await state.get_data()
        await db.del_question(data["del_q"], data["chosen"])
        await message.answer(f'Вопрос {data["del_q"]} удален')
        await state.set_state(ChQuiz.ch_action)
    elif(message.text.lower() == 'нет'):
        await message.answer('Напишите название вопроса, который хотите удалить:')
        await state.set_state(ChQuiz.del_q)
    else:
        await message.answer('Я не понимаю')
        

@router.message(ChQuiz.ch_action, Command("change_question"))
async def ch_quiz(message: Message, state: FSMContext):
    pass



@router.message(ChQuiz.ch_action, Command("change_start_time"))
async def ch_quiz(message: Message, state: FSMContext):
    await message.answer('Введите дату и время начала квиза (формат "дд.мм.гггг чч:мм:сс")')
    await message.answer('Пример: 16.10.2024 16:30:00')
    await state.set_state(ChQuiz.ch_time)

@router.message(ChQuiz.ch_time)
async def ch_quiz(message: Message, state: FSMContext):
    data = await state.get_data()
    # TODO проверка на ввод времени
    await db.set_quiz_time(message.text, data["chosen"])
    await message.answer(f'Время начала квиза {data["chosen"]} установлено на {message.text}')
    await state.set_state(ChQuiz.ch_action)

# -------- Принудительный запуск квиза

@router.message(F.from_user.id.in_(admins) | F.from_user.id.in_(moders), Command("start_quiz"))
async def st_quiz(message: Message, state: FSMContext):
    quizs = await db.get_quizs()
    await message.answer('Выберете квиз:')
    for i, quiz in enumerate(quizs):
        await message.answer(f'{i + 1}. {quiz}')
    await state.set_state(StQuiz.ch_name)

@router.message(StQuiz.ch_name)
async def st_quiz(message: Message, state: FSMContext):
    # TODO запуск по индексу
    await start_quiz(message.text)
    await message.answer('Квиз начат')
    await state.clear()


# -------- Режим юзера 

@router.message(F.from_user.id.in_(moders), Command("user"))
async def cmd_start(message: Message):
    await bot.set_my_commands(kb.commands_user(), BotCommandScopeChat(chat_id=message.from_user.id))
    await message.answer('Включен режим юзера. Для возвращения напишите /start')
    await state.clear()