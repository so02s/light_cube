from aiomqtt import Client
from src.domain import LightOutput, Cube, Color


class MQTTClient(LightOutput):
    def __init__(self, hostname: str, cube_topic: str):
        self._client = Client(hostname=hostname)
        self._cube_topic = cube_topic
        self._connected = False

    async def connect(self) -> None:
        await self._client.__aenter__()
        self._connected = True

    async def disconnect(self) -> None:
        if self._connected:
            await self._client.__aexit__(None, None, None)
            self._connected = False
    
    async def turn_on_all(self) -> None:
        await self._client.publish(self._cube_topic, payload="ON", qos=1)

    async def turn_off_all(self) -> None:
        await self._client.publish(self._cube_topic, payload="OFF", qos=1)

    async def set_color(self, cube: Cube, color: Color) -> None:
        topic = f"wled/cube_{cube.id}/col"
        await self._client.publish(topic, payload=color, qos=1)

    async def set_color_all(self, color: Color) -> None:
        topic = self._cube_topic + "/col"
        await self._client.publish(topic, payload=color, qos=1)

    async def set_command(self, cube: Cube, command: str) -> None:
        pass

    async def set_command_all(self, command: str) -> None:
        pass
    
    async def set_sync(self, sync: bool) -> None:
        pass