import asyncio
import aiomqtt
from decouple import config
import random

async def wled_publish(topic: str, msg: str):
    print("publish to", topic, ", payload:", msg)
    async with aiomqtt.Client(config('MQTT_HOST')) as client:
        await client.publish("wled/" + topic, payload=msg, qos=1)

async def set_color(color):
    payload_color = f'''{{
        "seg":
        [
            {{
            "col": [{color}]
            }}
        ]
    }}'''
    await wled_publish("cubes/api", payload_color)
    await asyncio.sleep(2)
    save_payload = f'{{"psave": 1}}'
    await wled_publish("cubes/api", save_payload)

async def main():
    colors = [
        '[68,235,153]',
        '[134,27,227]',
        '[54,197,240]',
        '[26,83,188]'
    ]
    
    for i in range(len(colors)):
        color = random.choice(colors)
        colors.remove(color)
        await set_color(color)

if __name__ == "__main__":
    asyncio.run(main())