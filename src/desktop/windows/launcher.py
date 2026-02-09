from gi.repository import Gdk, Gtk
from ignis.widgets import Box, Entry, Icon, Label, ListBox, ListBoxRow, Scroll
from ignis.services.applications import Application, ApplicationsService
from ignis.window_manager import WindowManager

from desktop.abstract.popup_window import PopupWindow

apps_service=ApplicationsService.get_default()

class Launcher(PopupWindow):
    def __init__(self):
        self.entry = Entry(
            placeholder_text="Search apps...",
            on_change=self._change,
        )
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self._on_entry_key_press)
        key_controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        self.entry.add_controller(key_controller)
        self.list_box = ListBox(
            rows=[]
        )
        self.scroll_widget = Scroll(
            child=self.list_box
        )
        child = Box(
            vertical=True,
            valign="center",
            halign="center",
            child=[
                self.entry,
                self.scroll_widget,
            ]
        )
        super().__init__(
            "Launcher",
            child,
        );
        self.connect("show", self._on_window_show)
        self._setup()

    def _setup(self):
        self._set_apps(apps_service.apps)

    def _change(self, *args):
        query=self.entry.text

        if query == "":
            self._setup()
        else:
            self._set_apps(apps_service.search(apps=apps_service.apps,query=query))

    def _set_apps(self, apps: list[Application]):
        self.list_box.remove_all()
        for app in apps:
            self.list_box.append(self._create_app_list_box_row(app))
        
        # Select the first item if the list is not empty
        if self.list_box.get_rows():
            self.list_box.select_row(self.list_box.get_rows()[0])
            self._scroll_to_selected_row()

    def _create_app_list_box_row(self, app: Application) -> ListBoxRow:
        return ListBoxRow(
            on_activate = lambda _: self._on_app_activated(app),
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

    def _on_app_activated(self, app: Application):
        app.launch()
        self.entry.text = ""
        WindowManager.get_default().close_window("Launcher")

    def _scroll_to_selected_row(self):
        selected_row = self.list_box.get_selected_row()
        if not selected_row:
            return

        adj = self.scroll_widget.get_vadjustment()
        if not adj:
            return

        row_allocation = selected_row.get_allocation()
        row_y = row_allocation.y
        row_height = row_allocation.height

        # Current scroll viewport
        viewport_top = adj.get_value()
        viewport_bottom = viewport_top + adj.get_page_size()

        # If row is above viewport, scroll up
        if row_y < viewport_top:
            adj.set_value(row_y)
        # If row is below viewport, scroll down
        elif row_y + row_height > viewport_bottom:
            adj.set_value(row_y + row_height - adj.get_page_size())

    def _on_window_show(self, window):
        self.entry.text = ""
        self._setup()
        self.entry.grab_focus()

    def _on_entry_key_press(self, controller: Gtk.EventControllerKey, keyval: int, keycode: int, state: Gdk.ModifierType):

        selected_row = self.list_box.get_selected_row()
        rows = self.list_box.get_rows()

        if keyval == Gdk.KEY_Up:
            if selected_row:
                idx = selected_row.get_index()
                if idx > 0:
                    self.list_box.select_row(rows[idx - 1])
                    self._scroll_to_selected_row()
                else: # Wrap around to the last item
                    self.list_box.select_row(rows[-1])
                    self._scroll_to_selected_row()
            elif rows: # If no selection, select the last item
                self.list_box.select_row(rows[-1])
                self._scroll_to_selected_row()
            return True  # Stop event propagation

        elif keyval == Gdk.KEY_Down:
            if selected_row:
                idx = selected_row.get_index()
                if idx < len(rows) - 1:
                    self.list_box.select_row(rows[idx + 1])
                    self._scroll_to_selected_row()
                else: # Wrap around to the first item
                    self.list_box.select_row(rows[0])
                    self._scroll_to_selected_row()
            elif rows: # If no selection, select the first item
                self.list_box.select_row(rows[0])
                self._scroll_to_selected_row()
            return True  # Stop event propagation

        elif keyval == Gdk.KEY_Return:
            if selected_row:
                self.list_box.activate_row(rows[selected_row.get_index()])
            return True  # Stop event propagation

        elif keyval == Gdk.KEY_Left or keyval == Gdk.KEY_Right:
            return False  # Let the Entry handle Left/Right arrows

        return False  # Let other keys be handled by the Entry
