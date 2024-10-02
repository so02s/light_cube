from sqlalchemy import Integer, String, BigInteger, TIMESTAMP
from create_bot import db_manager
import asyncio

async def create_table_users(table_name='users_reg'):
    async with db_manager as client:
        columns = [
            {"name": "user_id", "type": BigInteger, "options": {"primary_key": True, "autoincrement": False}},
            {"name": "full_name", "type": String},
            {"name": "user_login", "type": String},
            {"name": "refer_id", "type": BigInteger},
            {"name": "count_refer", "type": Integer, "options": {"default": 0, "server_default": 0}},
            {"name": "date_reg", "type": TIMESTAMP},
        ]
        await client.create_table(table_name=table_name, columns=columns)

async def create_table_quiz(table_name='quiz'):
    async with pg_manager:
        columns = ['id_quiz INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL',
                   'quiz_name TEXT NOT NULL',
                   'num_corrections INTEGER NOT NULL DEFAULT 0',
                   'time_start TEXT']
        await pg_manager.create_table(table_name=table_name, columns=columns)

async def create_table_question(table_name='question'):
    async with pg_manager:
        columns = ['id_question INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL',
                   'text TEXT NOT NULL',
                   'correct_answer INTEGER',
                   'time_for_answer INTEGER',
                   'quiz_id INTEGER',
                   'FOREIGN KEY (quiz_id) REFERENCES quiz(id_quiz)',
                   'FOREIGN KEY (correct_answer) REFERENCES answer(id_answer)']
        await pg_manager.create_table(table_name=table_name, columns=columns)

async def create_table_answer(table_name='answer'):
    async with pg_manager:
        columns = ['id_answer INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL',
                   'text TEXT NOT NULL',
                   'id_question INTEGER NOT NULL',
                   'FOREIGN KEY(id_question) REFERENCES question(id_question)']
        await pg_manager.create_table(table_name=table_name, columns=columns)

async def create_table_user(table_name='user'):
    async with pg_manager:
        columns = ['id_user INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL',
                   'text TEXT NOT NULL',
                   'num_attempts INTEGER NOT NULL DEFAULT 0']
        await pg_manager.create_table(table_name=table_name, columns=columns)

async def create_table_cube(table_name='cube'):
    async with pg_manager:
        columns = ['id_cube INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL',
                   'id_user INTEGER NOT NULL',
                   'status INTEGER',
                   'FOREIGN KEY(id_user) REFERENCES user(id_user)']
        await pg_manager.create_table(table_name=table_name, columns=columns)

async def create_table_attempt(table_name='attempt'):
    async with pg_manager:
        columns = ['id_attempt INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL',
                   'id_user INTEGER NOT NULL',
                   'result INTEGER NOT NULL',
                   'FOREIGN KEY(id_user) REFERENCES user(id_user)']
        await pg_manager.create_table(table_name=table_name, columns=columns)

async def create_table_testing(table_name='testing'):
    async with pg_manager:
        columns = ['id_testing INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL',
                   'id_question INTEGER NOT NULL',
                   'id_answer INTEGER NOT NULL',
                   'id_attempt INTEGER NOT NULL',
                   'FOREIGN KEY(id_attempt) REFERENCES attempt(id_attempt)',
                   'FOREIGN KEY(id_question) REFERENCES question(id_question)',
                   'FOREIGN KEY(id_answer) REFERENCES answer(id_answer)']
        await pg_manager.create_table(table_name=table_name, columns=columns)

async def get_user_data(user_id: int, table_name='users_reg'):
    async with pg_manager:
        user_info = await pg_manager.select_data(table_name=table_name, where_dict={'user_id': user_id}, one_dict=True)
        if user_info:
            return user_info
        else:
            return None
        
async def register_user(user_data: dict, table_name='user'):
    async with pg_manager:
        await pg_manager.insert_data(table_name=table_name, records_data=user_data)