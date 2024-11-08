import random
import asyncio
import time

from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.callback_handler import inline_kb
import keyboards.all_keyboards as kb
from mqtt.mqtt_handler import wled_publish, cube_on, cube_off
from utils.presets import breathe_effect, no_blinck, fast_breathe_effect

router = Router()

# ============== INLINE CALLBACS =============

@router.callback_query(F.data == 'moder_panel')
async def cube_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Выберете действие",
        reply_markup=kb.get_management_kb()
    )

# -------- Управление кубами ------------

@router.callback_query(F.data == 'cube_management')
async def cube_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Управление кубами",
        reply_markup=kb.get_cube_kb()
    )

@router.callback_query(F.data == 'cube_on')
async def cube_handler(callback: CallbackQuery):
    await cube_on()
    await callback.answer(show_alert=False)
    
@router.callback_query(F.data == 'cube_off')
async def cube_handler(callback: CallbackQuery):
    await cube_off()
    await callback.answer(show_alert=False)

@router.callback_query(F.data == 'cube_presets')
async def cube_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Пресеты",
        reply_markup=kb.get_color_blink_kb()
    )


@router.callback_query(F.data.startswith('color_'))
async def cubes_color(callback: CallbackQuery):
    color = callback.data.split('_')[1]
    await wled_publish('cubes/col', color)

# Тут только через пресеты на wled
@router.callback_query(F.data == 'blink')
async def cubes_blink(callback: CallbackQuery):
    await wled_publish('cubes/api', breathe_effect())

@router.callback_query(F.data == 'fast_blink')
async def cubes_fast_blink(callback: CallbackQuery):
    await wled_publish('cubes/api', fast_breathe_effect())

@router.callback_query(F.data == 'blink_off')
async def cubes_blink_off(callback: CallbackQuery):
    await wled_publish('cubes/api', no_blinck())

# ----- Разделение кубов по цвету

@router.callback_query(F.data == 'one_color')
async def cubes_color(callback: CallbackQuery):
    await wled_publish(f'cubes/col', '#00FF7F')

@router.callback_query(F.data == 'two_color')
async def cubes_color(callback: CallbackQuery):
    await wled_publish(f'cubes/col', '#00FF7F')
    for i in range(61, 121):
        await wled_publish(f'cube_{i}/col', '#00FFFF')

@router.callback_query(F.data == 'two_color_random')
async def cubes_color(callback: CallbackQuery):
    numbers = list(range(1, 121))
    random.shuffle(numbers)
    random_half = numbers[:60]
    await wled_publish(f'cubes/col', '#00FF7F')
    for i in random_half:
        await wled_publish(f'cube_{i}/col', '#00FFFF')