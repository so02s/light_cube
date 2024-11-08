import aiomqtt

from decouple import config

async def wled_publish(topic: str, msg: str):
    print("publish to", topic, ", payload:", msg)
    async with aiomqtt.Client(config('MQTT_HOST')) as client:
        await client.publish("wled/" + topic, payload=msg, qos=1)


# Управление кубами

async def cube_on():
    async with aiomqtt.Client(config('MQTT_HOST')) as client:
        await client.publish("wled/cubes", payload='ON', qos=1)

async def cube_off():
    async with aiomqtt.Client(config('MQTT_HOST')) as client:
        await client.publish("wled/cubes", payload='OFF', qos=1)

async def cube_publish_by_id(id: int, theme: str, msg: str):
    print("publish to", "wled/cube_" + str(id) + theme, ", payload:", msg)
    async with aiomqtt.Client(config('MQTT_HOST')) as client:
        await client.publish("wled/cube_" + str(id) + theme, payload=msg, qos=1)
