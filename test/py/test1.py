from dataclasses import dataclass
from typing import Union


@dataclass
class root:
    """root dataclass"""

    age: Union[int, float]
    name: str
