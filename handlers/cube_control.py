from aiogram import Router, F
from aiogram.types import CallbackQuery
from handlers.quiz_handler import QuizMiddleware
from mqtt.mqtt_handler import wled_publish, blink_cubes, cube_on, cube_off
from keyboards.keyboard_hendler import inline_kb
import keyboards.all_keyboards as kb

router = Router()

# ============== INLINE CALLBACS =============

@router.callback_query(F.data == 'moder_panel')
async def cube_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Выберете действие",
        kb.get_management_keyboard()
    )


# -------- Управление кубами ------------

@router.callback_query(F.data == 'cube_management')
async def cube_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Управление кубами",
        kb.get_cube_keyboard()
    )

@router.callback_query(F.data == 'cube_on')
async def cube_handler(callback: CallbackQuery):
    await cube_on()
    
@router.callback_query(F.data == 'cube_off')
async def cube_handler(callback: CallbackQuery):
    await cube_off()

@router.callback_query(F.data == 'cube_presets')
async def cube_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Пресеты",
        kb.get_color_blink_keyboard()
    )

@router.callback_query(F.data.startswith('color_'))
async def cubes_color(callback: CallbackQuery):
    color = F.data.split('_')[1]
    await wled_publish('cubes', color)

@router.callback_query(F.data == 'blink_on')
async def cubes_color(callback: CallbackQuery):
    await blink_cubes()

@router.callback_query(F.data == 'blink_off')
async def cubes_color(callback: CallbackQuery):
    await cube_on()
