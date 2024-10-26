from db_handler import db
import asyncio

async def add_testing_quizs():
    # Квиз по общим знаниям
    await db.add_quiz('Общие знания')
    quiz1 = await db.get_quiz('Общие знания')
    
    quest_1_1 = await db.add_question('0:30', 'Какой самый большой океан на Земле?', quiz1)
    await db.add_answ('#FF6347', 'Атлантический', 0, quest_1_1)
    await db.add_answ('#FF6347', 'Индийский', 0, quest_1_1)
    await db.add_answ('#32CD32', 'Тихий', 1, quest_1_1)
    await db.add_answ('#FF6347', 'Северный Ледовитый', 0, quest_1_1)
    
    quest_1_2 = await db.add_question('0:30', 'Кто написал роман "Война и мир"?', quiz1)
    await db.add_answ('#FF6347', 'Антон Чехов', 0, quest_1_2)
    await db.add_answ('#32CD32', 'Лев Толстой', 1, quest_1_2)
    await db.add_answ('#FF6347', 'Фёдор Достоевский', 0, quest_1_2)
    await db.add_answ('#FF6347', 'Александр Пушкин', 0, quest_1_2)
    
    quest_1_3 = await db.add_question('0:30', 'Какой элемент имеет химический символ "O"?', quiz1)
    await db.add_answ('#FF6347', 'Золото', 0, quest_1_3)
    await db.add_answ('#FF6347', 'Углерод', 0, quest_1_3)
    await db.add_answ('#32CD32', 'Кислород', 1, quest_1_3)
    await db.add_answ('#FF6347', 'Азот', 0, quest_1_3)

    quest_1_4 = await db.add_question('0:30', 'Столица Франции?', quiz1)
    await db.add_answ('#FF6347', 'Берлин', 0, quest_1_4)
    await db.add_answ('#FF6347', 'Мадрид', 0, quest_1_4)
    await db.add_answ('#32CD32', 'Париж', 1, quest_1_4)
    await db.add_answ('#FF6347', 'Рим', 0, quest_1_4)

    quest_1_5 = await db.add_question('0:30', 'Какой год считается годом окончания Второй мировой войны?', quiz1)
    await db.add_answ('#32CD32', '1945', 1, quest_1_5)
    await db.add_answ('#FF6347', '1946', 0, quest_1_5)
    await db.add_answ('#FF6347', '1944', 0, quest_1_5)
    await db.add_answ('#FF6347', '1939', 0, quest_1_5)
    
    
    # Квиз по программированию
    await db.add_quiz('Программирование', "24.10.2024 19:55")
    quiz2 = await db.get_quiz('Программирование')

    quest_2_1 = await db.add_question('0:30', 'Какой язык программирования используется для веб-разработки, выполняемый на стороне клиента?', quiz2)
    await db.add_answ('#32CD32', 'JavaScript', 1, quest_2_1)
    await db.add_answ('#FF6347', 'Python', 0, quest_2_1)
    await db.add_answ('#FF6347', 'Java', 0, quest_2_1)
    await db.add_answ('#FF6347', 'C#', 0, quest_2_1)

    quest_2_2 = await db.add_question('0:30', 'Что такое ООП?', quiz2)
    await db.add_answ('#32CD32', 'Объектно-Ориентированное Программирование', 1, quest_2_2)
    await db.add_answ('#FF6347', 'Объектно-Операционное Программирование', 0, quest_2_2)
    await db.add_answ('#FF6347', 'Операционное Программирование', 0, quest_2_2)
    await db.add_answ('#FF6347', 'Общее Программирование', 0, quest_2_2)

    quest_2_3 = await db.add_question('0:30', 'Какой из следующих языков является компилируемым?', quiz2)
    await db.add_answ('#FF6347', 'Python', 0, quest_2_3)
    await db.add_answ('#32CD32', 'C++', 1, quest_2_3)
    await db.add_answ('#FF6347', 'JavaScript', 0, quest_2_3)
    await db.add_answ('#FF6347', 'Ruby', 0, quest_2_3)

    quest_2_4 = await db.add_question('0:30', 'Что такое Git?', quiz2)
    await db.add_answ('#FF6347', 'Язык программирования', 0, quest_2_4)
    await db.add_answ('#32CD32', 'Система контроля версий', 1, quest_2_4)
    await db.add_answ('#FF6347', 'Текстовый редактор', 0, quest_2_4)
    await db.add_answ('#FF6347', 'Фреймворк', 0, quest_2_4)

    quest_2_5 = await db.add_question('0:30', 'Какой метод используется для добавления элемента в конец списка в Python?', quiz2)
    await db.add_answ('#32CD32', 'append()', 1, quest_2_5)
    await db.add_answ('#FF6347', 'add()', 0, quest_2_5)
    await db.add_answ('#FF6347', 'insert()', 0, quest_2_5)
    await db.add_answ('#FF6347', 'extend()', 0, quest_2_5)
    

async def main():
    # await db.add_moder('SpicySad')
    await add_testing_quizs()

if __name__ == "__main__":
    asyncio.run(main())