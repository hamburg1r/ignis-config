import gi
from ignis import utils

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ignis.widgets import Box, Grid, Icon, Label, Scroll, Window


class IconBrowser(Window):
    def __init__(self):
        super().__init__(
            namespace="icon-browser",
            layer="bottom",
            visible=True,
            title="Icon Browser",
        )
        # self.set_default_size(800, 600)

        icon_theme = Gtk.IconTheme.get_for_display(utils.get_gdk_display())
        icon_names = sorted(icon_theme.get_icon_names())

        grid = Grid(
            column_spacing=12,
            row_spacing=12,
            margin_top=12,
            margin_bottom=12,
            margin_start=12,
            margin_end=12,
        )

        column_count = 3
        # Filter out invalid icons and create widgets
        filtered_names = [
            name for name in icon_names if name and icon_theme.has_icon(name)
        ]

        for i, name in enumerate(filtered_names):
            box = Box(
                orientation="vertical",
                spacing=6,
                child=[
                    Icon(image=name, pixel_size=48),
                    Label(label=name, wrap=True, max_width_chars=12, justify="center"),
                ],
            )
            row, col = divmod(i, column_count)
            grid.attach(box, col, row, 1, 1)

        scroll = Scroll(child=grid)
        self.set_child(scroll)
