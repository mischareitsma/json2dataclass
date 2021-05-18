from dataclasses import dataclass
from typing import Union


@dataclass
class root:
    """root dataclass"""

    layerOne: root_layerOne


@dataclass
class root_layerOne:
    """root_layerOne dataclass"""

    layerTwo: root_layerOne_layerTwo


@dataclass
class root_layerOne_layerTwo:
    """root_layerOne_layerTwo dataclass"""

    layerThree: list[root_layerOne_layerTwo_layerThree]


@dataclass
class root_layerOne_layerTwo_layerThree:
    """root_layerOne_layerTwo_layerThree dataclass"""

    layerFour: root_layerOne_layerTwo_layerThree_layerFour


@dataclass
class root_layerOne_layerTwo_layerThree_layerFour:
    """root_layerOne_layerTwo_layerThree_layerFour dataclass"""

    _finally: str
