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
                BotCommand(command='deep_link', description='Создать реферальную ссылку для кубов'),
                BotCommand(command='deep_link_program', description='Создать реферальную ссылку для программы мероприятия'),
                BotCommand(command='all_moder', description='Все модераторы'),
                BotCommand(command='add_moder', description='Добавить модератора'),
                BotCommand(command='del_moder', description='Удалить модератора'),
                BotCommand(command='cancel', description='Отмена действия')
            ]

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
                BotCommand(command='user', description='Режим юзера'),
                BotCommand(command='cancel', description='Отмена действия')
            ]

def commands_change_quiz():
    return [
                BotCommand(command='cancel', description='Выход из изменения квиза'),
                BotCommand(command='help', description='Помощь'),
                BotCommand(command='all_info', description='Информация о квизе'),
                BotCommand(command='add_question', description='Добавить вопрос'), 
                BotCommand(command='del_question', description='Удалить вопрос'),
                BotCommand(command='change_question', description='Изменить вопрос'),
                BotCommand(command='change_start_time', description='Изменить время начала квиза')
            ]
    
def commands_change_question():
    return [
                BotCommand(command='cancel', description='Выход из изменения вопроса'),
                BotCommand(command='help', description='Помощь'),
                BotCommand(command='question_info', description='Вывод информации о вопросе'),
                BotCommand(command='change_time', description='Изменить время на вопрос'),
                BotCommand(command='add_answer', description='Добавить ответ к вопросу'),
                BotCommand(command='del_answer', description='Удалить ответ с подтверждением'),
                BotCommand(command='change_answer', description='Изменить ответ на вопрос')
            ]

def commands_change_answer():
    return [
                BotCommand(command='cancel', description='Выход из изменения ответа'),
                BotCommand(command='help', description='Помощь'),
                BotCommand(command='answer_info', description='Вывод информации о ответе'),
                BotCommand(command='change_correctness', description='Изменить правильность ответа'),
                BotCommand(command='change_text', description='Изменить текст ответа'),
                BotCommand(command='change_color', description='Изменить цвет ответа')
            ]

def commands_user():
    return [BotCommand(command='start', description='Старт')]