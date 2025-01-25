import uuid
from datetime import datetime

from nicegui import app, ui

from .moment import Moment
from .system import apply_moment, collect_windows


def capture_moment() -> None:
    moment = Moment(
        id=str(uuid.uuid4()),
        name=datetime.now().strftime(r'%Y-%m-%d %H:%M:%S'),
        windows=collect_windows(),
    )
    save_moment(moment)


def recapture_moment(moment: Moment) -> None:
    moment.windows.update(collect_windows())
    save_moment(moment)


def rename_moment(moment: Moment, name: str) -> None:
    moment.name = name
    save_moment(moment)


def save_moment(moment: Moment) -> None:
    data = app.storage.general.get('moments', {})
    data[moment.id] = moment.to_dict()
    app.storage.general['moments'] = data
    show_moments.refresh()


def delete_moment(moment: Moment) -> None:
    data = app.storage.general.get('moments', {})
    data.pop(moment.id)
    app.storage.general['moments'] = data
    show_moments.refresh()


@ui.refreshable
def show_moments():
    moments = [Moment.from_dict(m) for m in app.storage.general.get('moments', {}).values()]
    for moment in moments:
        with ui.card():
            ui.input(value=moment.name).props('borderless').classes('text-2xl font-medium') \
                .on('keydown.enter', lambda e, m=moment: rename_moment(m, e.sender.value)) \
                .on('keydown.escape', lambda e, m=moment: rename_moment(m, e.sender.value)) \
                .on('blur', lambda e, m=moment: rename_moment(m, e.sender.value))
            code = ui.code('\n'.join(f'{app_name}: {bounds.x}, {bounds.y}, {bounds.width}, {bounds.height}'
                                     for app_name, bounds in moment.windows.items()))
            code.copy_button.delete()
            with ui.card_actions().classes('w-full justify-end'):
                ui.button('Apply', icon='check', on_click=lambda moment=moment: apply_moment(moment)) \
                    .props('flat')
                with ui.button(icon='more_vert').props('flat'):
                    with ui.menu():
                        with ui.item(on_click=lambda moment=moment: recapture_moment(moment)):
                            with ui.item_section().props('side'):
                                ui.icon('refresh')
                            ui.item_section('Recapture')
                        with ui.item(on_click=lambda moment=moment: delete_moment(moment)):
                            with ui.item_section().props('side'):
                                ui.icon('clear', color='red')
                            ui.item_section('Delete')
