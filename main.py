# TODO midlware во время квиза - нельзя ничего менять

import asyncio
import logging

from aiogram.types import BotCommandScopeChat
from create_bot import bot, dp
from handlers import start, admin_handler, moder_handler
from keyboards import all_keyboards as kb

# from middleware import DbSessionMiddleware

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from decouple import config
from utils.filter import admins

async def start_bot():
    try:
        for admin_id in admins:
            await bot.set_my_commands(kb.commands_admin(), BotCommandScopeChat(chat_id=admin_id))
            await bot.send_message(admin_id, f'Я запущен🥳.')
    except:
        pass

async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except:
        pass


async def main():
    # engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True)
    # async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    dp.include_routers(start.router, admin_handler.router, moder_handler.router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    
    # dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())