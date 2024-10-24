from aiogram.types import CallbackQuery

async def inline_kb(callback: CallbackQuery, text: str, kb):
    await callback.message.edit_text(text, reply_markup=kb)