# src/desktop/settings/sections/user.py
from ignis.widgets.box import Box
from ignis.widgets.label import Label
from ignis.options_manager import OptionsGroup
from desktop.options import settings

from desktop.windows.settings.components import OptionRow, OptionEntry
# import Gtk # Removed: no longer needed for Gtk.Orientation

class UserSettingsBox(Box):
    """
    Settings section for User options.
    """
    def __init__(self, **kwargs):
        super().__init__(
            vertical=True, # Changed from Gtk.Orientation.VERTICAL
            spacing=10,
            **kwargs,
        )
        self.set_css_classes(["settings-section"])

        self.append(Label(label="<b>User Settings</b>", use_markup=True, halign=Gtk.Align.START))

        user_options: OptionsGroup = settings.user

        # Option: terminal_command (str)
        self.append(OptionRow(
            label_text="Terminal Command",
            control_widget=OptionEntry(settings_group=user_options, option_name="terminal_command")
        ))

        # Note: Nested 'Colors' OptionsGroup and 'colors' dictionary are not exposed directly here
        # due to complexity. They would require more advanced UI components or recursive rendering.