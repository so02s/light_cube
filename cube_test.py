import asyncio
import mqtt.mqtt_handler as mqtt

async def main():
    
    await mqtt.wled_publish('cubes/col', '#2f0bb3')
    
    await asyncio.sleep(5)
    
    for i in range(1, 121):
        await asyncio.sleep(0.5)
        await mqtt.cube_publish_by_id(i, '/col', '#fc0a3f')

if __name__ == "__main__":
    asyncio.run(main())