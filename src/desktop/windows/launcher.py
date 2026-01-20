from ignis.widgets import Box, Entry, Icon, Label, ListBox, ListBoxRow, Scroll
from ignis.services.applications import Application, ApplicationsService

from desktop.abstract.popup_window import PopupWindow

apps_service=ApplicationsService.get_default()

class Launcher(PopupWindow):
    def __init__(self):
        self.entry = Entry(
            placeholder_text="Search apps...",
            on_accept=lambda *args: self.list_box.activate(),
            on_change=self._change,
        )
        self.list_box = ListBox(
                    rows=[]
                )
        child = Box(
            vertical=True,
            valign="center",
            halign="center",
            child=[
                self.entry,
                Scroll(
                    child=Box(
                        width_request=30,
                        height_request=100,
                        child=self.list_box
                    )
                )
            ]
        )
        super().__init__(
            "Launcher",
            child,
        );
        self._setup()

    def _setup(self):
        self._set_apps(apps_service.apps)

    def _change(self, *args):
        query=self.entry.text

        if query == "":
            self._setup()

        self._set_apps(apps_service.search(apps=apps_service.apps,query=query))

    def _set_apps(self, apps: list[Application]):
        print("got apps:", apps)
        self.list_box.rows = [
            self._create_app_list_box_row(app) for app in apps
        ]

    def _create_app_list_box_row(self, app: Application) -> ListBoxRow:
        return ListBoxRow(
            child=Box(
                child=[
                    Icon(
                        image = app.bind('icon'),
                    ),
                    Box(
                        vertical=True,
                        child=[
                            Label(
                                label=app.bind('name')
                            ),
                            Label(
                                label=app.bind('description')
                            )
                        ]
                    )
                ]
            )
        )

    def _update_list_box(self, *args):
        pass
