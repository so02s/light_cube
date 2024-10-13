import aiomqtt
from decouple import config

async def wled_publish(topic, msg):
    async with aiomqtt.Client(config('MQTT_HOST')) as client:
        await client.publish("wled/" + topic, payload=msg)


# Управление кубами

async def cube_on():
    async with aiomqtt.Client(config('MQTT_HOST')) as client:
        await client.publish("wled/cubes", payload='ON')

async def cube_off():
    async with aiomqtt.Client(config('MQTT_HOST')) as client:
        await client.publish("wled/cubes", payload='OFF')

async def cube_publish_by_id(id, msg):
    async with aiomqtt.Client(config('MQTT_HOST')) as client:
        await client.publish("wled/cube_" + str(id), payload=msg)