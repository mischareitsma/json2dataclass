from dataclasses import dataclass
from typing import Union


@dataclass
class root:
    """root dataclass"""

    layerOne: object


@dataclass
class root_layerOne:
    """root_layerOne dataclass"""

    layerTwo: object


@dataclass
class root_layerOne_layerTwo:
    """root_layerOne_layerTwo dataclass"""

    layerThree: list[object]


@dataclass
class root_layerOne_layerTwo_layerThree:
    """root_layerOne_layerTwo_layerThree dataclass"""

    layerFour: object


@dataclass
class root_layerOne_layerTwo_layerThree_layerFour:
    """root_layerOne_layerTwo_layerThree_layerFour dataclass"""

    _finally: str
