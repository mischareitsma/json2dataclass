from dataclasses import dataclass
from typing import Union


@dataclass
class root:
    """root dataclass"""

    has_pets: bool
    name: str
    pets: list[object]


@dataclass
class root_pets:
    """root_pets dataclass"""

    has_teeth: bool
    likes_tea: bool
    name: str
    type: str
