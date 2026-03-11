# src/desktop/settings/sections/datetime.py
from ignis.widgets.box import Box
from ignis.widgets.label import Label
from ignis.options_manager import OptionsGroup
from desktop.options import settings

from desktop.windows.settings.components import OptionRow, OptionEntry, OptionSpinButton, OptionDropdown
# import Gtk # Removed: no longer needed for Gtk.Orientation

class DateTimeSettingsBox(Box):
    """
    Settings section for DateTime options.
    """
    def __init__(self, **kwargs):
        super().__init__(
            vertical=True, # Changed from Gtk.Orientation.VERTICAL
            spacing=10,
            **kwargs,
        )
        self.set_css_classes(["settings-section"])

        self.append(Label(label="<b>Date & Time Settings</b>", use_markup=True, halign=Gtk.Align.START))

        datetime_options: OptionsGroup = settings.date_time

        # Option: horizontal_format (str)
        self.append(OptionRow(
            label_text="Horizontal Format",
            control_widget=OptionEntry(settings_group=datetime_options, option_name="horizontal_format")
        ))

        # Option: vertical_format (str)
        self.append(OptionRow(
            label_text="Vertical Format",
            control_widget=OptionEntry(settings_group=datetime_options, option_name="vertical_format")
        ))

        # Option: tooltip_format (str)
        self.append(OptionRow(
            label_text="Tooltip Format",
            control_widget=OptionEntry(settings_group=datetime_options, option_name="tooltip_format")
        ))

        # Option: polling_time (int)
        self.append(OptionRow(
            label_text="Polling Time (ms)",
            control_widget=OptionSpinButton(settings_group=datetime_options, option_name="polling_time", min_value=100, max_value=5000, step_increment=100)
        ))

        # Option: display_mode (Literal["icon_only", "text_only", "icon_and_text"])
        self.append(OptionRow(
            label_text="Display Mode",
            control_widget=OptionDropdown(settings_group=datetime_options, option_name="display_mode")
        ))

        # Option: icon_name (str)
        self.append(OptionRow(
            label_text="Icon Name",
            control_widget=OptionEntry(settings_group=datetime_options, option_name="icon_name")
        ))