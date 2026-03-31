from dataclasses import dataclass

@dataclass
class Color:
    name: str
    value: str

    def __str__(self):
        return self.value