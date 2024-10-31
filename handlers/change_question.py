import re
import datetime

from aiogram import Router, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.types import Message, BotCommandScopeChat, CallbackQuery

from create_bot import bot
import keyboards.all_keyboards as kb
from keyboards.callback_handler import inline_kb, QuizCallbackFactory, QuestionCallbackFactory, AnswerCallbackFactory
from db_handler import db
from handlers.scheduler_handler import schedule_update_job


router = Router()

# -------- FSM

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class ChangeQuestTime(StatesGroup):
    ch_time = State()
    
class ChangeQuestText(StatesGroup):
    ch_text = State()
    
class AddAnswer(StatesGroup):
    ch_text = State()

# -------- Выход из FSM 

@router.message(
    Command("cancel"),
    StateFilter(
        ChangeQuestTime.ch_time,
        ChangeQuestText.ch_text,
        AddAnswer.ch_text
        )
)
async def edit_question(
    msg: Message,
    state: FSMContext
):
    await bot.delete_messages(msg.from_user.id, [msg.message_id - i for i in range(2)])
    
    question_id = (await state.get_data())['question_id']
    question = await db.get_question_by_id(question_id)
    minutes, seconds = divmod(question.time_limit_seconds, 60)
    answers = await db.get_answers(question)
    if not answers:
        text = 'Нет ответов'
    else:
        text = 'Ответы:\n'
        for answer in answers:
            correct_mark = "✔️" if answer.is_correct else "❌"
            text += f'{correct_mark} {answer.text} - {kb.hex_to_color.get(answer.color, 'серый')} цвет\n'
    await msg.answer(
        f'{question.text}\nВремя на выполнение: {minutes:02d}:{seconds:02d}\n\n{text}',
        reply_markup=kb.get_edit_question_kb(question.quiz_id, question_id)
    )
    
    await state.clear()

# -------- Изменение вопроса

@router.callback_query(QuizCallbackFactory.filter(F.action =='change_question'))
async def edit_question_choise(
    callback: CallbackQuery,
    callback_data: QuizCallbackFactory
):
    await inline_kb(
        callback,
        "Выберите какой вопрос вы хотите изменить",
        reply_markup= await kb.get_all_question_kb(callback_data.quiz_id, 'edit')
    )

@router.callback_query(QuestionCallbackFactory.filter(F.action =='edit'))
async def edit_question_handler(
    callback: CallbackQuery,
    callback_data: QuestionCallbackFactory
):
    question_id = callback_data.question_id
    question = await db.get_question_by_id(question_id)
    minutes, seconds = divmod(question.time_limit_seconds, 60)
    answers = await db.get_answers(question)
    if not answers:
        text = 'Нет ответов'
    else:
        text = 'Ответы:\n'
        for answer in answers:
            correct_mark = "✔️" if answer.is_correct else "❌"
            text += f'{correct_mark} {answer.text} - {kb.hex_to_color.get(answer.color, 'серый')} цвет\n'
    await inline_kb(
        callback,
        f'{question.text}\nВремя на выполнение: {minutes:02d}:{seconds:02d}\n\n{text}',
        reply_markup=kb.get_edit_question_kb(question.quiz_id, question_id) 
    )

# ------ Изменение времени вопроса 

@router.callback_query(QuestionCallbackFactory.filter(F.action =='change_time'))
async def edit_question_handler(
    callback: CallbackQuery,
    callback_data: QuestionCallbackFactory,
    state: FSMContext
):
    await callback.message.answer('Введите время на вопрос (мин:сек)\nПример: 01:30\n\nОтмена на /cancel')
    await callback.message.delete()
    await state.update_data(question_id=callback_data.question_id)
    await state.set_state(ChangeQuestTime.ch_time)

@router.message(ChangeQuestTime.ch_time)
async def add_quiz(
    msg: Message,
    state: FSMContext
):
    time_parts = msg.text.split(':')
    if len(time_parts) != 2:
        await msg.answer('Неверный формат времени. Пожалуйста, введите время в формате "мин:сек".\n(Либо отмените действие на /cancel)')
        return
    try:
        minutes, seconds = map(int, time_parts)
    except:
        await msg.answer('Неверный формат времени. Пожалуйста, введите время в формате "мин:сек".\n(Либо отмените действие на /cancel)')
        return
    if not(0 <= minutes <= 59 and 0 <= seconds <= 59):
        await msg.answer('Неверное время. Пожалуйста, введите время в формате "мин:сек", где мин не больше 59 и сек не больше 59.\n(Либо отмените действие на /cancel)')
        return
    
    question_id = (await state.get_data())['question_id']
    await db.update_question_time(question_id, minutes * 60 + seconds)
    await edit_question(msg, state)

# Изменение текста вопроса

