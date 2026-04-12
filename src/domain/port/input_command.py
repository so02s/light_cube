from abc import ABC, abstractmethod

class InputCommand(ABC):
    @abstractmethod
    async def set_color(cube_id: int, color: str):
        pass

    @abstractmethod
    async def set_synchronize(sync_set: bool):
        pass

    # @abstractmethod
    # async def set_