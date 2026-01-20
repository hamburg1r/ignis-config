import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from ignis.widgets import Box, Button, Entry, Icon, Label, Overlay, Scroll, Window
from ignis.window_manager import WindowManager

window_manager = WindowManager.get_default()


class SearchList(Window):
    def __init__(self, items: list[dict[str,str]] | None = None):
        self._all_items = items or []

        self._search_entry = Entry(
            css_classes=["search-entry"],
            placeholder_text="Search...",
            on_change=self._on_search_changed,
        )

        self._list_container = Box(  # Changed from Gtk.Grid to ignis.widgets.Box
            vertical=True,
            spacing=12,  # Spacing between list items
            margin_top=24,
            margin_bottom=24,
            margin_start=24,
            margin_end=24,
        )

        scrolled_window = Scroll(child=self._list_container, vexpand=True)

        self._child_box = Box(
            vertical=True,
            valign="start",
            halign="center",
            css_classes=["search-content-box"],
            spacing=12,
            child=[
                self._search_entry,
                scrolled_window,
            ],
        )

        super().__init__(
            namespace="search",
            css_classes=["search-window"],
            anchor=["left", "right", "top", "bottom"],
            kb_mode="on_demand",
            layer="bottom",
            visible=False,
            child=Overlay(
                css_classes=["backdrop"],
                child=Button(
                    css_classes=["unset"],
                    vexpand=True,
                    hexpand=True,
                    can_focus=False,
                    on_click=lambda x: window_manager.close_window("search"),
                ),
                overlays=[self._child_box],
            ),
        )
        self._populate_list(self._all_items)

    def _on_search_changed(self, entry: Entry):
        search_text = entry.get_text().lower()
        if not search_text:
            filtered_items = self._all_items
        else:
            filtered_items = [
                item
                for item in self._all_items
                if search_text in item.get("name", "").lower()
            ]
        self._populate_list(filtered_items)

    def _clear_list(self):  # Renamed from _clear_grid
        child = self._list_container.get_first_child()
        while child:
            self._list_container.remove(child)
            child = self._list_container.get_first_child()

    def _populate_list(self, items: list[dict]):  # Renamed from _populate_grid
        self._clear_list()

        for item in items:
            widget = Button(
                css_classes=["unset", "search-list-item"],
                child=Box(
                    orientation="horizontal",  # Changed to horizontal for a list item
                    spacing=12,
                    child=[
                        Icon(image=item.get("icon", "image-missing"), pixel_size=24),  # Smaller icon for list
                        Label(
                            label=item.get("name", "Unnamed"),
                            wrap=True,
                            xalign=0,  # Align text to start
                        ),
                    ],
                ),
            )
            self._list_container.append(widget)  # Changed from self._grid.attach
