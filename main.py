import asyncio
from handlers.scheduler_handler import schedule_quizzes, start_scheduler
from utils.filter import refresh_moders, refresh_admins
from create_bot import bot, dp
from handlers import start, cube_control, quiz_control, change_quiz_handler, quiz_handler

async def start_bot():
    start_scheduler()
    await schedule_quizzes()

async def stop_bot():
    pass

async def main():
    await refresh_moders()
    await refresh_admins()
    
    dp.include_routers(
        start.router,
        cube_control.router,
        quiz_control.router,
        change_quiz_handler.router,
        quiz_handler.router
    )
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())