import datetime

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, BotCommandScopeChat, CallbackQuery
from aiogram.types.input_file import FSInputFile
from aiogram.utils.deep_linking import decode_payload
from aiogram.fsm.context import FSMContext

from create_bot import bot
from db_handler import db
from utils.filter import is_moder
import keyboards.all_keyboards as kb
from keyboards.callback_handler import CubeExit
from handlers.quiz_handler import is_quiz_active

router = Router()

# Старт для QR
@router.message(CommandStart(deep_link=True))
async def cmd_start(msg: Message, command: CommandObject):
    args = command.args
    reference = decode_payload(args)
    
    # Переход к программе
    if(reference == 'program'):
        # TODO проверить скорость
        photo = FSInputFile("img/event_program.jpg")
        await bot.delete_messages(
            msg.from_user.id,
            [msg.message_id - i for i in range(1,3)]
        )
        await bot.send_photo(chat_id=msg.chat.id, photo=photo)
        return
    
    # Подключение к кубу
    try:
        cube_id = int(reference.split('_')[-1])
    except:
        return
    
    if cube_id > 120 or cube_id < 1:
        return
    
    connected_at = datetime.datetime.now()
    
    user_exists = await db.check_user_exists(msg.from_user.id) 
    if user_exists:
        await msg.answer("Вы уже зарегистрированы!", reply_markup=kb.get_quit(cube_id))
    elif (await db.add_user_to_cube(cube_id, msg.from_user.username, msg.from_user.id, connected_at)):
        await msg.answer("Добро пожаловать на квиз!\n\nКак только начнется квиз, вы будете получать вопросы.\nОтвечайте, нажимая на кнопки!")
    else:
        await msg.answer("Куб уже занят другим пользователем.")
    await msg.delete()

@router.callback_query(CubeExit.filter())
async def start_handler(callback: CallbackQuery, callback_data: CubeExit):
    await callback.message.delete_reply_markup()
    await db.remove_user(callback_data.cube_id)
    await callback.message.edit_text('Вы вышли из квиза')

@router.callback_query(F.data == 'back_to_quesion')
async def start_handler(callback: CallbackQuery):
    await callback.message.delete()

# Старт для модератора
@router.message(is_moder, Command("start"))
async def cmd_start_mod(msg: Message, state: FSMContext):
    await state.clear()
    
    if(is_quiz_active()):
        msg_bot = await msg.answer("Сейчас идет квиз\nПосле квиза вы можете использовать /start")
    else:
        msg_bot = await msg.answer(
            "Привет, модератор!\n\nВыберите действие",
            reply_markup=kb.get_management_kb()
        )
    
    await bot.set_my_commands(kb.commands_moder(), BotCommandScopeChat(chat_id=msg.from_user.id))
    await bot.delete_messages(
        msg.from_user.id,
        [msg_bot.message_id - i for i in range(1, 100)]
    )