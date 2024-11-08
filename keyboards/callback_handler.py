from typing import Optional

from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData

class QuizCallbackFactory(CallbackData, prefix="fabquiz"):
    quiz_id: int
    action: str
    
class QuestionCallbackFactory(CallbackData, prefix="fabquestion"):
    question_id: int
    action: str
    question_shuffle: Optional[int] = None

class AnswerCallbackFactory(CallbackData, prefix="fabanswer"):
    answer_id: int
    action: str
    color: Optional[str] = None

class UserCallbackFactory(CallbackData, prefix="fabuser"):
    answer_id: int
    cube_id: int

class CubeExit(CallbackData, prefix="fabexit"):
    cube_id: int

async def inline_kb(callback: CallbackQuery, text: str, reply_markup):
    await callback.message.edit_text(text, reply_markup=reply_markup)
