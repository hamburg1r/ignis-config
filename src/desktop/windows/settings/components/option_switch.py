# src/desktop/settings/components/option_switch.py
from ignis.widgets.switch import Switch
from ignis.options_manager import OptionsGroup # For type hinting the settings group

class OptionSwitch(Switch):
    """
    A reusable component for a boolean option, backed by an ignis.widgets.Switch.
    It automatically binds to a boolean property in an OptionsGroup.
    """
    def __init__(self, settings_group: OptionsGroup, option_name: str, **kwargs):
        super().__init__(**kwargs)
        self.settings_group = settings_group
        self.option_name = option_name

        # Set initial state from settings
        self.set_active(getattr(settings_group, option_name))

        # Connect to the switch's 'on_change' signal to update settings
        # The on_change signal passes the switch itself and a GParamSpec
        self.on_change = lambda s, g: self._on_switch_changed(s, g)

        # Connect to the settings_group's 'changed' signal to update switch if settings change externally
        settings_group.connect_option(option_name, self._on_settings_changed)

    def _on_switch_changed(self, switch, gparam):
        """Callback for when the switch state changes."""
        new_value = switch.get_active()
        setattr(self.settings_group, self.option_name, new_value)

    def _on_settings_changed(self, settings_group, changed_option_name):
        """Callback for when the corresponding setting changes externally."""
        # Ensure the switch state matches the setting
        self.set_active(getattr(settings_group, self.option_name))
