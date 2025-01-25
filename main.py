#!/usr/bin/env python3
from nicegui import ui

from windows_moments import capture_moment, show_moments

ui.colors(primary='#0088CC')
with ui.header():
    ui.label('Window Moments').classes('text-2xl font-medium')

show_moments()

ui.button('Capture moment', icon='add', on_click=capture_moment).props('unelevated')

ui.run()
