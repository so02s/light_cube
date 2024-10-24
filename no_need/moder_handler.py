import re, datetime

from aiogram import Router, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.types import Message, BotCommandScopeChat, CallbackQuery
from aiogram.fsm.context import FSMContext

from create_bot import bot
from utils.filter import is_admin_or_moder, is_moder
import keyboards.all_keyboards as kb
from db_handler import db
from fms.moder_fms import AddQuiz, DelQuiz, ChQuiz, StQuiz
from handlers.quiz_handler import start_quiz, QuizMiddleware
from handlers.scheduler_handler import schedule_add_job, schedule_del_job




router = Router()
router.message.middleware(QuizMiddleware())


# ------ Помощь

@router.message(is_moder,
                StateFilter(None), 
                Command("help"))
async def help_moder(msg: Message):
    await msg.answer('''
/start - стартовое сообщение
/help - помощь, выводит это сообщение
/change_program - изменить сообщение о программе мероприятия. Еще не работает
/all_quiz - вывести все квизы
/start_quiz - начать квиз
/add_quiz - добавить квиз
/del_quiz - удаляет квиз
/change_quiz - изменить квиз
/cancel - отмена действия
''')

# ------ Отмена действий

@router.message(Command("cancel"),
                StateFilter(StQuiz.ch_name,
                            AddQuiz.ch_name,
                            DelQuiz.ch_name,
                            DelQuiz.confirm,
                            ChQuiz.ch_name,
                            ChQuiz.ch_action))
async def cancel_chosen(msg: Message, state: FSMContext):
    await msg.answer('Вы отменили действие')
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await state.clear()

