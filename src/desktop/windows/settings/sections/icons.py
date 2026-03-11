# src/desktop/settings/sections/icons.py
from ignis.widgets.box import Box
from ignis.widgets.label import Label
from ignis.options_manager import OptionsGroup
from desktop.options import settings

from desktop.windows.settings.components import OptionRow, OptionDropdown
# import Gtk # Removed: no longer needed for Gtk.Orientation

class IconsSettingsBox(Box):
    """
    Settings section for Icons options.
    """
    def __init__(self, **kwargs):
        super().__init__(
            vertical=True, # Changed from Gtk.Orientation.VERTICAL
            spacing=10,
            **kwargs,
        )
        self.set_css_classes(["settings-section"])

        self.append(Label(label="<b>Icon Settings</b>", use_markup=True, halign=Gtk.Align.START))

        icons_options: OptionsGroup = settings.icons

        # Option: icon_theme (Literal["material", "fontawesome", "codicons", "image"])
        self.append(OptionRow(
            label_text="Global Icon Theme",
            control_widget=OptionDropdown(settings_group=icons_options, option_name="icon_theme")
        ))

        # Note: Blinker_start and Blinker_stop (dictionaries) are not exposed via UI directly here.
        # Managing dictionary options requires more complex UI (e.g., list editor, text editor).
        # For simplicity, we only expose the global 'icon_theme' for now.