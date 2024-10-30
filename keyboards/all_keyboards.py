from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from db_handler import db
from keyboards.callback_handler import QuizCallbackFactory, QuestionCallbackFactory, AnswerCallbackFactory, UserCallbackFactory

hex_to_color = {
    '#FF0000': 'красный',
    '#0000FF': 'синий',
    '#FFFF00': 'желтый',
    '#00FF00': 'зеленый',
    '#FFA500': 'оранжевый',
    '#800080': 'фиолетовый',
    '#00CED1': 'голубой',
}

def get_management_kb():
    buttons = [
        [   InlineKeyboardButton(text="Управление кубами", callback_data="cube_management")],
        [   InlineKeyboardButton(text="Квизы и мероприятие", callback_data="quiz_management")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def get_cube_kb():
    buttons = [
        [
            InlineKeyboardButton(text="Вкл", callback_data="cube_on"),
            InlineKeyboardButton(text="Выкл", callback_data="cube_off")
        ],
        [   InlineKeyboardButton(text="Пресеты", callback_data="cube_presets")],
        [   InlineKeyboardButton(text="Назад", callback_data="moder_panel")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb


# TODO добавить необходимые цвета
def get_color_blink_kb():
    buttons = [
        [
            InlineKeyboardButton(text="Красный", callback_data="color_#FF0000"),
            InlineKeyboardButton(text="Синий", callback_data="color_#0000CD"),
        ],
        [
            InlineKeyboardButton(text="Медленное мигание", callback_data="blink"),
            InlineKeyboardButton(text="Быстрое мигание", callback_data="fast_blink"),
            InlineKeyboardButton(text="Выкл мигание", callback_data="blink_off")
        ],
        [
            InlineKeyboardButton(text="Все", callback_data="one_color"),
            InlineKeyboardButton(text="Половина", callback_data="two_color"),
            InlineKeyboardButton(text="Рандомная половина", callback_data="two_color_random")
        ],
        [   InlineKeyboardButton(text="Назад", callback_data="cube_management")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def get_quiz_kb():
    buttons = [
        [   InlineKeyboardButton(text="Программа", callback_data="event_program")],
        [   InlineKeyboardButton(text="Вывести информацию о квизе", callback_data="info_quiz")],
        [
            InlineKeyboardButton(text="Добавить квиз", callback_data="add_quiz"),
            InlineKeyboardButton(text="Изменить квиз", callback_data="edit_quiz")
        ],
        [   InlineKeyboardButton(text="Начать квиз", callback_data="start_quiz")],
        [   InlineKeyboardButton(text="Вывести результат последнего квиза", callback_data="result_quiz")],
        [   InlineKeyboardButton(text="Удалить квиз", callback_data="delete_quiz")],
        [   InlineKeyboardButton(text="Назад", callback_data="moder_panel")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def get_sterted_quiz_kb():
    buttons = [
        [   InlineKeyboardButton(text="Остановить квиз", callback_data="start_quiz")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

async def get_all_quizs_kb(action: str):
    builder = InlineKeyboardBuilder()
    
    quizs = await db.get_quizs()
    
    if not quizs:
        builder.button(text='Нет квизов', callback_data='no_data')
    else:
        for quiz in quizs:
            builder.button(
                text=quiz.name,
                callback_data=QuizCallbackFactory(quiz_id=quiz.id, action=action)
            )
    builder.button(text="Назад", callback_data="quiz_management")
    builder.adjust(1)

    return builder.as_markup()

def get_edit_quiz_kb(quiz_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить время начала", callback_data=QuizCallbackFactory(quiz_id=quiz_id, action="change_start_time"))
    builder.button(text="Изменить вопрос", callback_data=QuizCallbackFactory(quiz_id=quiz_id, action="change_question"))
    # builder.button(text="Поменять порядок вопросов", callback_data=QuizCallbackFactory(quiz_id=quiz_id, action="shuffle_question"))
    builder.button(text="Добавить вопрос", callback_data=QuizCallbackFactory(quiz_id=quiz_id, action="add_question"))
    builder.button(text="Удалить вопрос", callback_data=QuizCallbackFactory(quiz_id=quiz_id, action="delete_question"))
    builder.button(text="Назад", callback_data="quiz_management")
    builder.adjust(1)
    return builder.as_markup()

def get_done_kb(callback_data):
    builder = InlineKeyboardBuilder()
    builder.button(text="Хорошо", callback_data=callback_data)
    return builder.as_markup()

async def get_all_question_kb(quiz_id: int, action: str):
    builder = InlineKeyboardBuilder()

    questions = await db.get_questions_by_id(quiz_id)
    
    if not questions:
        builder.button(text='Нет вопросов', callback_data='no_data')
    else:
        for question in questions:
            builder.button(
                text= question.text,
                callback_data=QuestionCallbackFactory(question_id=question.id, action=action)
            )
    builder.button(text="Назад", callback_data=QuizCallbackFactory(quiz_id=quiz_id, action="edit"))
    builder.adjust(1)

    return builder.as_markup()

async def get_all_question_without_kb(question_id: int, quiz_id: int, action: str):
    builder = InlineKeyboardBuilder()

    questions = await db.get_questions_by_id(quiz_id)
    
    if not questions:
        builder.button(text='Нет вопросов', callback_data='no_data')
    else:
        for question in questions:
            if question.id == question_id:
                continue
            builder.button(
                text=question.text,
                callback_data=QuestionCallbackFactory(question_id=question_id, action=action, question_shuffle=question.id)
            )
    builder.button(text="Назад", callback_data=QuizCallbackFactory(quiz_id=quiz_id, action="edit"))
    builder.adjust(1)

    return builder.as_markup()


def get_edit_question_kb(quiz_id: int, question_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить время на вопрос", callback_data=QuestionCallbackFactory(question_id=question_id, action="change_time"))
    builder.button(text="Изменить текст вопроса", callback_data=QuestionCallbackFactory(question_id=question_id, action="change_text"))
    builder.button(text="Добавить ответ", callback_data=QuestionCallbackFactory(question_id=question_id, action="add_answer"))
    builder.button(text="Удалить ответ", callback_data=QuestionCallbackFactory(question_id=question_id, action="delete_answer"))
    builder.button(text="Изменить ответ", callback_data=QuestionCallbackFactory(question_id=question_id, action="change_answer"))
    builder.button(text="Назад", callback_data=QuizCallbackFactory(quiz_id=quiz_id, action="edit"))
    builder.adjust(1)
    return builder.as_markup()

def get_edit_new_question_kb(quiz_id: int, question_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить время на вопрос", callback_data=QuestionCallbackFactory(question_id=question_id, action="change_time"))
    builder.button(text="Изменить текст вопроса", callback_data=QuestionCallbackFactory(question_id=question_id, action="change_text"))
    builder.button(text="Добавить ответ", callback_data=QuestionCallbackFactory(question_id=question_id, action="add_answer"))
    builder.button(text="Назад", callback_data=QuizCallbackFactory(quiz_id=quiz_id, action="edit"))
    builder.adjust(1)
    return builder.as_markup()

async def get_all_answer_kb(question_id: int, action: str):
    builder = InlineKeyboardBuilder()

    answers = await db.get_answers_by_id(question_id)
    
    if not answers:
        builder.button(text='Нет ответов', callback_data='no_data')
    else:
        for answer in answers:
            builder.button(
                text= answer.text,
                callback_data=AnswerCallbackFactory(answer_id=answer.id, action=action)
            )
    builder.button(text="Назад", callback_data=QuestionCallbackFactory(question_id=question_id, action="edit"))
    builder.adjust(1)

    return builder.as_markup()

def get_edit_answer_kb(question_id: int, answer_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить правильность ответа", callback_data=AnswerCallbackFactory(answer_id=answer_id, action="change_correctness"))
    builder.button(text="Изменить текст ответа", callback_data=AnswerCallbackFactory(answer_id=answer_id, action="change_text"))
    builder.button(text="Изменить цвет ответа", callback_data=AnswerCallbackFactory(answer_id=answer_id, action="change_color"))
    builder.button(text="Назад", callback_data=QuestionCallbackFactory(question_id=question_id, action="edit"))
    builder.adjust(1)
    return builder.as_markup()

# Подтверждение удаления

def get_confirm_delete_kb(next_step, before_step):
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data=next_step)
    builder.button(text="Назад", callback_data=before_step)
    builder.adjust(1)
    return builder.as_markup()

def get_event_program_kb():
    buttons = [
        [InlineKeyboardButton(text="Изменить программу", callback_data="edit_program")],
        [InlineKeyboardButton(text="Назад", callback_data="back_from_event_program")], 
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

def get_answer_color_kb(answer_id: int):
    builder = InlineKeyboardBuilder()
    for hex_color, color_name in hex_to_color.items():
        builder.button(
            text=color_name,
            callback_data=AnswerCallbackFactory(answer_id=answer_id, action="change_color_answ", color=hex_color)
        )
    builder.adjust(2)
    builder.button(text="Назад", callback_data=AnswerCallbackFactory(answer_id=answer_id, action="edit"))
    return builder.as_markup()

def reply_answers(answers: list):
    builder = InlineKeyboardBuilder()
    for answer in answers:
        builder.button(text=answer.text, callback_data=UserCallbackFactory(answer_id=answer.id))

def commands_moder():
    return [BotCommand(command='start', description='Старт')]