from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from handlers.quiz_handler import QuizMiddleware
from mqtt.mqtt_handler import wled_publish, blink_cubes, cube_on, cube_off
from keyboards.callback_handler import inline_kb
import keyboards.all_keyboards as kb
from create_bot import bot
from aiogram.types.input_file import FSInputFile
from keyboards.callback_handler import QuizCallbackFactory
from db_handler import db
from handlers.scheduler_handler import schedule_del_job
from aiogram.filters import Command, StateFilter
from create_bot import bot

router = Router()


# ------- FSM

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class AddQuiz(StatesGroup):
    ch_name = State()
class Form(StatesGroup):
    waiting_for_photo = State()

# -------- Выход из FSM

@router.message(
    Command("cancel"),
    StateFilter(
        AddQuiz.ch_name,
        Form.waiting_for_photo
    )
)
async def add_quiz(msg: Message, state: FSMContext):
    await bot.delete_messages(msg.from_user.id, [msg.message_id - i for i in range(2)])
    await msg.answer(
        "Управление квизами",
        reply_markup=kb.get_quiz_kb()
    )
    await state.clear()
    
# -------- Управление квизами ------------

@router.callback_query(F.data == 'quiz_management')
async def first_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Управление квизами",
        reply_markup=kb.get_quiz_kb()
    )

# ------- Запуск квиза

@router.callback_query(F.data == 'start_quiz')
async def quiz_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Выберите какой квиз вы хотите начать",
        reply_markup= await kb.get_all_quizs_kb('start')
    )

# ------- Программа мероприятия

@router.callback_query(F.data == 'event_program')
async def quiz_handler(callback: CallbackQuery):
    photo = FSInputFile("img/event_program.jpg")
    await callback.message.answer_photo(photo, reply_markup=kb.get_event_program_kb())
    await callback.message.delete()

@router.callback_query(F.data == 'back_from_event_program')
async def quiz_handler(callback: CallbackQuery):
    await callback.message.answer("Управление квизами", reply_markup=kb.get_quiz_kb())
    await callback.message.delete()

@router.callback_query(F.data == 'edit_program')
async def quiz_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста, отправьте фото для программы мероприятия.")
    await Form.waiting_for_photo.set()
    await callback.message.delete()

@router.message(State=Form.waiting_for_photo, content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)

    file_path = f"img/event_program.jpg"
    await message.bot.download_file(file.file_path, file_path)

    await message.answer("Фото успешно загружено!")
    await state.finish()

@router.message(State=Form.waiting_for_photo)
async def invalid_photo_handler(message: types.Message):
    await message.answer("Пожалуйста, отправьте фото.")
    
# ------- Добавление

@router.callback_query(F.data == 'add_quiz')
async def add_quiz(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите название квиза.\nОтмена на /cancel')
    await callback.message.delete()
    await state.set_state(AddQuiz.ch_name)
    
@router.message(AddQuiz.ch_name)
async def add_quiz(msg: Message, state: FSMContext):
    await bot.delete_messages(msg.from_user.id, [msg.message_id - i for i in range(2)])
    quiz_id = await db.add_quiz(msg.text)
    await msg.answer(
        f'Добавлен квиз\n{msg.text}',
        reply_markup=kb.get_edit_quiz_kb(quiz_id)
    )
    await state.clear()

# -------- Изменение

@router.callback_query(F.data == 'edit_quiz')
async def quiz_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Выберите какой квиз вы хотите изменить",
        reply_markup= await kb.get_all_quizs_kb('edit')
    )

# -------- Удаление

@router.callback_query(F.data == 'delete_quiz')
async def quiz_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Выберите какой квиз вы хотите удалить",
        reply_markup= await kb.get_all_quizs_kb('delete')
    )

@router.callback_query(QuizCallbackFactory.filter(F.action == 'delete'))
async def edit_quiz_handler(callback: CallbackQuery, callback_data: QuizCallbackFactory):
    quiz_id = callback_data.quiz_id
    quiz = await db.get_quiz_by_id(quiz_id)
    await inline_kb(
        callback,
        f"Вы уверены, что хотите удалить {quiz.name}?",
        reply_markup=kb.get_confirm_delete_kb(
            next_step=QuizCallbackFactory(quiz_id=quiz_id, action='confirm delete'),
            before_step='quiz_management'
        )
    )

@router.callback_query(QuizCallbackFactory.filter(F.action == 'confirm delete'))
async def edit_quiz_handler(callback: CallbackQuery, callback_data: QuizCallbackFactory):
    quiz_id = callback_data.quiz_id
    await db.del_quiz_by_id(quiz_id)
    await schedule_del_job(quiz_id)
    await inline_kb(
        callback,
        f"Квиз успешно удален",
        reply_markup=kb.get_delete_done_kb('quiz_management')
    )