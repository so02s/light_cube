import random

from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.callback_handler import inline_kb
import keyboards.all_keyboards as kb
from mqtt.mqtt_handler import wled_publish, cube_on, cube_off


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
    print(color)
    await wled_publish('cubes/col', color)

# TODO чекнуть и загрузить пресеты
# Тут только через пресеты на wled
@router.callback_query(F.data == 'blink')
async def cubes_blink(callback: CallbackQuery):
    await wled_publish('cubes/api', 1)

@router.callback_query(F.data == 'fast_blink')
async def cubes_fast_blink(callback: CallbackQuery):
    await wled_publish('cubes/api', 2)

@router.callback_query(F.data == 'blink_off')
async def cubes_blink_off(callback: CallbackQuery):
    await wled_publish('cubes/api', 0)

# ----- Разделение кубов по цвету

@router.callback_query(F.data == 'one_color')
async def cubes_color(callback: CallbackQuery):
    for i in range(1, 121):
        await wled_publish(f'cube_{i}/col', '#00FF7F')

@router.callback_query(F.data == 'two_color')
async def cubes_color(callback: CallbackQuery):
    for i in range(1, 61):
        await wled_publish(f'cube_{i}/col', '#00FF7F')
    for i in range(61, 121):
        await wled_publish(f'cube_{i}/col', '#00FFFF')

@router.callback_query(F.data == 'two_color_random')
async def cubes_color(callback: CallbackQuery):
    index = [i for i in range(1, 121)]
    random.shuffle(index)
    mid_index = len(index) // 2
    first_half = index[:mid_index]
    second_half = index[mid_index:]
    for i in first_half:
        await wled_publish(f'cube_{i}/col', '#00FF7F')
    for i in second_half:
        await wled_publish(f'cube_{i}/col', '#00FFFF')