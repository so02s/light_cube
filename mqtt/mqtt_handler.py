import aiomqtt
from decouple import config

async def wled_publish(topic, msg):
    async with aiomqtt.Client(config('MQTT_HOST')) as client:
        await client.publish("wled/" + topic, payload=msg)


# Управление кубами

async def cube_on():
    try:
        async with aiomqtt.Client(config('MQTT_HOST')) as client:
            await client.publish("wled/cubes", payload='ON')
    except:
        print("Error: MQTT is not connected")

async def cube_off():
    try:
        async with aiomqtt.Client(config('MQTT_HOST')) as client:
            await client.publish("wled/cubes", payload='OFF')
    except:
        print("Error: MQTT is not connected")

async def cube_publish_by_id(id, msg):
    try:
        async with aiomqtt.Client(config('MQTT_HOST')) as client:
            await client.publish("wled/cube_" + str(id), payload=msg)
    except:
        print("Error: MQTT is not connected")
        

async def blink_cubes():
    # TODO анимация медленного мигания на разных кубах (несколько рандомных групп)
    pass