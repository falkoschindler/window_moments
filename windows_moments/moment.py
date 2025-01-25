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

    def to_svg(self) -> str:
        min_x = min(screen.x for screen in self.screens.values())
        min_y = min(screen.y for screen in self.screens.values())
        max_x = max(screen.right for screen in self.screens.values())
        max_y = max(screen.bottom for screen in self.screens.values())
        svg = f'<svg viewBox="{min_x} {min_y} {max_x - min_x} {max_y - min_y}" xmlns="http://www.w3.org/2000/svg">'
        for s in self.screens.values():
            svg += (f'<rect x="{s.x}" y="{s.y}" width="{s.width}" height="{s.height}" '
                    'fill="GhostWhite" stroke="LightGray" stroke-width="5" />')
        for w in self.windows.values():
            svg += (f'<rect x="{w.x}" y="{w.y}" width="{w.width}" height="{w.height}" '
                    'fill="AliceBlue" stroke="CornflowerBlue" stroke-width="5" />')
        svg += '</svg>'
        return svg
