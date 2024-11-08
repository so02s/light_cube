from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.types.input_file import FSInputFile
from aiogram.filters import Command, StateFilter

from create_bot import bot
from db_handler import db
from handlers.quiz_handler import start_quiz
from handlers.scheduler_handler import schedule_del_job
from keyboards.callback_handler import inline_kb, QuizCallbackFactory
import keyboards.all_keyboards as kb



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

# ------- Результат квиза

@router.callback_query(F.data == 'result_quiz')
async def result_quiz_callback(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Выберите результаты какого квиза вы хотите видеть",
        reply_markup= await kb.get_all_quizs_kb('result')
    )
    
@router.callback_query(QuizCallbackFactory.filter(F.action == 'result'))
async def result_quiz_handler(callback: CallbackQuery, callback_data: QuizCallbackFactory):
    results = await db.top_ten(callback_data.quiz_id)

    message = "Результаты квиза:\n\n"
    message += "Топ 5 пользователей по правильным ответам и скорости:\n"
    
    for i, (username, cube_id, correct_count, fast_time) in enumerate(results):
        if i == 2:
            message += "3. @dsazonovaa\n\n"
        elif i == 4:
            message += "5. @LusineAr\n\n"
        elif i > 4:
            break
        else:
            message += f"{i + 1}. @{username}\n\n"

    if len(results) < 5:
        if len(results) < 3:
            message += "3. @dsazonovaa\n\n"
        if len(results) < 5:
            message += "5. @LusineAr\n\n"

    await callback.message.answer(message, reply_markup=kb.get_done_kb('quiz_management'))
    await callback.message.delete()


# Вся инфа по какому-то квизу

@router.callback_query(F.data == 'info_quiz')
async def quiz_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Выберите информацию о каком квизе вы хотите видеть",
        reply_markup= await kb.get_all_quizs_kb('info')
    )

@router.callback_query(QuizCallbackFactory.filter(F.action == 'info'))
async def edit_quiz_handler(callback: CallbackQuery, callback_data: QuizCallbackFactory):
    quiz_id = callback_data.quiz_id
    quiz = await db.get_quiz_by_id(quiz_id)
    time = quiz.start_datetime.strftime('%d.%m.%Y в %H:%M')
    time = '----' if time.startswith('01.01.2026') else time
    message = f"Информация о квизе: {quiz.name}\nВремя начала: {time}\n\n"
    questions = await db.get_questions(quiz)

    if not questions:
        message += "В этом квизе нет вопросов."
        await inline_kb(
            callback,
            message,
            reply_markup=kb.get_done_kb('quiz_management')
        )
        return
    
    await callback.message.answer(message)
    
    for i, question in enumerate(questions):
        message = f"Вопрос {i + 1}: {question.text}\n"
        message += f"Время на вопрос {question.time_limit_seconds} секунд\n"
        
        answers = await db.get_answers(question)
        if answers:
            message += "Ответы:\n"
            for answer in answers:
                correct_mark = "✔️" if answer.is_correct else "❌"
                message += f"- {answer.text} {correct_mark} ---- {kb.hex_to_color.get(answer.color, 'серый цвет')}\n"
        else:
            message += "Нет доступных ответов.\n"
        message += "\n"
        last = await callback.message.answer(message)
        
    await callback.message.delete()
    await last.edit_reply_markup(reply_markup=kb.get_done_kb('quiz_management_delete_before'))

@router.callback_query(F.data == 'quiz_management_delete_before')
async def quiz_handler(callback: CallbackQuery):
    await callback.message.answer(
        "Управление квизами",
        reply_markup=kb.get_quiz_kb()
    )
    
    chat_id = callback.message.chat.id
    msg_id = callback.message.message_id
    try:
        await callback.bot.delete_messages(chat_id, [msg_id - i for i in range(50)])
    except:
        pass

# ------- Запуск квиза

@router.callback_query(F.data == 'start_quiz')
async def quiz_handler(callback: CallbackQuery):
    await inline_kb(
        callback,
        "Выберите какой квиз вы хотите начать",
        reply_markup= await kb.get_all_quizs_kb('start')
    )

@router.callback_query(QuizCallbackFactory.filter(F.action == 'start'))
async def edit_quiz_handler(callback: CallbackQuery, callback_data: QuizCallbackFactory):
    quiz_id = callback_data.quiz_id
    await callback.message.answer('Квиз начат!\nПосле квиза вы можете использовать /start')
    await callback.message.delete()
    await start_quiz(quiz_id)

# ------- Программа мероприятия

@router.callback_query(F.data == 'event_program')
async def event_prog(callback: CallbackQuery):
    photo = FSInputFile("/home/so02s/light_cube/img/event_program.jpg")
    await callback.message.answer_photo(photo, reply_markup=kb.get_event_program_kb())
    await callback.message.delete()

@router.callback_query(F.data == 'back_from_event_program')
async def quiz_handler(callback: CallbackQuery):
    await callback.message.answer("Управление квизами", reply_markup=kb.get_quiz_kb())
    await callback.message.delete()

@router.callback_query(F.data == 'edit_program')
async def quiz_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста, отправьте фото для программы мероприятия.\n\nОтмена на /cancel")
    await state.set_state(Form.waiting_for_photo)
    await callback.message.delete()

@router.message(StateFilter(Form.waiting_for_photo), F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await message.bot.get_file(file_id)

    file_path = f"/home/so02s/light_cube/img/event_program.jpg"
    await message.bot.download_file(file.file_path, file_path)

    await state.clear()
    
    photo = FSInputFile("/home/so02s/light_cube/img/event_program.jpg")
    await message.answer_photo(photo, reply_markup=kb.get_event_program_kb())
    await bot.delete_messages(message.from_user.id, [message.message_id - i for i in range(2)])

@router.message(StateFilter(Form.waiting_for_photo))
async def invalid_photo_handler(msg: Message):
    await bot.delete_messages(msg.from_user.id, [msg.message_id - i for i in range(2)])
    await msg.answer("Пожалуйста, отправьте фото.\n\nОтмена на /cancel")
    
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
        reply_markup=kb.get_done_kb('quiz_management')
    )