import re, datetime

from aiogram import Router
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.types import Message, BotCommandScopeChat
from aiogram.fsm.context import FSMContext

from create_bot import bot
import keyboards.all_keyboards as kb
from db_handler import db
from fms.moder_fms import ChQuiz

router = Router()

# ----- Отмена действия

@router.message(Command("cancel"),
                StateFilter(ChQuiz.add_q,
                            ChQuiz.add_q_time,
                            ChQuiz.add_answ,
                            ChQuiz.add_answ_correct,
                            ChQuiz.add_answ_color,
                            ChQuiz.del_q,
                            ChQuiz.del_q_confirm,
                            ChQuiz.ch_q,
                            ChQuiz.ch_time))
async def cancel_chosen(msg: Message, state: FSMContext):
    await msg.answer('Вы отменили действие')
    await bot.set_my_commands(kb.commands_change_quiz(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await state.set_state(ChQuiz.ch_action)

# ----- Помощь

@router.message(ChQuiz.ch_action,
                Command("help"))
async def help_chosen(msg: Message):
    await msg.answer('''========= Команды изменения квиза ========
/cancel - выход из изменения квиза
/help - это сообщение
/all_info - вывод информации о квизе
/add_question {text} {time в мм:сс} - добавить вопрос в квиз с временем на ответ time, если аргументов нет - спрашивается по очереди
/del_question {text} - удалить вопрос из квиза с подтверждением, если аргумента нет - дается выбор
/change_question {text} - изменить вопрос, если аргумента нет - дается выбор
/change_start_time {time в "дд.мм.гггг чч:мм:сс"} - изменить время начала квиза, если аргумента нет - прямо спрашивается
''')

# TODO добавить этот функционал
@router.message(ChQuiz.ch_q,
                Command("help"))
async def help_chosen(msg: Message):
    await msg.answer('''========= Команды изменения квиза ========
/cancel - выход из изменения вопроса
/help - это сообщение
/question_info - вывод информации о вопросе
/change_time {time в мм:сс} - изменить время на вопрос, если аргумента нет - прямо спрашивается
/add_answer {text} {is_correct} {color в HEX} - добавить ответ (текст ответа, правильность, цвет в HEX), если аргументов нет - спрашивается по очереди. Если нет правильного ответа, ставьте 0
/del_answer {text} - удалить ответ с подтверждением, если аргумента нет - дается выбор
/change_answer {text} - изменить ответ, если аргумента нет - дается выбор
''')
    
# TODO
@router.message(ChQuiz.ch_answ,
                Command("help"))
async def help_chosen(msg: Message):
    await msg.answer('''========= Команды изменения ответа ========
/cancel - выход из изменения ответа
/help - это сообщение
/answer_info - вывод информации о ответе
/change_correctness - изменить правильность ответа
/change_text - изменить текст ответа
/change_color - изменить цвет ответа
''')

# ----- Вывод всей информации о квизе

@router.message(ChQuiz.ch_action,
                Command("all_info"))
async def show_q(msg: Message, state: FSMContext):
    data = await state.get_data()
    quiz = data['chosen']
    
    time = quiz.start_datetime
    if time:
        formatted_time = time.strftime('%d.%m.%Y в %H:%M')
        if formatted_time.startswith('01.01.2026'):
            await msg.answer('Этот квиз не запланирован на ближайшее время')
        else:
            await msg.answer(f'Квиз запланирован на\n{formatted_time}')
        
    try:
        result = await db.get_questions(quiz)
        if not result:
            await msg.answer('Нет вопросов')
            return

        await msg.answer('Вопросы:')
        for i, el in enumerate(result):
            minutes, seconds = divmod(el.time_limit_seconds, 60)
            await msg.answer(f'''{i + 1}. {el.text}\nВремя на выполнение - {minutes:02d}:{seconds:02d} секунд''')
            answers = await db.get_answers(el)
            if not answers:
                await msg.answer('Нет ответов для этого вопроса')
                continue
            answers_text = "Ответы:\n\n"
            for answer in answers:
                correct = "Правильный ответ" if answer.is_correct else "Неправильный ответ"
                answers_text += f'{answer.text}\n{correct}\nЦвет - {answer.color}\n\n'
            await msg.answer(answers_text)
            
    except Exception as e:
        await msg.answer(f'Ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()

# ----- Добавление вопроса в квиз
@router.message(ChQuiz.ch_action,
                Command("add_question"))
async def add_q(msg: Message, state: FSMContext, command: CommandObject):
    args: str = command.args
    if args:
        args_list = args.split(' ')
        if len(args_list) < 2:
            await msg.answer('Неправильный формат команды. Попробуйте снова\n/add_question {text} {time в мм:сс}')
            return
        question_text = args_list[0]
        question_time = args_list[1]
        time_parts = question_time.split(':')
        if len(time_parts) != 2:
            await msg.answer('Неверный формат времени. Пожалуйста, введите время в формате "мм:сс".')
            return
        try:
            minutes, seconds = map(int, time_parts)
        except:
            await msg.answer('Неверный формат времени. Пожалуйста, введите время в формате "мм:сс".')
            return
        if not(0 <= minutes <= 59 and 0 <= seconds <= 59):
            await msg.answer('Неверное время. Пожалуйста, введите время в формате "мм:сс", где мм не больше 59 и сс не больше 59.')
            return
        
        quiz = (await state.get_data())['chosen']
        question = await db.add_question(question_time, question_text, quiz)
        await msg.answer('Вопрос добавлен.')
        return
    
    await msg.answer('Отмена на /cancel\nВведите вопрос:')
    await state.set_state(ChQuiz.add_q)

# + текст вопроса
@router.message(ChQuiz.add_q)
async def add_q(msg: Message, state: FSMContext):
    await state.update_data(q_name=msg.text)
    await msg.answer('Отмена на /cancel\nСколько времени будет на вопрос (формат "мм:сс"):')
    await state.set_state(ChQuiz.add_q_time)

# + время. добавление вопроса в бд
@router.message(ChQuiz.add_q_time)
async def add_q(msg: Message, state: FSMContext):
    data = await state.get_data()
    time_parts = msg.text.split(':')
    if len(time_parts) != 2:
        await msg.answer('Отмена на /cancel\nНеверный формат времени. Пожалуйста, введите время в формате "мм:сс".')
        return
    try:
        minutes, seconds = map(int, time_parts)
    except:
        await msg.answer('Отмена на /cancel\nНеверный формат времени. Пожалуйста, введите время в формате "мм:сс".')
        return
    if not(0 <= minutes <= 59 and 0 <= seconds <= 59):
        await msg.answer('Отмена на /cancel\nНеверное время. Пожалуйста, введите время в формате "мм:сс", где мм не больше 59 и сс не больше 59.')
        return
    
    try:
        question = await db.add_question(msg.text, data['q_name'], data['chosen'])
        await state.update_data(q_name=question)
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()
    await msg.answer('Вопрос добавлен.')
    await msg.answer('Введите ответ(остановка ввода на /stop):')
    await state.set_state(ChQuiz.add_answ)

# ------ Выход из добавления ответов

@router.message(StateFilter(ChQuiz.add_answ_color,
                            ChQuiz.add_answ,
                            ChQuiz.add_answ_correct),
                Command("stop"))
async def stop(msg: Message, state: FSMContext):
    await msg.answer(f'Вы на экране изменения квиза. Чтобы выйти нажмите /cancel')
    await state.set_state(ChQuiz.ch_action)

# + текст ответа
@router.message(ChQuiz.add_answ)
async def add_answ(msg: Message, state: FSMContext):
    await state.update_data(answ=msg.text)
    await msg.answer('Введите, правилен ли ответ (для опросов без правильного ответа оставьте нет):')
    await state.set_state(ChQuiz.add_answ_correct)

# + корректность ответа
@router.message(ChQuiz.add_answ_correct)
async def add_answ(msg: Message, state: FSMContext):
    if msg.text.lower() in ['да', 'yes', '1']:
        await state.update_data(is_answ_corr=True)
    elif msg.text.lower() in ['нет', 'no', '0']:
        await state.update_data(is_answ_corr=False)
    else:
        await msg.answer('Пожалуйста, введите "да" или "нет"')
        return
    await msg.answer('Введите цвет ответа (в HEX):')
    await state.set_state(ChQuiz.add_answ_color)

# + цвет. добавление ответа в бд
@router.message(ChQuiz.add_answ_color)
async def add_answ(msg: Message, state: FSMContext):
    color = msg.text
    data = await state.get_data()
    hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    if not hex_pattern.match(color):
        await msg.answer('Неправильный формат цвета. Пожалуйста, введите цвет в формате HEX (например, #FFFFFF или #FFF).')
        return
    
    try:
        await db.add_answ(color, data['answ'], data['is_answ_corr'], data['q_name'])
        await msg.answer('Ответ добавлен')
        await msg.answer('Введите следующий ответ(остановка ввода на /stop):')
        await state.set_state(ChQuiz.add_answ)
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()

# ------ Удаление вопроса

@router.message(ChQuiz.ch_action,
                Command("del_question"))
async def del_q(msg: Message, state: FSMContext):
    data = await state.get_data()
    try:
        questions = await db.get_question(data['chosen'])
        await msg.answer('Выберете номер вопроса, который хотите удалить:\n(Либо отмените действие на /cancel)')
        for i, question in enumerate(questions):
            await msg.answer(f'{i + 1}. {question}')
        await state.set_state(ChQuiz.del_q)
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()

@router.message(ChQuiz.del_q)
async def del_q(msg: Message, state: FSMContext):
    data = await state.get_data()
    try:
        index = int(msg.text) - 1
        questions = await db.get_question(data['chosen'])
        if not(0 <= index < len(questions)):
            await msg.answer('Некорректный индекс. Пожалуйста, введите номер вопроса снова.\nЛибо отмените действие на /cancel')
            return
        chosen_questions = questions[index]
        await state.update_data(del_q=chosen_questions)
        await msg.answer(f'Вы выбрали вопрос "{chosen_questions.text}"')
        await msg.answer('Этот вопрос вы хотите удалить? Введите "да" или "нет"')
        await state.set_state(ChQuiz.del_q_confirm)
    except ValueError:
        await msg.answer('Некорректный ввод. Пожалуйста, введите номер вопроса.\nЛибо отмените действие на /cancel')
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()

@router.message(ChQuiz.del_q_confirm)
async def del_q(msg: Message, state: FSMContext):
    if(msg.text.lower() == 'да'):
        data = await state.get_data()
        try:
            await db.del_question(data["del_q"])
            await msg.answer(f'Вопрос {data["del_q"].text} удален')
            await state.set_state(ChQuiz.ch_action)
        except Exception as e:
            await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
            await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
            await state.clear()
    elif(msg.text.lower() == 'нет'):
        await msg.answer('Напишите название вопроса, который хотите удалить:')
        await state.set_state(ChQuiz.del_q)
    else:
        await msg.answer('Я не понимаю. Напишите "да" или "нет"\nЛибо отмените действие на /cancel')


# TODO Изменение вопросов
@router.message(ChQuiz.ch_action,
                Command("change_question"))
async def ch_quiz(msg: Message, state: FSMContext):
    pass


# ------ Добавление времени квиза
@router.message(ChQuiz.ch_action,
                Command("change_start_time"))
async def ch_quiz(msg: Message, state: FSMContext):
    args: str = command.args
    if args:
        args_list = args.split(' ')
        time = args_list[0]
        try:
            datetime.datetime.strptime(time, "%d.%m.%Y %H:%M:%S")
        except ValueError:
            await msg.answer('Неправильный формат даты и времени. Пожалуйста, введите дату и время в формате "дд.мм.гггг чч:мм:сс"')
            return
        
        quiz = (await state.get_data())['chosen']
        try:
            await db.set_quiz_time(time, quiz)
            await msg.answer(f'Время начала квиза {quiz.name} установлено на {time}')
        except Exception as e:
            await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
            await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
            await state.clear()
        return
    
    await msg.answer('Введите дату и время начала квиза (формат "дд.мм.гггг чч:мм:сс")')
    await msg.answer('Пример: 16.10.2024 16:30:00')
    await state.set_state(ChQuiz.ch_time)

@router.message(ChQuiz.ch_time)
async def ch_quiz(msg: Message, state: FSMContext):
    data = await state.get_data()
    try:
        datetime.datetime.strptime(msg.text, "%d.%m.%Y %H:%M:%S")
    except ValueError:
        await msg.answer('Неправильный формат даты и времени. Пожалуйста, введите дату и время в формате "дд.мм.гггг чч:мм:сс"\nЛибо выйдете на /cancel')
        return
    try:
        await db.set_quiz_time(msg.text, data["chosen"])
        await msg.answer(f'Время начала квиза {data["chosen"].name} установлено на {msg.text}')
        await state.set_state(ChQuiz.ch_action)
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()