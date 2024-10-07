from create_bot import admins
import aiomqtt

async def wled_publish(topic, msg):
    async with aiomqtt.Client("localhost") as client:
        await client.publish("wled/" + topic, payload=msg)