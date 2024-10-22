from db_handler.db import get_moders
import re

admins_username = []
moders_username = []
users_id = []

async def refresh_moders() -> None:
    global moders_username
    try:
        moders_username = await get_moders()
    except Exception as e:
        print(f"Error: {e}")
        
async def refresh_admins() -> None:
    global admins_username
    try:
        admins_username = ['SpicySad']
    except Exception as e:
        print(f"Error: {e}")

def moders() -> list:
    global moders_username
    return moders_username

def admins() -> list:
    global admins_username
    return admins_username

def users_in_quiz() -> list:
    global users_id
    return users_id

is_moder = lambda msg: msg.from_user.username in moders()
is_admin = lambda msg: msg.from_user.username in admins()
is_admin_or_moder = lambda msg: msg.from_user.username in admins() + moders()
is_quiz_user = lambda msg: msg.from_user.id in users_in_quiz()