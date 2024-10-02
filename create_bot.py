import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config
from asyncpg_lite import DatabaseManager
import paho.mqtt.client as mqtt

# получение админов
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

# логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MQTT
client = mqtt.Client()
client.connect("127.0.0.1", 1883)

# взаимодействие с бд
db_manager = DatabaseManager(db_url=config('PG_LINK'), deletion_password=config('ROOT_PASS'))

# инициализация бота
bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()