@router.callback_query(QuestionCallbackFactory.filter(F.action =='change_text'))
async def edit_question_handler(
    callback: CallbackQuery,
    callback_data: QuestionCallbackFactory,
    state: FSMContext
):
    question_id = callback_data.question_id
    question = await db.get_question_by_id(question_id)
    await callback.message.answer(f'Введите текст вопроса, на который хотите поменять\n{question.text}\n\nОтмена на /cancel')
    await callback.message.delete()
    await state.update_data(question_id=question_id)
    await state.set_state(ChangeQuestText.ch_text)

@router.message(ChangeQuestText.ch_text)
async def add_quiz(
    msg: Message,
    state: FSMContext
):    
    question_id = (await state.get_data())['question_id']
    await db.update_question_text(question_id, msg.text)
    await edit_question(msg, state)

# Добавление ответа

@router.callback_query(QuestionCallbackFactory.filter(F.action =='add_answer'))
async def add_answer(
    callback: CallbackQuery,
    callback_data: QuestionCallbackFactory,
    state: FSMContext
):
    question_id = callback_data.question_id
    answers = await db.get_answers_by_id(question_id)
    if(len(answers) == 10):
        await inline_kb(
            callback,
            'Можно добавить только 10 ответов',
            kb.get_done_kb(QuestionCallbackFactory(question_id=question_id, action='edit'))
        )
        return
    await callback.message.answer('Введите ответ.\nОтмена на /cancel')
    await callback.message.delete()
    await state.update_data(question_id=question_id)
    await state.set_state(AddAnswer.ch_text)

@router.message(AddAnswer.ch_text)
async def add_answer(
    msg: Message,
    state: FSMContext
):
    question_id = (await state.get_data())['question_id']
    await bot.delete_messages(msg.from_user.id, [msg.message_id - i for i in range(2)])
    answer_id = await db.add_answ(msg.text, question_id)
    await msg.answer(
        f'Добавлен ответ\n{msg.text}',
        reply_markup=kb.get_edit_answer_kb(question_id, answer_id)
    )
    await state.clear()

# Удаление ответа

@router.callback_query(QuestionCallbackFactory.filter(F.action =='delete_answer'))
async def cube_handler(
    callback: CallbackQuery,
    callback_data: QuestionCallbackFactory
):
    await inline_kb(
        callback,
        "Выберите какой ответ вы хотите удалить",
        reply_markup= await kb.get_all_answer_kb(callback_data.question_id, 'delete')
    )
    
@router.callback_query(AnswerCallbackFactory.filter(F.action == 'delete')) 
async def confirm_delete_question_handler(
    callback: CallbackQuery,
    callback_data: AnswerCallbackFactory
): 
    answer_id = callback_data.answer_id 
    answer = await db.get_answer_by_id(answer_id) 
    await inline_kb(
        callback,
        f"Вы уверены, что хотите удалить ответ:\n{answer.text}",
        reply_markup=kb.get_confirm_delete_kb(
            next_step=AnswerCallbackFactory(answer_id=answer_id, action='confirm_delete'),
            before_step=QuestionCallbackFactory(question_id=answer.question_id, action='edit')
        )
    )

@router.callback_query(AnswerCallbackFactory.filter(F.action == 'confirm_delete')) 
async def execute_delete_question_handler(
    callback: CallbackQuery,
    callback_data: AnswerCallbackFactory
): 
    answer_id = callback_data.answer_id
    answer = await db.get_answer_by_id(answer_id) 
    await db.del_answer(answer) 
    await inline_kb(
        callback,
        f"Ответ успешно удален",
        reply_markup=kb.get_done_kb(
            QuestionCallbackFactory(question_id=answer.question_id, action='edit')
        )
    )

# ------ Смена порядка

@router.callback_query(QuizCallbackFactory.filter(F.action =='shuffle_question'))
async def edit_question_choise(
    callback: CallbackQuery,
    callback_data: QuizCallbackFactory
):
    await inline_kb(
        callback,
        "Выберите какой вопрос вы хотите подвинуть",
        reply_markup= await kb.get_all_question_kb(callback_data.quiz_id, 'shuffle_to')
    )

@router.callback_query(QuestionCallbackFactory.filter(F.action =='shuffle_to'))
async def edit_question_handler(
    callback: CallbackQuery,
    callback_data: QuestionCallbackFactory
):
    question_id = callback_data.question_id
    question = await db.get_question_by_id(question_id)
    await inline_kb(
        callback,
        "На какое место?",
        reply_markup= await kb.get_all_question_without_kb(callback_data.question_id, question.quiz_id, 'shuffle')
    )

@router.callback_query(QuestionCallbackFactory.filter(F.action =='shuffle'))
async def edit_question_handler(
    callback: CallbackQuery,
    callback_data: QuestionCallbackFactory
):
    question_id = callback_data.question_id
    shuffle_to = await db.get_question_by_id(callback_data.question_shuffle)
    await db.shuffle_quest(question_id, shuffle_to.question_number)
    question = await db.get_question_by_id(question_id)
    await inline_kb(
        callback,
        "Сделано!",
        reply_markup=kb.get_done_kb(QuizCallbackFactory(quiz_id=question.quiz_id, action='edit'))
    )