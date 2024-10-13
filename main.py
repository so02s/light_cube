# TODO midlware во время квиза - нельзя ничего менять

import asyncio
import logging

from aiogram.types import BotCommandScopeChat
from create_bot import bot, dp
from handlers import start, admin_handler, moder_handler
from keyboards import all_keyboards as kb
from utils.filter import refresh_moders, refresh_admins

# from middleware import DbSessionMiddleware

from decouple import config


# Старт переписать? 

async def start_bot():
    # try:
    #     for admin in admins:
    #         await bot.set_my_commands(kb.commands_admin(), BotCommandScopeChat(chat_id=admin))
    #         await bot.send_message(admin, f'Я запущен🥳.')
    # except:
        pass

async def stop_bot():
    # try:
    #     for admin in admins:
    #         await bot.send_message(admin, 'Бот остановлен. За что?😔')
    # except:
        pass


async def main():
    await refresh_moders()
    await refresh_admins()
    
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