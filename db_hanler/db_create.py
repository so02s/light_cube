# from sqlalchemy import Table, Integer, String, MetaData, DateTime

# metadata_obj = MetaData()

# quiz_table = Table(
#     "quiz",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("quiz_name", String, nullable=True),
#     Column("num_corrections", Integer, nullable=True, default=1),
#     Column("time_start", DateTime),
# )

# async def create_table_quiz(table_name='quiz'):
#     async with db_manager as client:
#         columns = [
#             {"name": "id_quiz", "type": BigInteger, "options": {"primary_key": True, "autoincrement": True}},
#             {"name": "quiz_name", "type": String, "options": {"not_null": True}},
#             {"name": "num_corrections", "type": Integer, "options": {"not_null": True, "default": 0, "server_default": 0}},
#             {"name": "time_start", "type": String},
#         ]
#         await client.create_table(table_name=table_name, columns=columns)

# async def create_table_question(table_name='question'):
#     async with db_manager as client:
#         columns = [
#             {"name": "id_question", "type": BigInteger, "options": {"primary_key": True, "autoincrement": True}},
#             {"name": "text", "type": String, "options": {"not_null": True}},
#             {"name": "correct_answer", "type": Integer},
#             {"name": "time_for_answer", "type": Integer},
#             {"name": "quiz_id", "type": BigInteger},
#         ]
#         foreign_keys = [
#             {"columns": ["quiz_id"], "references": {"table": "quiz", "columns": ["id_quiz"]}},
#             {"columns": ["correct_answer"], "references": {"table": "answer", "columns": ["id_answer"]}},
#         ]
#         await client.create_table(table_name=table_name, columns=columns, foreign_keys=foreign_keys)

# async def create_table_answer(table_name='answer'):
#     async with db_manager as client:
#         columns = [
#             {"name": "id_answer", "type": BigInteger, "options": {"primary_key": True, "autoincrement": True}},
#             {"name": "text", "type": String, "options": {"not_null": True}},
#             {"name": "id_question", "type": BigInteger, "options": {"not_null": True}},
#         ]
#         foreign_keys = [
#             {"columns": ["id_question"], "references": {"table": "question", "columns": ["id_question"]}},
#         ]
#         await client.create_table(table_name=table_name, columns=columns, foreign_keys=foreign_keys)

# async def create_table_user(table_name='user'):
#     async with db_manager as client:
#         columns = [
#             {"name": "id_user", "type": BigInteger, "options": {"primary_key": True, "autoincrement": True}},
#             {"name": "text", "type": String, "options": {"not_null": True}},
#             {"name": "num_attempts", "type": Integer, "options": {"not_null": True, "default": 0, "server_default": 0}},
#         ]
#         await client.create_table(table_name=table_name, columns=columns)

# async def create_table_cube(table_name='cube'):
#     async with db_manager as client:
#         columns = [
#             {"name": "id_cube", "type": BigInteger, "options": {"primary_key": True, "autoincrement": True}},
#             {"name": "id_user", "type": BigInteger, "options": {"not_null": True}},
#             {"name": "status", "type": Integer},
#         ]
#         foreign_keys = [
#             {"columns": ["id_user"], "references": {"table": "user", "columns": ["id_user"]}},
#         ]
#         await client.create_table(table_name=table_name, columns=columns, foreign_keys=foreign_keys)

# async def create_table_attempt(table_name='attempt'):
#     async with db_manager as client:
#         columns = [
#             {"name": "id_attempt", "type": BigInteger, "options": {"primary_key": True, "autoincrement": True}},
#             {"name": "id_user", "type": BigInteger, "options": {"not_null": True}},
#             {"name": "result", "type": Integer, "options": {"not_null": True}},
#         ]
#         foreign_keys = [
#             {"columns": ["id_user"], "references": {"table": "user", "columns": ["id_user"]}},
#         ]
#         await client.create_table(table_name=table_name, columns=columns, foreign_keys=foreign_keys)

# async def create_table_testing(table_name='testing'):
#     async with db_manager as client:
#         columns = [
#             {"name": "id_testing", "type": BigInteger, "options": {"primary_key": True, "autoincrement": True}},
#             {"name": "id_question", "type": BigInteger, "options": {"not_null": True}},
#             {"name": "id_answer", "type": BigInteger, "options": {"not_null": True}},
#             {"name": "id_attempt", "type": BigInteger, "options": {"not_null": True}},
#         ]
#         foreign_keys = [
#             {"columns": ["id_attempt"], "references": {"table": "attempt", "columns": ["id_attempt"]}},
#             {"columns": ["id_question"], "references": {"table": "question", "columns": ["id_question"]}},
#             {"columns": ["id_answer"], "references": {"table": "answer", "columns": ["id_answer"]}},
#         ]
#         await client.create_table(table_name=table_name, columns=columns, foreign_keys=foreign_keys)

# async def get_user_data(user_id: int, table_name='users_reg'):
#     async with pg_manager:
#         user_info = await pg_manager.select_data(table_name=table_name, where_dict={'user_id': user_id}, one_dict=True)
#         if user_info:
#             return user_info
#         else:
#             return None
        
# async def register_user(user_data: dict, table_name='user'):
#     async with pg_manager:
#         await pg_manager.insert_data(table_name=table_name, records_data=user_data)
        
