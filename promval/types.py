from dataclasses import dataclass


@dataclass
class Label:
    name: str
    operator: str
    value: str
