import asyncio
from create_bot import bot, dp, admins, db_manager, client
from handlers.start import start_router
from handlers.admin_handler import admin_router
from aiogram.types import BotCommand, BotCommandScopeDefault
from sqlalchemy import Integer, String, BigInteger, TIMESTAMP
from concurrent.futures import ThreadPoolExecutor

import asyncio_mqtt as aiomqtt

async def set_commands():
    commands = [BotCommand(command='start', description='Старт'), 
                BotCommand(command='on', description='Включить свет'),
                BotCommand(command='off', description='Выключить свет'),
                BotCommand(command='random', description='Поменять на рандомный цвет')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def start_bot():
    await set_commands()
    # count_users = await get_all_users(count=True)
    try:
        for admin_id in admins:
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
    dp.include_router(start_router)
    dp.include_router(admin_router)
    
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    
    # loop = SelectorEventLoop()
    # executor = ThreadPoolExecutor()
    
    # await loop.run_in_executor(executor, client.connect, "127.0.0.1")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())