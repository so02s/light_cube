import asyncio, datetime
from create_bot import bot, dp
from handlers import start, admin_handler, moder_handler, change_quiz_handler, quiz_handler
from utils.filter import refresh_moders, refresh_admins
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db_handler.db import get_quizs
from handlers.quiz_handler import start_quiz

scheduler = AsyncIOScheduler()

async def schedule_quizzes():
    quizzes = await get_quizs()
    formatted_time = datetime.datetime.strptime('01.01.2026 00:00', '%d.%m.%Y %H:%M')
    for quiz in quizzes:
        if quiz.start_datetime != formatted_time:
            scheduler.add_job(
                start_quiz,
                'date',
                run_date=quiz.start_datetime,
                args=[quiz]
            )

async def start_bot():
    await schedule_quizzes()
    scheduler.start()

async def stop_bot():
    scheduler.shutdown()


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