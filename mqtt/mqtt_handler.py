import aiomqtt
from data.config import MQTT_HOST

async def wled_publish(topic, msg):
    async with aiomqtt.Client(MQTT_HOST) as client:
        await client.publish("wled/" + topic, payload=msg)