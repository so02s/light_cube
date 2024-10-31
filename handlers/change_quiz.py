import re
import datetime

from aiogram import Router, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.types import Message, BotCommandScopeChat, CallbackQuery

from create_bot import bot
import keyboards.all_keyboards as kb
from keyboards.callback_handler import inline_kb, QuizCallbackFactory, QuestionCallbackFactory
from db_handler import db
from handlers.scheduler_handler import schedule_update_job


router = Router()

# -------- FSM

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class ChangeQuizTime(StatesGroup):
    ch_time = State()
    
class AddQuest(StatesGroup):
    ch_text = State()

# -------- Выход из FSM 

@router.message(
    Command("cancel"),
    StateFilter(
        ChangeQuizTime.ch_time,
        AddQuest.ch_text
        )
)
async def edit_quiz(msg: Message, state: FSMContext):
    await bot.delete_messages(msg.from_user.id, [msg.message_id - i for i in range(2)])
    
    quiz_id = (await state.get_data())['quiz_id']
    quiz = await db.get_quiz_by_id(quiz_id)
    time = quiz.start_datetime.strftime('%d.%m.%Y в %H:%M')
    time = '----' if time.startswith('01.01.2026') else time
    questions = await db.get_questions(quiz)
    if not questions:
        text = 'Нет вопросов'
    else:
        quest = '\n'.join([f'{i+1}. {q.text}' for i, q in enumerate(questions)])
        text = 'Вопросы:\n' + quest
    await msg.answer(
        f'Квиз {quiz.name}\nВремя начала: {time}\n\n{text}',
        reply_markup=kb.get_edit_quiz_kb(quiz_id)
    )
    
    await state.clear()

# -------- Информация о квизе

@router.callback_query(QuizCallbackFactory.filter(F.action == 'edit'))
async def edit_quiz_handler(callback: CallbackQuery, callback_data: QuizCallbackFactory):
    quiz_id = callback_data.quiz_id
    quiz = await db.get_quiz_by_id(quiz_id)
    time = quiz.start_datetime.strftime('%d.%m.%Y в %H:%M')
    time = '----' if time.startswith('01.01.2026') else time
    questions = await db.get_questions(quiz)
    if not questions:
        text = 'Нет вопросов'
    else:
        quest = '\n'.join([f'{i+1}. {q.text}' for i, q in enumerate(questions)])
        text = 'Вопросы:\n' + quest
    await inline_kb(
        callback,
        f'Квиз {quiz.name}\nВремя начала: {time}\n\n{text}',
        reply_markup=kb.get_edit_quiz_kb(quiz_id)
    )

# -------- Изменение времени начала

@router.callback_query(QuizCallbackFactory.filter(F.action =='change_start_time'))
async def start_time(
    callback: CallbackQuery,
    callback_data: QuizCallbackFactory,
    state: FSMContext
):
    await callback.message.answer('Введите время начала квиза (день.месяц.год час:мин)\nПример: 27.10.2024 19:00\n\nОтмена на /cancel')
    await callback.message.delete()
    await state.update_data(quiz_id=callback_data.quiz_id)
    await state.set_state(ChangeQuizTime.ch_time)

@router.message(ChangeQuizTime.ch_time)
async def add_quiz(msg: Message, state: FSMContext):
    time = msg.text
    try:
        datetime.datetime.strptime(time, "%d.%m.%Y %H:%M")
    except ValueError:
        await bot.delete_messages(msg.from_user.id, [msg.message_id - i for i in range(2)])
        await msg.answer('Неправильный формат даты и времени. Пожалуйста, введите дату и время в формате "день.месяц.год час:мин"\n\nОтмена на /cancel')
        return
    
    quiz_id = (await state.get_data())['quiz_id']
    await db.set_quiz_time(time, quiz_id)
    await schedule_update_job(quiz_id)
    await edit_quiz(msg, state)

# -------- Добавление вопроса

@router.callback_query(QuizCallbackFactory.filter(F.action =='add_question'))
async def cube_handler(callback: CallbackQuery, callback_data: QuizCallbackFactory, state: FSMContext):
    await callback.message.answer('Введите вопрос.\nОтмена на /cancel')
    await callback.message.delete()
    await state.update_data(quiz_id=callback_data.quiz_id)
    await state.set_state(AddQuest.ch_text)

@router.message(AddQuest.ch_text)
async def add_quiz(msg: Message, state: FSMContext):
    quiz_id = (await state.get_data())['quiz_id']
    await bot.delete_messages(msg.from_user.id, [msg.message_id - i for i in range(2)])
    question_id = await db.add_question(msg.text, quiz_id)
    await msg.answer(
        f'Добавлен вопрос\n{msg.text}',
        reply_markup=kb.get_edit_question_kb(quiz_id, question_id)
    )
    await state.clear()

# -------- Удаление вопроса

@router.callback_query(QuizCallbackFactory.filter(F.action =='delete_question'))
async def cube_handler(callback: CallbackQuery, callback_data: QuizCallbackFactory):
    await inline_kb(
        callback,
        "Выберите какой вопрос вы хотите удалить",
        reply_markup= await kb.get_all_question_kb(callback_data.quiz_id, 'delete')
    )
    
@router.callback_query(QuestionCallbackFactory.filter(F.action == 'delete')) 
async def confirm_delete_question_handler(callback: CallbackQuery, callback_data: QuestionCallbackFactory): 
    question_id = callback_data.question_id 
    question = await db.get_question_by_id(question_id) 
    await inline_kb(
        callback,
        f"Вы уверены, что хотите удалить вопрос:\n{question.text}",
        reply_markup=kb.get_confirm_delete_kb(
            next_step=QuestionCallbackFactory(question_id=question_id, action='confirm_delete'),
            before_step=QuizCallbackFactory(quiz_id=question.quiz_id, action='edit')
        )
    )

@router.callback_query(QuestionCallbackFactory.filter(F.action == 'confirm_delete')) 
async def execute_delete_question_handler(callback: CallbackQuery, callback_data: QuestionCallbackFactory): 
    question_id = callback_data.question_id
    question = await db.get_question_by_id(question_id) 
    await db.del_question(question) 
    await inline_kb(
        callback,
        f"Вопрос успешно удален",
        reply_markup=kb.get_done_kb(
            QuizCallbackFactory(quiz_id=question.quiz_id, action='edit')
        )
    )