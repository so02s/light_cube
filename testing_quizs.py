from db_handler import db
import asyncio, datetime

async def add_testing_quizs():
    # Квиз по общим знаниям
    await db.add_quiz('Общие знания')
    quiz1 = await db.get_quiz('Общие знания')
    
    quest_1_1 = await db.add_question('Какой самый большой океан на Земле?', quiz1.id, time=30)
    await db.add_answ('Атлантический', quest_1_1, col='#FF6347', is_correct=False) 
    await db.add_answ('Индийский', quest_1_1,  col='#FF6347', is_correct=False)
    await db.add_answ('Тихий', quest_1_1,  col='#32CD32', is_correct=True)
    await db.add_answ('Северный Ледовитый', quest_1_1, col='#FF6347', is_correct=False) 
    
    quest_1_2 = await db.add_question('Кто написал роман "Война и мир"?', quiz1.id, time=30)
    await db.add_answ('Антон Чехов', quest_1_2,  col='#FF6347', is_correct=False)
    await db.add_answ('Лев Толстой', quest_1_2,  col='#32CD32', is_correct=True)
    await db.add_answ('Фёдор Достоевский', quest_1_2,  col='#FF6347', is_correct=False)
    await db.add_answ('Александр Пушкин', quest_1_2,  col='#FF6347', is_correct=False)
    
    quest_1_3 = await db.add_question('Какой элемент имеет химический символ "O"?', quiz1.id, time=30)
    await db.add_answ('Золото', quest_1_3,  col='#FF6347', is_correct=False)
    await db.add_answ('Углерод', quest_1_3,  col='#FF6347', is_correct=False)
    await db.add_answ('Кислород', quest_1_3,  col='#32CD32', is_correct=True)
    await db.add_answ('Азот', quest_1_3,  col='#FF6347', is_correct=False)

    quest_1_4 = await db.add_question('Столица Франции?', quiz1.id, time=30)
    await db.add_answ('Берлин', quest_1_4,  col='#FF6347', is_correct=False)
    await db.add_answ('Мадрид', quest_1_4,  col='#FF6347', is_correct=False)
    await db.add_answ('Париж', quest_1_4, col='#32CD32', is_correct=True)
    await db.add_answ('Рим', quest_1_4,  col='#FF6347', is_correct=False)

    quest_1_5 = await db.add_question('Какой год считается годом окончания Второй мировой войны?', quiz1.id, time=30)
    await db.add_answ('1945', quest_1_5,  col='#32CD32', is_correct=True)
    await db.add_answ('1946', quest_1_5,  col='#FF6347', is_correct=False)
    await db.add_answ('1944', quest_1_5,  col='#FF6347', is_correct=False)
    await db.add_answ('1939', quest_1_5,  col='#FF6347', is_correct=False)
    
    
    # Квиз по программированию
    await db.add_quiz('Программирование', "24.10.2024 19:55")
    quiz2 = await db.get_quiz('Программирование')

    quest_2_1 = await db.add_question('Какой язык программирования используется для веб-разработки, выполняемый на стороне клиента?', quiz2.id, time=30)
    # await db.add_answ(col='#32CD32', 'JavaScript', 1, quest_2_1)
    # await db.add_answ(col='#FF6347', 'Python', 0, quest_2_1)
    # await db.add_answ(col='#FF6347', 'Java', 0, quest_2_1)
    # await db.add_answ(col='#FF6347', 'C#', 0, quest_2_1)

    quest_2_2 = await db.add_question('Что такое ООП?', quiz2.id, time=30)
    # await db.add_answ(col='#32CD32', 'Объектно-Ориентированное Программирование', 1, quest_2_2)
    # await db.add_answ(col='#FF6347', 'Объектно-Операционное Программирование', 0, quest_2_2)
    # await db.add_answ(col='#FF6347', 'Операционное Программирование', 0, quest_2_2)
    # await db.add_answ(col='#FF6347', 'Общее Программирование', 0, quest_2_2)

    quest_2_3 = await db.add_question('Какой из следующих языков является компилируемым?', quiz2.id, time=30)
    # await db.add_answ(col='#FF6347', 'Python', 0, quest_2_3)
    # await db.add_answ(col='#32CD32', 'C++', 1, quest_2_3)
    # await db.add_answ(col='#FF6347', 'JavaScript', 0, quest_2_3)
    # await db.add_answ(col='#FF6347', 'Ruby', 0, quest_2_3)

    quest_2_4 = await db.add_question('Что такое Git?', quiz2.id, time=30)
    # await db.add_answ(col='#FF6347', 'Язык программирования', 0, quest_2_4)
    # await db.add_answ(col='#32CD32', 'Система контроля версий', 1, quest_2_4)
    # await db.add_answ(col='#FF6347', 'Текстовый редактор', 0, quest_2_4)
    # await db.add_answ(col='#FF6347', 'Фреймворк', 0, quest_2_4)

    quest_2_5 = await db.add_question('Какой метод используется для добавления элемента в конец списка в Python?', quiz2.id, time=30)
    # await db.add_answ(col='#32CD32', 'append()', 1, quest_2_5)
    # await db.add_answ(col='#FF6347', 'add()', 0, quest_2_5)
    # await db.add_answ(col='#FF6347', 'insert()', 0, quest_2_5)
    # await db.add_answ(col='#FF6347', 'extend()', 0, quest_2_5)
    

async def main():
    await db.add_moder('SpicySad')
    connected_at = datetime.datetime.now()
    await db.add_user_to_cube(120, 'SpicySad', 1339384726, connected_at)
    await add_testing_quizs()

if __name__ == "__main__":
    asyncio.run(main())