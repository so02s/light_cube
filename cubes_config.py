import asyncio
import mqtt.mqtt_handler as mqtt

# Настройка пресета "победа"

async def preset_color(color, i):
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

if __name__ == "__main__":
    asyncio.run(main())