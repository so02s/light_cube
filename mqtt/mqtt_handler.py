from create_bot import client

async def publish(topic, msg):
    await client.publish(topic, payload=msg)