from decouple import config

# получение админов, модеров
# TODO : подкачка не через конфиги, а через бд 
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]
moders = [int(moders_id) for moders_id in config('MODERS').split(',')] + admins