# src/desktop/settings/sections/battery.py
from ignis.widgets.box import Box
from ignis.widgets.label import Label
from ignis.options_manager import OptionsGroup
from desktop.options import settings

from desktop.windows.settings.components import OptionRow, OptionEntry, OptionSwitch, OptionSpinButton
# import Gtk # Removed: no longer needed for Gtk.Orientation

class BatterySettingsBox(Box):
    """
    Settings section for Battery options.
    """
    def __init__(self, **kwargs):
        super().__init__(
            vertical=True, # Changed from Gtk.Orientation.VERTICAL
            spacing=10,
            **kwargs,
        )
        self.set_css_classes(["settings-section"])

        self.append(Label(label="<b>Battery Settings</b>", use_markup=True, halign=Gtk.Align.START))

        battery_options: OptionsGroup = settings.battery

        # Option: max (int)
        self.append(OptionRow(
            label_text="Max Percentage",
            control_widget=OptionSpinButton(settings_group=battery_options, option_name="max", min_value=1, max_value=100)
        ))

        # Option: show_battery (bool)
        self.append(OptionRow(
            label_text="Show Battery Icon",
            control_widget=OptionSwitch(settings_group=battery_options, option_name="show_battery")
        ))

        # Option: format_string (str)
        self.append(OptionRow(
            label_text="Format String",
            control_widget=OptionEntry(settings_group=battery_options, option_name="format_string")
        ))