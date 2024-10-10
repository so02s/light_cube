import configparser

read_config = configparser.ConfigParser()
read_config.read('settings.ini')
try:
    BOT_TOKEN = read_config['settings']['TOKEN'].strip()
    DB_DB = read_config['settings']['db'].strip()
    DB_HOST = read_config['settings']['host'].strip()
    DB_USER = read_config['settings']['user'].strip()
    DB_PASS = read_config['settings']['password'].strip()
    MQTT_HOST = read_config['settings']['mqtt_host'].strip()
    if DB_DB and DB_HOST and DB_USER and DB_PASS and BOT_TOKEN:
        DB_PATH = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_DB}"
    else:
        raise Exception
    
except Exception as ex:
    cancel('Переменные не найдены в файле "settings.ini".')
    
    
def get_admins():
    read_admins = configparser.ConfigParser()
    read_admins.read('settings.ini')
    
    try:
        admins = read_admins['settings']['ADMINS'].strip()
        admins = admins.replace(' ', '').split(',')
        admins = list(map(int, admins))
        return admins
    except:
        print('Админ(ы) не указан(ы)')
        
def get_moders():
    read_moders = configparser.ConfigParser()
    read_moders.read('settings.ini')
    
    try:
        moders = read_moders['settings']['MODERS'].strip()
        moders = moders.replace(' ', '').split(',')
        moders = list(map(int, moders))
        return moders
    except:
        print('Модератор(ы) не указан(ы)')