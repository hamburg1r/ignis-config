from ignis.widgets import Box, Button, Overlay, Window
from ignis.window_manager import WindowManager

window_manager=WindowManager.get_default()

class PopupWindow(Window):
    def __init__(self, name: str, child: Box, **kwargs):
        super().__init__(
            namespace=name,
            css_classes=["search-window"],
            anchor=["left", "right", "top", "bottom"],
            kb_mode="on_demand",
            layer="bottom",
            visible=False,
            popup=True,
            # setup=lambda self: self.connect("notify::visible", self.__on_open),
            child=Overlay(
                css_classes=["backdrop"],
                child=Button(
                    css_classes=["unset"],
                    vexpand=True,
                    hexpand=True,
                    can_focus=False,
                    on_click=lambda x: window_manager.close_window(name),
                ),
                overlays=[child],
            ),
            **kwargs
        )
