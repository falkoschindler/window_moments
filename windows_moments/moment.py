from __future__ import annotations

from dataclasses import dataclass

from .bounds import Bounds


@dataclass
class Moment:
    id: str
    name: str
    windows: dict[str, list[Bounds]]
    screens: dict[str, Bounds]

    @classmethod
    def from_dict(cls, data: dict) -> Moment:
        return cls(
            id=data['id'],
            name=data['name'],
            windows={app_name: [Bounds(**bounds) for bounds in list_of_bounds]
                     for app_name, list_of_bounds in data['windows'].items()},
            screens={screen_name: Bounds(**bounds)
                     for screen_name, bounds in data['screens'].items()},
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'windows': {app_name: [bounds.to_dict() for bounds in list_of_bounds]
                        for app_name, list_of_bounds in self.windows.items()},
            'screens': {screen_name: bounds.to_dict()
                        for screen_name, bounds in self.screens.items()},
        }

    def to_svg(self) -> str:
        min_x = min(screen.x for screen in self.screens.values())
        min_y = min(screen.y for screen in self.screens.values())
        max_x = max(screen.right for screen in self.screens.values())
        max_y = max(screen.bottom for screen in self.screens.values())
        svg = f'<svg viewBox="{min_x} {min_y} {max_x - min_x} {max_y - min_y}" xmlns="http://www.w3.org/2000/svg">'
        for list_of_bounds in self.windows.values():
            for b in list_of_bounds:
                tailwind = 'class="fill-slate-500/30 stroke-slate-500/50 stroke-[2]"'
                svg += (f'<rect x="{b.x+1}" y="{b.y+1}" width="{b.width-2}" height="{b.height-2}" {tailwind} />')
        svg += '</svg>'
        return svg
