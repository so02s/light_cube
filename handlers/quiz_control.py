from aiogram import Router, F
from aiogram.types import CallbackQuery
from handlers.quiz_handler import QuizMiddleware
from mqtt.mqtt_handler import wled_publish, blink_cubes, cube_on, cube_off
from keyboards.keyboard_hendler import inline_kb
import keyboards.all_keyboards as kb

router = Router()

# -------- Управление квизом ------------

@router.callback_query(F.data == 'quiz_management')
async def quiz_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Управление квизами",
        kb.get_quiz_keyboard()
    )

@router.callback_query(F.data == 'start_quiz')
async def quiz_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Выберите какой квиз вы хотите начать",
        await kb.get_all_quizs_keyboard('start')
    )

@router.callback_query(F.data == 'change_program')
async def quiz_handler(callback: CallbackQuery):
    # TODO изменение картинки
    pass

@router.callback_query(F.data == 'add_quiz')
async def quiz_handler(callback: CallbackQuery):
    # TODO каким образом добавлять квизы?
    pass

@router.callback_query(F.data == 'edit_quiz')
async def quiz_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Выберите какой квиз вы хотите изменить",
        await kb.get_all_quizs_keyboard('edit')
    )

@router.callback_query(F.data == 'delete_quiz')
async def quiz_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Выберите какой квиз вы хотите удалить",
        await kb.get_all_quizs_keyboard('delete')
    )