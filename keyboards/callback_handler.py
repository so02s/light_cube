from aiogram.types import CallbackQuery
from typing import Optional
from aiogram.filters.callback_data import CallbackData

class QuizCallbackFactory(CallbackData, prefix="fabquiz"):
    quiz_id: int
    action: str

async def inline_kb(callback: CallbackQuery, payload, kb):
    await callback.message.edit_text(payload, reply_markup=kb)