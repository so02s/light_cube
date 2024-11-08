import logging

from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


# логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename="/home/so02s/light_cube/logs.log",filemode="w")
logger=logging.getLogger(__name__)

# взаимодействие с бд
DATABASE_URL = f"postgresql+asyncpg://{config('DB_USER')}:{config('DB_PASS')}@{config('DB_HOST')}/{config('DB_NAME')}"
engine = create_async_engine(url=DATABASE_URL, echo=True)
Session = async_sessionmaker(engine, expire_on_commit=False)

# инициализация бота
bot = Bot(token=config('TOKEN_BOT'), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) 
dp = Dispatcher()