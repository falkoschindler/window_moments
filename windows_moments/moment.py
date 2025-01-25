from __future__ import annotations

from dataclasses import dataclass

from .bounds import Bounds


@dataclass
class Moment:
    id: str
    name: str
    windows: dict[str, Bounds]
    screens: dict[str, Bounds]

    @classmethod
    def from_dict(cls, data: dict) -> Moment:
        return cls(
            id=data['id'],
            name=data['name'],
            windows={app_name: Bounds(**bounds) for app_name, bounds in data['windows'].items()},
            screens={screen_name: Bounds(**bounds) for screen_name, bounds in data['screens'].items()},
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'windows': {app_name: bounds.to_dict() for app_name, bounds in self.windows.items()},
            'screens': {screen_name: bounds.to_dict() for screen_name, bounds in self.screens.items()},
        }
