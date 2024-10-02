import asyncio
from create_bot import bot, dp, admins
from handlers.start import start_router
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands():
    commands = [BotCommand(command='start', description='Старт')]
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
    # dp.include_router(admin_router)
    
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())