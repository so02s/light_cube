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

class ChangeAnswText(StatesGroup):
    ch_text = State()
    
# -------- Выход из FSM 

@router.message(
    Command("cancel"),
    StateFilter(ChangeAnswText.ch_text)
)
async def edit_answer_repl(
    msg: Message,
    state: FSMContext
):
    await bot.delete_messages(msg.from_user.id, [msg.message_id - i for i in range(2)])
    answer_id = (await state.get_data())['answer_id']
    answer = await db.get_answer_by_id(answer_id)
    text = 'Правильный ответ' if answer.is_correct else 'Неправильный ответ'
    hex_color = kb.hex_to_color.get(answer.color, 'серый')
    response_text = (
        f"{answer.text}\n\n"
        f"Цвет: {hex_color}\n"
        f"{text}"
    )
    await msg.answer(
        response_text,
        reply_markup=kb.get_edit_answer_kb(answer.question_id, answer_id)
    )
    await state.clear()

# ------ Изменение ответа (выбор)

@router.callback_query(QuestionCallbackFactory.filter(F.action =='change_answer'))
async def edit_answer(
    callback: CallbackQuery,
    callback_data: QuestionCallbackFactory
):
    await inline_kb(
        callback,
        "Выберите какой ответ вы хотите изменить",
        reply_markup= await kb.get_all_answer_kb(callback_data.question_id, 'edit')
    )

# ------ Изменение ответа

@router.callback_query(AnswerCallbackFactory.filter(F.action =='edit'))
async def edit_answer_handler(
    callback: CallbackQuery,
    callback_data: AnswerCallbackFactory
):
    answer_id = callback_data.answer_id
    answer = await db.get_answer_by_id(answer_id)
    text = 'Правильный ответ' if answer.is_correct else 'Неправильный ответ'
    hex_color = kb.hex_to_color.get(answer.color, 'серый')
    response_text = (
        f"{answer.text}\n\n"
        f"Цвет: {hex_color}\n"
        f"{text}"
    )
    await inline_kb(
        callback,
        response_text,
        reply_markup=kb.get_edit_answer_kb(answer.question_id, answer_id) 
    )
    
    
# Правильность

@router.callback_query(AnswerCallbackFactory.filter(F.action =='change_correctness'))
async def edit_answer(
    callback: CallbackQuery,
    callback_data: AnswerCallbackFactory
):
    await db.update_answer_cor(callback_data.answer_id)
    await edit_answer_handler(callback, callback_data)
    
# Текст

@router.callback_query(AnswerCallbackFactory.filter(F.action =='change_text'))
async def edit_answer(
    callback: CallbackQuery,
    callback_data: AnswerCallbackFactory,
    state: FSMContext
):
    answer_id = callback_data.answer_id
    answer = await db.get_answer_by_id(answer_id)
    await callback.message.answer(f'Введите текст ответа, на который хотите поменять\n{answer.text}\n\nОтмена на /cancel')
    await callback.message.delete()
    await state.update_data(answer_id=answer_id)
    await state.set_state(ChangeAnswText.ch_text)
    
@router.message(ChangeAnswText.ch_text)
async def add_quiz(
    msg: Message,
    state: FSMContext
):    
    answer_id = (await state.get_data())['answer_id']
    await db.update_answer_text(answer_id, msg.text)
    await edit_answer_repl(msg, state)
    
# Цвет

@router.callback_query(AnswerCallbackFactory.filter(F.action =='change_color'))
async def edit_answer(
    callback: CallbackQuery,
    callback_data: AnswerCallbackFactory
):
    await inline_kb(
        callback,
        'Выберите цвет ответа',
        reply_markup=kb.get_answer_color_kb(callback_data.answer_id) 
    )

@router.callback_query(AnswerCallbackFactory.filter(F.action =='change_color_answ'))
async def edit_answer(
    callback: CallbackQuery,
    callback_data: AnswerCallbackFactory
):
    answer_id = callback_data.answer_id
    await db.update_answer_color(answer_id, callback_data.color)
    await edit_answer_handler(callback, callback_data)