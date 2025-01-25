import subprocess
from collections import Counter

import Quartz

from .moment import Bounds, Moment


def collect_windows() -> dict[str, list[Bounds]]:
    result: dict[str, list[Bounds]] = {}
    for window in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly |
                                                    Quartz.kCGWindowListExcludeDesktopElements,
                                                    Quartz.kCGNullWindowID):
        if window.get(Quartz.kCGWindowLayer, 0) != 0:
            continue
        app_name = window.get(Quartz.kCGWindowOwnerName, '')
        bounds = window.get(Quartz.kCGWindowBounds)
        if app_name and bounds:
            if app_name not in result:
                result[app_name] = []
            result[app_name].append(Bounds(
                x=int(bounds['X']),
                y=int(bounds['Y']),
                width=int(bounds['Width']),
                height=int(bounds['Height']),
            ))
    return result


def collect_screens() -> dict[str, Bounds]:
    result: dict[str, Bounds] = {}
    for display in Quartz.CGGetActiveDisplayList(32, None, None)[1]:
        bounds = Quartz.CGDisplayBounds(display)
        result[str(display)] = Bounds(
            x=int(bounds.origin.x),
            y=int(bounds.origin.y),
            width=int(bounds.size.width),
            height=int(bounds.size.height),
        )
    return result


def apply_moment(moment: Moment) -> None:
    windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly |
                                                Quartz.kCGWindowListExcludeDesktopElements,
                                                Quartz.kCGNullWindowID)
    window_names = Counter(window.get(Quartz.kCGWindowOwnerName, '') for window in windows)
    for window_name, count in window_names.items():
        if window_name not in moment.windows:
            continue
        list_of_bounds = moment.windows[window_name]
        for i in range(min(count, len(list_of_bounds))):
            bounds = list_of_bounds[i]
            script = f'''
                tell application "{window_name}"
                    try
                        set the bounds of window {i+1} to {{{bounds.x}, {bounds.y}, {bounds.right}, {bounds.bottom}}}
                    on error
                        tell application "System Events"
                            tell process "{window_name}"
                                try
                                    set position of window {i+1} to {{{bounds.x}, {bounds.y}}}
                                    set size of window {i+1} to {{{bounds.width}, {bounds.height}}}
                                end try
                            end tell
                        end tell
                    end try
                end tell
            '''
            try:
                result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=False)
                if result.returncode != 0:
                    print(f'Warning: Could not move window for {window_name}: {result.stderr}')
            except subprocess.CalledProcessError as e:
                print(f'Failed to apply moment for {window_name}: {e}')
