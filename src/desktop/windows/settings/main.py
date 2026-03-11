# src/desktop/windows/settings/main.py
from ignis.widgets.regular_window import RegularWindow
from ignis.widgets.box import Box
from ignis.widgets.stack import Stack
from ignis.widgets.stack_switcher import StackSwitcher
from ignis.widgets.stack_page import StackPage
# import Gtk # Removed - Relying on implicit availability of Gtk.Align or re-adding if error occurs

from desktop.windows.settings.sections import (
    BarSettingsBox,
    DateTimeSettingsBox,
    BatterySettingsBox,
    BlinkerSettingsBox,
    IconsSettingsBox,
    UserSettingsBox,
)

class SettingsWindow(RegularWindow):
    """
    A window for displaying and managing application settings,
    organized into sections with a Stack and StackSwitcher.
    """
    def __init__(self, **kwargs):
        super().__init__(
            namespace="settings",
            title="Settings",
            default_width=600, # Set a reasonable default size
            default_height=400,
            **kwargs,
        )

        main_box = Box(vertical=False, spacing=10) # Main horizontal layout
        # Left side: StackSwitcher for navigation
        self.stack = Stack(transition_type="slide_left") # Stack to hold the settings sections
        self.switcher = StackSwitcher(stack=self.stack) # Switcher for navigation

        left_panel = Box(vertical=True, spacing=5)
        left_panel.set_css_classes(["settings-sidebar"])
        left_panel.append(self.switcher)

        # Right side: Stack containing the actual settings sections
        right_panel = Box(vertical=True)
        right_panel.append(self.stack)
        # Changed Gtk.Align.FILL to string "fill"
        right_panel.set_halign("fill")
        right_panel.set_valign("fill")
        right_panel.set_hexpand(True)
        right_panel.set_vexpand(True)

        main_box.append(left_panel)
        main_box.append(right_panel)

        self.set_child(main_box)

        # Add all settings sections to the stack
        self._add_settings_sections()

    def _add_settings_sections(self):
        """
        Adds instances of all settings section widgets to the stack.
        """
        sections = [
            ("Bar", BarSettingsBox()),
            ("Date & Time", DateTimeSettingsBox()),
            ("Battery", BatterySettingsBox()),
            ("Blinker", BlinkerSettingsBox()),
            ("Icons", IconsSettingsBox()),
            ("User", UserSettingsBox()),
        ]

        for title, section_widget in sections:
            self.stack.add_child(StackPage(title=title, child=section_widget))