#!/usr/bin/env python3
from nicegui import ui

from windows_moments import capture_moment, show_moments

ui.colors(primary='#0088CC')
with ui.header().classes('dark:bg-[#0088CC88]'):
    ui.label('Window Moments').classes('text-2xl font-medium')
    ui.space()
    ui.button('Capture', icon='add', on_click=capture_moment).props('flat color=white')

with ui.row():
    show_moments()

ui.run(title='Window Moments', favicon='🔲', dark=None)
