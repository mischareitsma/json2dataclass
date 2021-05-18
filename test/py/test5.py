from dataclasses import dataclass
from typing import Union


@dataclass
class root:
    """root dataclass"""

    assignee: Union[int, float]
    assigner: Union[int, float]
    comment_count: Union[int, float]
    completed: bool
    content: str
    description: str
    due: root_due
    id: Union[int, float]
    label_ids: list[Union[int, float]]
    order: Union[int, float]
    parent_id: Union[int, float]
    priority: Union[int, float]
    project_id: Union[int, float]
    section_id: Union[int, float]
    url: str


@dataclass
class root_due:
    """root_due dataclass"""

    date: str
    datetime: str
    recurring: bool
    string: str
    timezone: str
