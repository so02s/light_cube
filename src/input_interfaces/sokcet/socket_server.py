import asyncio
import logging

from src.domain.service.cube_control_impl import CubeControl
from src.domain.model.color import Color
from src.domain.model.cube import Cube

logger = logging.getLogger(__name__)

class SocketCommandServer:
    def __init__(self):
        pass