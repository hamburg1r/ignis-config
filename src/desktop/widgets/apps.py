from typing import cast
from ignis import widgets
from ignis.utils import Utils
from ignis.window_manager import WindowManager
from ignis.services.applications import ApplicationsService, Application
from ignis.services.hyprland import HyprlandService, HyprlandWindow
from ignis.menu_model import IgnisMenuModel, IgnisMenuItem, IgnisMenuSeparator

from desktop.options import settins
from desktop.utils import toggle_launcher

applications = ApplicationsService.get_default()
window_manager = WindowManager.get_default()
hyprland = HyprlandService.get_default()

class ApplicationWithStats:
    def __init__(self, app: Application) -> None:
        self.application: Application = app
        self.active: bool = False

    def setActive(self):
        self.active = True

    def setInactive(self):
        self.active = False

class AppItem(widgets.Button):
    def __init__(self, app: Application, running: bool = False):
        menu = widgets.PopoverMenu(
            model=IgnisMenuModel(
                *(
                    IgnisMenuItem(label="Launch", on_activate=lambda _: app.launch()),
                    IgnisMenuSeparator()
                ) if not running else (),
                *(
                    IgnisMenuItem(
                        label=i.name, on_activate=lambda _, action=i: action.launch()
                    )
                    for i in app.actions
                ),
                IgnisMenuSeparator(),
                IgnisMenuItem(label="Unpin", on_activate=lambda x: app.unpin()),
            )
        )

        super().__init__(
            child=widgets.Box(child=[widgets.Icon(image=app.icon, pixel_size=32), menu]),
            on_click=lambda x: app.launch(terminal_format=settins.user.terminal_command),
            on_right_click=lambda x: menu.popup(),
            css_classes=["pinned-app", "unset"],
        )


class Apps(widgets.Box):
    def __init__(self):
        self.apps: list[Application] = []
        super().__init__(
            child=applications.bind(
                "pinned",
                transform=lambda value: [AppItem(app) for app in value]
                # + [
                #     widgets.Box(
                #         child = hyprland.bind(
                #             "windows",
                #             transform = lambda _: [
                #                 widgets.Button(
                #                     child = widgets.Icon(icon_name=Utils.get_app_icon_name(window.class_name)),
                #                     tooltip_text = window.title,
                #                     on_click = self.focusClient(window.address),
                #                 ) for window in self.fetchClients()
                #             ]
                #         )
                #     )
                # ]
                + [
                    widgets.Button(
                        child=widgets.Icon(image="start-here-symbolic", pixel_size=32),
                        on_click=lambda x: toggle_launcher(),
                        css_classes=["pinned-app", "unset"],
                    )
                ],
            )
        )

    def fetchClients(self):
        clients: list[HyprlandWindow] = cast(list[HyprlandWindow], hyprland.windows)
        for c in clients:
            print(c.class_name)
        clients = sorted(clients, key=lambda client: client.class_name)
        for c in clients:
            print(c.class_name)
        return clients

    def focusClient(self, address: str):
        cmd = f"dispatch focuswindow address:{address}"
        cmd_next = "dispatch alterzorder top"
        def callback(_):
            print(hyprland.send_command(cmd))
            print(hyprland.send_command(cmd_next))
        return callback
