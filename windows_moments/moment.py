from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Moment:
    id: str
    name: str
    windows: dict[str, Bounds]

    @classmethod
    def from_dict(cls, data: dict) -> Moment:
        return cls(
            id=data['id'],
            name=data['name'],
            windows={app_name: Bounds(**bounds) for app_name, bounds in data['windows'].items()}
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'windows': {app_name: bounds.to_dict() for app_name, bounds in self.windows.items()}
        }


@dataclass
class Bounds:
    x: int
    y: int
    width: int
    height: int

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @classmethod
    def from_dict(cls, data: dict) -> Bounds:
        return cls(**data)

    def to_dict(self) -> dict[str, int]:
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
        }
