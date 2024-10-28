import aiomqtt
from decouple import config

async def wled_publish(topic, msg):
    try:
        async with aiomqtt.Client(config('MQTT_HOST')) as client:
            await client.publish("wled/" + topic, payload=msg)
    except:
        print("Error: MQTT is not connected")

is_blinking = False

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

async def blink_cubes(speed: int, count: int = 121):
    global is_blinking
    is_blinking = True
    while is_blinking:
        for cube_id in range(1, count):
            await cube_publish_by_id(cube_id, 'ON')
        await asyncio.sleep(speed / 1000)
        
        for cube_id in range(1, count):
            await cube_publish_by_id(cube_id, 'OFF')
        await asyncio.sleep(speed / 1000)
