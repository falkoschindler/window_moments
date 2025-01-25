from __future__ import annotations

from dataclasses import dataclass


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
