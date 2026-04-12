# Okay, I'm not sure what I'm doing
# Maybe that's not okay to call MQTT command here
# but idk I don't have a mentor
# just need to be work

from ..model.cube import Cube
from ..model.color import Color
from ..port.cube_control import LightOutput

class CubeControl:
    def __init__(self, light_output: LightOutput):
        self._light_output = light_output

    async def turn_all_on(self) -> None:
        await self._light_output.turn_on_all()

    async def turn_all_off(self) -> None:
        await self._light_output.turn_off_all()

    async def set_color(self, cube: Cube, color: Color) -> None:
        await self._light_output.set_color(cube, color)