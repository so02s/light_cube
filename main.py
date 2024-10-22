import asyncio
from create_bot import bot, dp
from handlers import start, admin_handler, moder_handler, change_quiz_handler, quiz_handler
from utils.filter import refresh_moders, refresh_admins

async def start_bot():
    pass

async def stop_bot():
    pass


async def main():
    await refresh_moders()
    await refresh_admins()
    
    dp.include_routers(start.router,
                       admin_handler.router,
                       moder_handler.router,
                       change_quiz_handler.router,
                       quiz_handler.router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
    
#TODO старт квизов по времени - нужно разобраться как