from decouple import config
from db_handler.db import get_moders
import re

admins_username = []
moders_username = []

async def refresh_moders() -> None:
    global moders_username
    try:
        moders_username = await get_moders()
    except Exception as e:
        print(f"Error: {e}")

# TODO : подкачка не через конфиги, а через бд 
async def refresh_admins() -> None:
    global admins_username
    try:
        admins_username = []
    except Exception as e:
        print(f"Error: {e}")

def moders() -> list:
    global moders_username
    return moders_username

def admins() -> list:
    global admins_username
    return admins_username
