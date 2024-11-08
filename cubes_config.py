import asyncio
import mqtt.mqtt_handler as mqtt 
from utils.presets import win_color

async def preset_color(color, i):
    # payload_color = f'''{{"on": t,"bri": 200,"seg":[{{"col":{color} }}] }}'''
    payload_color = f'''{{
        "seg":
        [
            {{
            "col": [{color}]
            }}
        ]
    }}'''
    await mqtt.wled_publish("cubes/api", payload_color)
    await asyncio.sleep(2)
    save_payload = f'{{"psave": {i+1}}}'
    await mqtt.wled_publish("cubes/api", save_payload)


async def main():
    colors = [
        '[68,235,153]',
        '[134,27,227]',
        '[54,197,240]',
        '[26,83,188]'
    ]
    
    for i, color in enumerate(colors):
        await preset_color(color, i)
    # for i in range(1, 121):
    #     await mqtt.cube_publish_by_id(i, '/api', win_color())

if __name__ == "__main__":
    asyncio.run(main())