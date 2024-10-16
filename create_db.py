from db_handler.models import create_all_tables
import asyncio

asyncio.run(create_all_tables())