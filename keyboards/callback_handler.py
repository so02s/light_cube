from aiogram.types import CallbackQuery, Message
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from create_bot import bot

class QuizCallbackFactory(CallbackData, prefix="fabquiz"):
    quiz_id: int
    action: str
    
class QuestionCallbackFactory(CallbackData, prefix="fabquestion"):
    question_id: int
    action: str

class AnswerCallbackFactory(CallbackData, prefix="fabanswer"):
    answer_id: int
    action: str
    color: Optional[str] = None

async def inline_kb(callback: CallbackQuery, text: str, reply_markup):
    await callback.message.edit_text(text, reply_markup=reply_markup)
