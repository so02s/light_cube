from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, BotCommandScopeChat

import re

from utils.filter import admins, moders
import keyboards.all_keyboards as kb
from aiogram.fsm.context import FSMContext
from fms.moder_fms import AddQuiz, DelQuiz, ChQuiz, StQuiz
from db_handler import db
from handlers.quiz_handler import start_quiz
from create_bot import bot

router = Router()

# -------- Вывод всех квизов

@router.message(lambda msg: msg.from_user.username in admins() + moders(), StateFilter(None), Command("all_quiz"))
async def cmd_start(msg: Message):
    try:
        result = await db.get_quizs()
        if(result != []):
            await msg.answer('Квизы:')
            for i, el in enumerate(result):
                await msg.answer(f'{i + 1}. {el}')
        else:
            await msg.answer('Нет квизов')
    except Exception as e:
        await msg.answer(f'Ошибка: {e}')


# -------- Добавление квиза

@router.message(lambda msg: msg.from_user.username in admins() + moders(), StateFilter(None), Command("add_quiz"))
async def cmd_start(msg: Message, state: FSMContext):
    await msg.answer('Отмена на /cancel')
    await msg.answer('Введите название квиза:')
    await state.set_state(AddQuiz.ch_name)

# TODO проверка на название
# TODO добавить настройки
@router.message(AddQuiz.ch_name)
async def moder_chosen(msg: Message, state: FSMContext):
    try:
        await db.add_quiz(msg.text)
        await msg.answer(f'Добавлен квиз {msg.text}')
        await state.clear()
    except Exception as e:
        await msg.answer(f'Ошибка: {e}')


# -------- Удаление квиза

@router.message(lambda msg: msg.from_user.username in admins() + moders(), StateFilter(None), Command("del_quiz"))
async def cmd_start(msg: Message, state: FSMContext):
    try:
        quizs = await db.get_quizs()
        if(quizs != []):
            await msg.answer('Отмена на /cancel')
            await msg.answer('Выберете квиз, который хотите удалить (номер):')
            for i, quiz in enumerate(quizs):
                await msg.answer(f'{i + 1}. {quiz}')
            await state.set_state(DelQuiz.ch_name)
        else:
            await msg.answer('Нет квизов')
            await state.clear()
    except Exception as e:
        await msg.answer(f'Ошибка: {e}')

@router.message(DelQuiz.ch_name)
async def delquiz_chosen(msg: Message, state: FSMContext):
    try:
        quizs = await db.get_quizs()
        index = int(msg.text) - 1
        if 0 <= index < len(quizs):
            chosen_quiz = quizs[index]
            await state.update_data(chosen=chosen_quiz)
            await msg.answer(f'Вы выбрали квиз {chosen_quiz}')
            await msg.answer('Этот квиз вы хотите удалить? Введите "да" или "нет"')
            await state.set_state(DelQuiz.confirm)
        else:
            await msg.answer('Некорректный индекс. Пожалуйста, введите номер квиза снова.')
    except ValueError:
        await msg.answer('Некорректный ввод. Пожалуйста, введите номер квиза.')
    except Exception as e:
        await msg.answer(f'Ошибка: {e}')

@router.message(DelQuiz.confirm)
async def confirm_delquiz(msg: Message, state: FSMContext):
    if(msg.text.lower() == 'да'):
        name = await state.get_data()
        try:
            await db.del_quiz(name["chosen"])
            await msg.answer(f'Квиз {name["chosen"]} удален')
        except Exception as e:
            await msg.answer(f'Произошла ошибка: {e}, попробуйте снова с самого начала')
        finally:
            await state.clear()
    elif(msg.text.lower() == 'нет'):
        await msg.answer('Напишите номер квиза, который хотите удалить:')
        await state.set_state(DelQuiz.ch_name)
    else:
        await msg.answer('Я не понимаю. Напишите "да" или "нет"')


# -------- Настройка квиза

@router.message(lambda msg: msg.from_user.username in admins() + moders(), StateFilter(None), Command("change_quiz"))
async def ch_quiz(msg: Message, state: FSMContext):
    quizs = await db.get_quizs()
    if(quizs != []):
        await msg.answer('Отмена на /cancel')
        await msg.answer('Выберете квиз, который хотите изменить (номер):')
        for i, quiz in enumerate(quizs):
            await msg.answer(f'{i + 1}. {quiz}')
        await state.set_state(ChQuiz.ch_name)
    else:
        await msg.answer('Нет квизов')
        await state.clear()


