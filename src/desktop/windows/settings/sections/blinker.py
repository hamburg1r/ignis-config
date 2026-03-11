# src/desktop/settings/sections/blinker.py
from ignis.widgets.box import Box
from ignis.widgets.label import Label
from ignis.options_manager import OptionsGroup
from desktop.options import settings

from desktop.windows.settings.components import OptionRow, OptionSpinButton
# import Gtk # Removed: no longer needed for Gtk.Orientation

class BlinkerSettingsBox(Box):
    """
    Settings section for Blinker options.
    """
    def __init__(self, **kwargs):
        super().__init__(
            vertical=True, # Changed from Gtk.Orientation.VERTICAL
            spacing=10,
            **kwargs,
        )
        self.set_css_classes(["settings-section"])

        self.append(Label(label="<b>Blinker Settings</b>", use_markup=True, halign=Gtk.Align.START))

        blinker_options: OptionsGroup = settings.blinker

        # Option: blink_interval_ms (int)
        self.append(OptionRow(
            label_text="Blink Interval (ms)",
            control_widget=OptionSpinButton(settings_group=blinker_options, option_name="blink_interval_ms", min_value=100, max_value=10000, step_increment=100)
        ))

        # Option: blink_duration_ms (int)
        self.append(OptionRow(
            label_text="Blink Duration (ms)",
            control_widget=OptionSpinButton(settings_group=blinker_options, option_name="blink_duration_ms", min_value=10, max_value=2000, step_increment=10)
        ))