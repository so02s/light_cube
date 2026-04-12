import asyncio
from src.di import Container

async def main():
    container = Container()
    container.config.from_ini("config.ini")

    server = container.socket_server()

    mqtt = container.light_output_adapter()
    await mqtt.connect()
    await server.start()
    try:
        await asyncio.Event().wait()
    finally:
        await server.stop()
        await mqtt.disconnect()

if __name__ == "__main__":
    asyncio.run(main())