@router.message(ChQuiz.ch_name)
async def ch_quiz(msg: Message, state: FSMContext):
    try:
        index = int(msg.text) - 1
        quizs = await db.get_quizs()
        if 0 <= index < len(quizs):
            chosen_quiz = quizs[index]
            await state.update_data(chosen=chosen_quiz)
            await msg.answer(f'Вы выбрали квиз "{chosen_quiz}"')
            await msg.answer('Выйти из меню изменения квиза на /cancel')
            await bot.set_my_commands(kb.commands_change_quiz(), BotCommandScopeChat(chat_id=msg.from_user.id))
            await state.set_state(ChQuiz.ch_action)
        else:
            await msg.answer('Некорректный индекс. Пожалуйста, введите номер квиза снова.')
    except ValueError:
        await msg.answer('Некорректный ввод. Пожалуйста, введите номер квиза.')
    except Exception as e:
        await msg.answer(f'Ошибка: {e}')


# TODO добавить все state отсюда в cancel для ch_quiz
@router.message(lambda msg: msg.from_user.username in moders(), StateFilter(ChQuiz.ch_action), Command("cancel"))
async def cancel_chosen(msg: Message, state: FSMContext):
    await msg.answer('Вы отменили действие. Вернуться в главное меню можно на /cancel')
    await bot.set_my_commands(kb.commands_change_quiz(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await state.set_state(ChQuiz.ch_name)

# ----- Вывод всей информации о квизе
@router.message(ChQuiz.ch_action, Command("all_info"))
async def show_q(msg: Message, state: FSMContext):
    data = await state.get_data()
    try:
        time = await db.get_quiz_time(data['chosen'])
        if time:
            await msg.answer(f'Квиз запланирован на {time}')
        result = await db.get_questions(data['chosen'])
        if result == None:
            await msg.answer('Нет вопросов')
            return
        
        await msg.answer('Вопросы:')
        for i, el in enumerate(result):
            await msg.answer(f'{i + 1}. {el}')
            # TODO еще сколько времени дается на вопрос
            answers = await db.get_answers(el)
            if answers == None:
                await msg.answer('Нет ответов для этого вопроса')
                continue
            await msg.answer('Ответы:')
            for j, answer in enumerate(answers):
                await msg.answer(f'     {j + 1}. {answer}')
                # TODO еще цвет ответа

    except Exception as e:
        await msg.answer(f'Ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()

# ----- Добавление вопроса в квиз
@router.message(ChQuiz.ch_action, Command("add_question"))
async def add_q(msg: Message, state: FSMContext):
    await msg.answer('Отмена на /cancel')
    await msg.answer('Введите вопрос:')
    await state.set_state(ChQuiz.add_q)

# + текст вопроса
@router.message(ChQuiz.add_q)
async def add_q(msg: Message, state: FSMContext):
    await state.update_data(q_name=msg.text)
    await msg.answer('Сколько времени будет на вопрос (формат "мм:сс"):')
    await state.set_state(ChQuiz.add_q_time)

# + время. добавление вопроса в бд
@router.message(ChQuiz.add_q_time)
async def add_q(msg: Message, state: FSMContext):
    data = await state.get_data()
    time_format = re.match(r'^\d{1,2}:\d{2}$', msg.text)
    if not time_format:
        await msg.answer('Неверный формат времени. Пожалуйста, введите время в формате "мм:сс".')
        return
    
    minutes, seconds = map(int, time_format.groups())
    if not(0 <= minutes <= 59 and 0 <= seconds <= 59):
        await msg.answer('Неверное время. Пожалуйста, введите время в формате "мм:сс", где мм не больше 59 и сс не больше 59.')
        return
    
    try:
        await db.add_question(msg.text, data['q_name'], data['chosen'])
        await msg.answer('Вопрос добавлен.')
        await msg.answer('Введите ответ(остановка ввода на /stop):')
        await state.set_state(ChQuiz.add_answ)
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()


# TODO state не может быть multiple()
# стоп добавления ответов на вопрос
# @router.message(lambda state: state in [ChQuiz.add_answ_color, ChQuiz.add_answ], Command("stop"))
# async def stop(msg: Message, state: FSMContext):
#     await msg.answer(f'Вы на экране изменения квиза. Чтобы выйти нажмите /cancel')
#     await state.set_state(ChQuiz.ch_action)

# + текст ответа
@router.message(ChQuiz.add_answ)
async def add_answ(msg: Message, state: FSMContext):
    await state.update_data(answ=msg.text)
    await msg.answer('Введите цвет ответа (в HEX):')
    await state.set_state(ChQuiz.add_answ_color)

# + цвет. добавление ответа в бд
@router.message(ChQuiz.add_answ_color)
async def add_answ(msg: Message, state: FSMContext):
    data = await state.get_data()
    hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    if not hex_pattern.match(msg.text):
        await msg.answer('Неправильный формат цвета. Пожалуйста, введите цвет в формате HEX (например, #FFFFFF или #FFF).')
        return
    
    try:
        await db.add_answ(msg.text, data['answ'], data['q_name'], data['chosen'])
        await msg.answer('Ответ добавлен')
        await msg.answer('Введите следующий ответ(остановка ввода на /stop):')
        await state.set_state(ChQuiz.add_answ)
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()

# ------ Удаление вопроса
@router.message(ChQuiz.ch_action, Command("del_question"))
async def del_q(msg: Message, state: FSMContext):
    data = await state.get_data()
    try:
        questions = await db.get_question(data['chosen'])
        await msg.answer('Выберете номер вопроса, который хотите удалить:')
        for i, question in enumerate(questions):
            await msg.answer(f'{i + 1}. {question}')
        await state.set_state(ChQuiz.del_q)
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()

@router.message(ChQuiz.del_q)
async def del_q(msg: Message, state: FSMContext):
    try:
        index = int(msg.text) - 1
        questions = await db.get_question(data['chosen'])
        if not(0 <= index < len(questions)):
            await msg.answer('Некорректный индекс. Пожалуйста, введите номер вопроса снова.')
            return
        chosen_questions = questions[index]
        await state.update_data(del_q=chosen_questions)
        await msg.answer(f'Вы выбрали вопрос "{chosen_questions}"')
        await msg.answer('Этот вопрос вы хотите удалить? Введите "да" или "нет"')
        await state.set_state(ChQuiz.del_q_confirm)
    except ValueError:
        await msg.answer('Некорректный ввод. Пожалуйста, введите номер вопроса.')
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()

@router.message(ChQuiz.del_q_confirm)
async def del_q(msg: Message, state: FSMContext):
    if(msg.text.lower() == 'да'):
        data = await state.get_data()
        try:
            await db.del_question(data["del_q"], data["chosen"])
            await msg.answer(f'Вопрос {data["del_q"]} удален')
            await state.set_state(ChQuiz.ch_action)
        except Exception as e:
            await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
            await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
            await state.clear()
    elif(msg.text.lower() == 'нет'):
        await msg.answer('Напишите название вопроса, который хотите удалить:')
        await state.set_state(ChQuiz.del_q)
    else:
        await msg.answer('Я не понимаю. Напишите "да" или "нет"')


# TODO Изменение вопросов
@router.message(ChQuiz.ch_action, Command("change_question"))
async def ch_quiz(msg: Message, state: FSMContext):
    pass


# ------ Добавление времени квиза
@router.message(ChQuiz.ch_action, Command("change_start_time"))
async def ch_quiz(msg: Message, state: FSMContext):
    await msg.answer('Введите дату и время начала квиза (формат "дд.мм.гггг чч:мм:сс")')
    await msg.answer('Пример: 16.10.2024 16:30:00')
    await state.set_state(ChQuiz.ch_time)

@router.message(ChQuiz.ch_time)
async def ch_quiz(msg: Message, state: FSMContext):
    data = await state.get_data()
    try:
        datetime.datetime.strptime(msg.text, "%d.%m.%Y %H:%M:%S")
    except ValueError:
        await msg.answer('Неправильный формат даты и времени. Пожалуйста, введите дату и время в формате "дд.мм.гггг чч:мм:сс"')
        return
    try:
        await db.set_quiz_time(msg.text, data["chosen"])
        await msg.answer(f'Время начала квиза {data["chosen"]} установлено на {msg.text}')
        await state.set_state(ChQuiz.ch_action)
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()


# -------- Принудительный запуск квиза
@router.message(lambda msg: msg.from_user.username in admins() + moders(), Command("start_quiz"))
async def st_quiz(msg: Message, state: FSMContext):
    try:
        quizs = await db.get_quizs()
        if quizs:
            await msg.answer('Выберете квиз:')
            for i, quiz in enumerate(quizs):
                await msg.answer(f'{i + 1}. {quiz}')
            await state.set_state(StQuiz.ch_name)
        else:
            await msg.answer('Нет квизов')
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()

@router.message(StQuiz.ch_name)
async def st_quiz(msg: Message, state: FSMContext):
    try:
        index = int(msg.text) - 1
        quizs = await db.get_quizs()
        if not(0 <= index < len(quizs)):
            await msg.answer('Некорректный индекс. Пожалуйста, введите номер вопроса снова.')
            return
        chosen_quiz = quizs[index]
        await start_quiz(chosen_quiz)
        await msg.answer('Квиз начат')
        await state.clear()
    except ValueError:
        await msg.answer('Некорректный ввод. Пожалуйста, введите номер вопроса.')
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()


# -------- Режим юзера 

@router.message(lambda msg: msg.from_user.username in moders(), Command("user"))
async def cmd_start(msg: Message):
    await bot.set_my_commands(kb.commands_user(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await msg.answer('Включен режим юзера. Для возвращения напишите /cancel или /start')
    await state.clear()


# ------ Отмена действий

@router.message(lambda msg: msg.from_user.username in moders(), Command("cancel"))
async def cancel_chosen(msg: Message, state: FSMContext):
    await msg.answer('Вы отменили действие')
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await state.clear()