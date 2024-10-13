from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import BotCommand, BotCommandScopeDefault

def commands_admin():
    return [
                BotCommand(command='start', description='Старт'), 
                BotCommand(command='on', description='Включить свет'),
                BotCommand(command='off', description='Выключить свет'),
                BotCommand(command='random', description='Поменять на рандомный цвет'),
                BotCommand(command='deep_link', description='Создать реферальную ссылку'),
                BotCommand(command='all_moder', description='Все модераторы'),
                BotCommand(command='add_moder', description='Добавить модератора'),
                BotCommand(command='del_moder', description='Удалить модератора'),
                BotCommand(command='moder', description='Режим модератора'),
                BotCommand(command='user', description='Режим юзера')]

def commands_moder():
    return [
                BotCommand(command='start', description='Старт'), 
                BotCommand(command='all_quiz', description='Вывести все квизы'),
                BotCommand(command='start_quiz', description='Начать квиз'),
                BotCommand(command='add_quiz', description='Добавить квиз'),
                BotCommand(command='del_quiz', description='Удалить квиз'),
                BotCommand(command='change_quiz', description='Изменить квиз'),
                BotCommand(command='user', description='Режим юзера')]

def commands_change_quiz():
    return [
                BotCommand(command='cancel', description='Выход из изменения квиза'),
                BotCommand(command='add_question', description='Добавить вопрос'), 
                BotCommand(command='del_question', description='Удалить вопрос'),
                BotCommand(command='change_question', description='Изменить вопрос'),
                BotCommand(command='change_start_time', description='Изменить время начала квиза')]
    
def commands_user():
    return [BotCommand(command='start', description='Старт')]