# -------- Режим юзера
# TODO - добавление в список с юзерами кубов
@router.message(is_moder, Command("user"))
async def cmd_start(msg: Message, state: FSMContext):
    await bot.set_my_commands(kb.commands_user(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await msg.answer('Включен режим юзера. Для возвращения напишите /start')
    await state.clear()

# -------- Изменить сообщение о программе мероприятия
# TODO еще добавление файла/картинки/каким-то образом копирование сообщения от пользователя и его сохранение
@router.message(is_admin_or_moder, StateFilter(None), Command("change_program"))
async def cmd_start(msg: Message):
    await msg.answer('Функция еще не добавлена')


# -------- Вывод всех квизов

@router.message(is_admin_or_moder, StateFilter(None), Command("all_quiz"))
async def cmd_start(msg: Message):
    try:
        result = await db.get_quizs()
        if not result:
            await msg.answer('Нет квизов')
            return

        await msg.answer('Квизы:')
        for i, el in enumerate(result):
            await msg.answer(f'{i + 1}. {el.name}')

    except Exception as e:
        await msg.answer(f'Ошибка: {e}')

# -------- Принудительный запуск квиза

@router.message(is_admin_or_moder, Command("start_quiz"))
async def st_quiz(msg: Message, state: FSMContext, command: CommandObject):
    args: str = command.args
    if args:
        quiz_name = args.split(' ')[0]
        quiz = await db.get_quiz(quiz_name)
        if not quiz:
            await msg.answer(f'Квиза {quiz_name} не существует, попробуйте использовать команду /start_quiz без аргументов')
            return
        await start_quiz(quiz)
        await msg.answer(f'Квиз {quiz_name} начат')
        return
    
    try:
        quizs = await db.get_quizs()
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        return

    if not quizs:
        await msg.answer('Нет квизов')
        return
    
    await msg.answer('Выберете квиз:')
    for i, quiz in enumerate(quizs):
        await msg.answer(f'{i + 1}. {quiz.name}')
    await state.set_state(StQuiz.ch_name)

@router.message(StQuiz.ch_name)
async def st_quiz(msg: Message, state: FSMContext):
    try:
        index = int(msg.text) - 1
        quizs = await db.get_quizs()
    except ValueError:
        await msg.answer('Некорректный ввод. Пожалуйста, введите номер квиза снова, либо выйдите на /cancel')
        return
    except Exception as e:
        await msg.answer(f'Произошла ошибка: {e}, вы возвращены на экран модератора')
        await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.clear()
        return
    
    if not(0 <= index < len(quizs)):
        await msg.answer('Некорректный индекс. Пожалуйста, введите номер квиза снова, либо выйдите на /cancel')
        return
    
    chosen_quiz = quizs[index]
    await msg.answer('Квиз начат')
    await state.clear()
    await start_quiz(chosen_quiz)

# -------- Добавление квиза
@router.message(is_admin_or_moder, StateFilter(None), Command("add_quiz"))
async def cmd_start(msg: Message, state: FSMContext, command: CommandObject):
    args: str = command.args
    if args:
        quiz_name = args.split(' ')[0]
        await db.add_quiz(quiz_name)
        await msg.answer(f'Добавлен квиз {quiz_name}')
        return
    
    await msg.answer('Отмена на /cancel')
    await msg.answer('Введите название квиза:')
    await state.set_state(AddQuiz.ch_name)

@router.message(AddQuiz.ch_name)
async def moder_chosen(msg: Message, state: FSMContext):
    try:
        await db.add_quiz(msg.text)
        await msg.answer(f'Добавлен квиз {msg.text}')
        await state.clear()
    except Exception as e:
        await msg.answer(f'Ошибка: {e}')

# -------- Удаление квиза

@router.message(is_admin_or_moder,
                StateFilter(None),
                Command("del_quiz"))
async def cmd_start(msg: Message, state: FSMContext, command: CommandObject):
    try:
        quizs = await db.get_quizs()
        if not quizs:
            await msg.answer('Нет квизов')
            return
    except Exception as e:
        await msg.answer(f'Ошибка: {e}')
    
    args: str = command.args
    if args:
        quiz_name = args.split(' ')[0]
        quiz = await db.get_quiz(quiz_name)
        if not quiz:
            await msg.answer(f'Такого квиза не существует. Попробуйте еще раз через /del_quiz без аргументов')
            return
        await state.update_data(chosen=quiz)
        await msg.answer(f'Вы выбрали квиз {quiz.name}')
        await msg.answer('Этот квиз вы хотите удалить? Введите "да" или "нет"')
        await state.set_state(DelQuiz.confirm)
        return

    await msg.answer('Отмена на /cancel')
    await msg.answer('Выберете квиз, который хотите удалить (номер):')
    for i, quiz in enumerate(quizs):
        await msg.answer(f'{i + 1}. {quiz.name}')
    await state.set_state(DelQuiz.ch_name)

@router.message(DelQuiz.ch_name)
async def delquiz_chosen(msg: Message, state: FSMContext):
    try:
        quizs = await db.get_quizs()
        index = int(msg.text) - 1
        if 0 <= index < len(quizs):
            chosen_quiz = quizs[index]
            await state.update_data(chosen=chosen_quiz)
            await msg.answer(f'Вы выбрали квиз {chosen_quiz.name}')
            await msg.answer('Этот квиз вы хотите удалить? Введите "да" или "нет"')
            await state.set_state(DelQuiz.confirm)
        else:
            await msg.answer('Некорректный индекс. Пожалуйста, введите номер квиза снова.\nВы можете отменить действие на /cancel')
    except ValueError:
        await msg.answer('Некорректный ввод. Пожалуйста, введите номер квиза.\nВы можете отменить действие на /cancel')
    except Exception as e:
        await msg.answer(f'Ошибка: {e}')

@router.message(DelQuiz.confirm)
async def confirm_delquiz(msg: Message, state: FSMContext):
    if(msg.text.lower() == 'да'):
        quiz = (await state.get_data())["chosen"]
        try:
            await db.del_quiz(quiz)
            await schedule_del_job(quiz.id)
            await msg.answer(f'Квиз {quiz.name} удален')
        except Exception as e:
            await msg.answer(f'Произошла ошибка: {e}, попробуйте снова с самого начала')
        finally:
            await state.clear()
    elif(msg.text.lower() == 'нет'):
        await msg.answer('Напишите номер квиза, который хотите удалить.\nВы можете отменить действие на /cancel')
        await state.set_state(DelQuiz.ch_name)
    else:
        await msg.answer('Я не понимаю. Напишите "да" или "нет"\nВы можете отменить действие на /cancel')


# -------- Настройка квиза

@router.message(is_admin_or_moder,
                StateFilter(None),
                Command("change_quiz"))
async def ch_quiz(msg: Message, state: FSMContext, command: CommandObject):
    try:
        quizs = await db.get_quizs()
        if not quizs:
            await msg.answer('Нет квизов')
            return
    except Exception as e:
        await msg.answer(f'Ошибка: {e}')
    
    args: str = command.args
    if args:
        quiz_name = args.split(' ')[0]
        quiz = await db.get_quiz(quiz_name)
        if not quiz:
            await msg.answer(f'Такого квиза не существует. Попробуйте еще раз через /change_quiz без аргументов')
            return
        await state.update_data(chosen=quiz)
        await msg.answer(f'Вы выбрали квиз {quiz.name}')
        await msg.answer('Выйти из меню изменения квиза на /cancel')
        await bot.set_my_commands(kb.commands_change_quiz(), BotCommandScopeChat(chat_id=msg.from_user.id))
        await state.set_state(ChQuiz.ch_action)
        return
    
    await msg.answer('Отмена на /cancel')
    await msg.answer('Выберете квиз, который хотите изменить (номер):')
    for i, quiz in enumerate(quizs):
        await msg.answer(f'{i + 1}. {quiz.name}')
    await state.set_state(ChQuiz.ch_name)

@router.message(ChQuiz.ch_name)
async def ch_quiz(msg: Message, state: FSMContext):
    try:
        index = int(msg.text) - 1
        quizs = await db.get_quizs()
        if 0 <= index < len(quizs):
            chosen_quiz = quizs[index]
            await state.update_data(chosen=chosen_quiz)
            await msg.answer(f'Вы выбрали квиз "{chosen_quiz.name}"')
            await msg.answer('Выйти из меню изменения квиза на /cancel')
            await bot.set_my_commands(kb.commands_change_quiz(), BotCommandScopeChat(chat_id=msg.from_user.id))
            await state.set_state(ChQuiz.ch_action)
        else:
            await msg.answer('Некорректный индекс. Пожалуйста, введите номер квиза снова, либо выйдите на /cancel')
    except ValueError:
        await msg.answer('Некорректный ввод. Пожалуйста, введите номер квиза, либо выйдите на /cancel')
    except Exception as e:
        await msg.answer(f'Ошибка: {e}')
        
# TODO вывод результатов квиза
