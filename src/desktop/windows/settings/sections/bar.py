# src/desktop/settings/sections/bar.py
from ignis.widgets.box import Box
from ignis.widgets.label import Label
from ignis.options_manager import OptionsGroup # For type hinting
from desktop.options import settings # Global settings object

from desktop.windows.settings.components import OptionRow, OptionSwitch, OptionDropdown
# import Gtk # Removed: no longer needed for Gtk.Orientation

class BarSettingsBox(Box):
    """
    Settings section for Bar options.
    """
    def __init__(self, **kwargs):
        super().__init__(
            vertical=True, # Changed from Gtk.Orientation.VERTICAL
            spacing=10,
            **kwargs,
        )
        self.set_css_classes(["settings-section"])

        self.append(Label(label="<b>Bar Settings</b>", use_markup=True, halign=Gtk.Align.START))

        # Get the Bar options group
        bar_options: OptionsGroup = settings.bar

        # Option: direction (Literal['vertical', 'horizontal'])
        self.append(OptionRow(
            label_text="Direction",
            control_widget=OptionDropdown(settings_group=bar_options, option_name="direction")
        ))

        # Option: side (Literal['left', 'right', 'top', 'bottom'])
        self.append(OptionRow(
            label_text="Side",
            control_widget=OptionDropdown(settings_group=bar_options, option_name="side")
        ))