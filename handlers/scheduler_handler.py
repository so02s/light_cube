import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db_handler.db import get_quizs
from db_handler.models import Quiz
from handlers.quiz_handler import start_quiz


scheduler = AsyncIOScheduler()
formatted_time = datetime.datetime.strptime('01.01.2026 00:00', '%d.%m.%Y %H:%M')

async def schedule_quizzes():
    quizzes = await get_quizs()
    for quiz in quizzes:
        if quiz.start_datetime != formatted_time:
            scheduler.add_job(
                start_quiz,
                'date',
                run_date=quiz.start_datetime,
                args=[quiz],
                id=f"quiz_{quiz.id}"
            )

async def schedule_add_job(quiz: Quiz):
    if quiz.start_datetime != formatted_time:
        scheduler.add_job(
            start_quiz,
            'date',
            run_date=quiz.start_datetime,
            args=[quiz],
            id=f"quiz_{quiz.id}"
        )

async def schedule_del_job(quiz_id: int):
    job_id = f"quiz_{quiz_id}"
    job = scheduler.get_job(job_id)
    if job:
        scheduler.remove_job(job_id)

async def schedule_update_job(quiz_id: int):
    job_id = f"quiz_{quiz_id}"
    job = scheduler.get_job(job_id)
    if job:
        await schedule_del_job(job_id)
    await schedule_add_job(quiz)

def start_scheduler():
    scheduler.start()