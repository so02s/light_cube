from aiogram.types import BotCommand

def commands_admin():
    return [
                BotCommand(command='start', description='Старт'),
                BotCommand(command='help', description='Помощь'),
                BotCommand(command='moder', description='Режим модератора'),
                BotCommand(command='user', description='Режим юзера'),
                BotCommand(command='on', description='Включить свет'),
                BotCommand(command='off', description='Выключить свет'),
                BotCommand(command='color', description='Установка цвета'),
                BotCommand(command='random', description='Поменять на рандомный цвет'),
                BotCommand(command='deep_link', description='Создать реферальную ссылку'),
                BotCommand(command='all_moder', description='Все модераторы'),
                BotCommand(command='add_moder', description='Добавить модератора'),
                BotCommand(command='del_moder', description='Удалить модератора')]

def commands_moder():
    return [
                BotCommand(command='start', description='Старт'), 
                BotCommand(command='help', description='Помощь'),
                BotCommand(command='change_program', description='Изменить сообщение о программе мероприятия. Еще не работает'),
                BotCommand(command='all_quiz', description='Вывести все квизы'),
                BotCommand(command='start_quiz', description='Начать квиз'),
                BotCommand(command='add_quiz', description='Добавить квиз'),
                BotCommand(command='del_quiz', description='Удалить квиз'),
                BotCommand(command='change_quiz', description='Изменить квиз'),
                BotCommand(command='user', description='Режим юзера')]

def commands_change_quiz():
    return [
                BotCommand(command='cancel', description='Выход из изменения квиза'),
                BotCommand(command='help_change_quiz', description='Помощь'),
                BotCommand(command='all_info', description='Информация о квизе'),
                BotCommand(command='add_question', description='Добавить вопрос'), 
                BotCommand(command='del_question', description='Удалить вопрос'),
                BotCommand(command='change_question', description='Изменить вопрос'),
                BotCommand(command='change_start_time', description='Изменить время начала квиза')]
    
def commands_user():
    return [BotCommand(command='start', description='Старт')]