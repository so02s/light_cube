import asyncio

from db_handler.models import create_all_tables

asyncio.run(create_all_tables())