import asyncio
from aiogram.types import BotCommandScopeChat

import aiomqtt

from create_bot import bot, dp, admins #, db_manager
from handlers.start import start_router
from handlers.admin_handler import admin_router
from handlers.moder_handler import moder_router
import keyboards.all_keyboards as kb

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
    dp.include_routers(start_router, admin_router, moder_router)
    
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())