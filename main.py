import asyncio

from create_bot import bot, dp
from db_handler.models import create_all_tables
from handlers import (
    start,
    cube_control,
    quiz_control,
    change_quiz,
    change_question,
    change_answer,
    quiz_handler,
    admin,
)
from handlers.scheduler_handler import schedule_quizzes, start_scheduler
from utils.filter import refresh_moders, refresh_admins
from mqtt.mqtt_handler import wled_publish


async def start_bot():
    start_scheduler()
    await schedule_quizzes()
    # await wled_publish('cubes/api', f'{{"bri": {200}}}')

async def stop_bot():
    pass


async def main():
    # Создание всех таблиц
    await create_all_tables()
    
    # Обновление модеров и админов (из бд в оперативу)
    await refresh_admins()
    await refresh_moders()
    
    # Подключение хендлеров
    dp.include_routers(
        admin.router,
        start.router,
        cube_control.router,
        quiz_control.router,
        change_quiz.router,
        change_question.router,
        change_answer.router,
        quiz_handler.router
    )
    
    # Подключение функций на включении бота и выключении
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Начало работы
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())