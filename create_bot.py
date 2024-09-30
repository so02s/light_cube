import logging
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config
from db_handler.db_class import PostgresHandler
import paho.mqtt.client as mqtt

# получение админов
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

# логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MQTT
client = mqtt.Client()
client.connect("192.168.87.9", 1883)

# взаимодействие с бд
pg_db = PostgresHandler(dsn=config('PG_LINK'), deletion_password=config('ROOT_PASS'))

# инициализация бота
bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()