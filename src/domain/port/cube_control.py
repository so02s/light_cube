from abc import ABC, abstractmethod
from ..model.color import Color
from ..model.cube import Cube

class LightOutput(ABC):
    @abstractmethod
    async def turn_on_all(self) -> None:
        pass

    @abstractmethod
    async def turn_off_all(self) -> None:
        pass

    @abstractmethod
    async def set_color(self, cube: Cube, color: Color) -> None:
        pass

    @abstractmethod
    async def set_color_all(self, color: Color) -> None:
        pass
    
    @abstractmethod
    async def set_command(self, cube: Cube, command: str) -> None:
        pass

    @abstractmethod
    async def set_command_all(self, command: str) -> None:
        pass

    @abstractmethod
    async def set_sync(self, sync: bool) -> None:
        pass