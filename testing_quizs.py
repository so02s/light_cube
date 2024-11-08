from db_handler import db
import asyncio, datetime
async def add_testing_quizs():
    # Квиз по общим знаниям
    await db.add_quiz('Общие знания')
    quiz1 = await db.get_quiz('Общие знания')
    
    quest_1_1 = await db.add_question('Какой самый большой океан на Земле?', quiz1.id, time=10)
    await db.add_answ('Атлантический', quest_1_1, is_correct=False, col='#FF7400') 
    await db.add_answ('Индийский', quest_1_1, is_correct=False, col='#00FFFF')
    await db.add_answ('Тихий', quest_1_1, is_correct=True, col='#00FF7F')
    await db.add_answ('Северный Ледовитый', quest_1_1, is_correct=False, col='#9315F6') 
    
    quest_1_2 = await db.add_question('Кто написал роман "Война и мир"?', quiz1.id, time=10)
    await db.add_answ('Антон Чехов', quest_1_2, is_correct=False, col='#00FFFF')
    await db.add_answ('Лев Толстой', quest_1_2, is_correct=True, col='#00FF7F')
    await db.add_answ('Фёдор Достоевский', quest_1_2, is_correct=False, col='#FF7400')
    await db.add_answ('Александр Пушкин', quest_1_2, is_correct=False, col='#9315F6')
    
    quest_1_3 = await db.add_question('Какой элемент имеет химический символ "O"?', quiz1.id, time=10)
    await db.add_answ('Золото', quest_1_3, is_correct=False, col='#FF7400')
    await db.add_answ('Углерод', quest_1_3, is_correct=False, col='#00FFFF')
    await db.add_answ('Кислород', quest_1_3, is_correct=True, col='#00FF7F')
    await db.add_answ('Азот', quest_1_3, is_correct=False, col='#9315F6')

    quest_1_4 = await db.add_question('Столица Франции?', quiz1.id, time=10)
    await db.add_answ('Берлин', quest_1_4, is_correct=False, col='#FF7400')
    await db.add_answ('Мадрид', quest_1_4, is_correct=False, col='#00FFFF')
    await db.add_answ('Париж', quest_1_4, is_correct=True, col='#00FF7F')
    await db.add_answ('Рим', quest_1_4, is_correct=False, col='#9315F6')

    quest_1_5 = await db.add_question('Какой год считается годом окончания Второй мировой войны?', quiz1.id, time=10)
    await db.add_answ('1945', quest_1_5, is_correct=True, col='#00FF7F')
    await db.add_answ('1946', quest_1_5, is_correct=False, col='#FF7400')
    await db.add_answ('1944', quest_1_5, is_correct=False, col='#00FFFF')
    await db.add_answ('1939', quest_1_5, is_correct=False, col='#9315F6')
    
    
    
    # Квиз по программированию
    await db.add_quiz('Программирование', "24.10.2024 19:55")
    quiz2 = await db.get_quiz('Программирование')

    quest_2_1 = await db.add_question('Какой язык программирования используется для веб-разработки, выполняемый на стороне клиента?', quiz2.id, time=10)
    await db.add_answ('JavaScript', quest_2_1, is_correct=True, col='#00FF7F')
    await db.add_answ('Python', quest_2_1, is_correct=False, col='#FF7400')
    await db.add_answ('Java', quest_2_1, is_correct=False, col='#00FFFF')
    await db.add_answ('C#', quest_2_1, is_correct=False, col='#9315F6')

    quest_2_2 = await db.add_question('Что такое ООП?', quiz2.id, time=10)
    await db.add_answ('Объектно-Ориентированное Программирование', quest_2_2, is_correct=True, col='#00FF7F')
    await db.add_answ('Объектно-Операционное Программирование', quest_2_2, is_correct=False, col='#FF7400')
    await db.add_answ('Операционное Программирование', quest_2_2, is_correct=False, col='#00FFFF')
    await db.add_answ('Общее Программирование', quest_2_2, is_correct=False, col='#9315F6')

    quest_2_3 = await db.add_question('Какой из следующих языков является компилируемым?', quiz2.id, time=10)
    await db.add_answ('Python', quest_2_3, is_correct=False, col='#FF7400')
    await db.add_answ('C++', quest_2_3, is_correct=True, col='#00FF7F')
    await db.add_answ('JavaScript', quest_2_3, is_correct=False, col='#00FFFF')
    await db.add_answ('Ruby', quest_2_3, is_correct=False, col='#9315F6')

    quest_2_4 = await db.add_question('Что такое Git?', quiz2.id, time=10)
    await db.add_answ('Язык программирования', quest_2_4, is_correct=False, col='#FF7400')
    await db.add_answ('Система контроля версий', quest_2_4, is_correct=True, col='#00FF7F')
    await db.add_answ('Текстовый редактор', quest_2_4, is_correct=False, col='#00FFFF')
    await db.add_answ('Фреймворк', quest_2_4, is_correct=False, col='#9315F6')

    quest_2_5 = await db.add_question('Какой метод используется для добавления элемента в конец списка в Python?', quiz2.id, time=10)
    await db.add_answ('append()', quest_2_5, is_correct=True, col='#00FF7F')
    await db.add_answ('add()', quest_2_5, is_correct=False, col='#FF7400')
    await db.add_answ('insert()', quest_2_5, is_correct=False, col='#00FFFF')
    await db.add_answ('extend()', quest_2_5, is_correct=False, col='#9315F6')
    

async def main():
    await db.add_cubes()
    await db.add_moder('SpicySad')
    connected_at = datetime.datetime.now()
    await db.add_user_to_cube(120, 'SpicySad', 1339384726, connected_at)
    await add_testing_quizs()

if __name__ == "__main__":
    asyncio.run(main())