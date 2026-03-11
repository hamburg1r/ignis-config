# src/desktop/settings/components/option_spinbutton.py
from ignis.widgets.spin_button import SpinButton
from ignis.options_manager import OptionsGroup

class OptionSpinButton(SpinButton):
    """
    A reusable component for an integer option, backed by an ignis.widgets.SpinButton.
    It automatically binds to an integer property in an OptionsGroup.
    """
    def __init__(
        self,
        settings_group: OptionsGroup,
        option_name: str,
        min_value: int = 0,
        max_value: int = 100,
        step_increment: int = 1,
        **kwargs
    ):
        super().__init__(
            min=min_value,
            max=max_value,
            step=step_increment,
            **kwargs
        )
        self.settings_group = settings_group
        self.option_name = option_name

        # Set initial state from settings
        self.set_value(getattr(settings_group, option_name))

        # Connect to the spin button's 'on_change' signal to update settings
        self.on_change = lambda sb: self._on_spinbutton_changed(sb)

        # Connect to the settings_group's 'changed' signal to update spin button if settings change externally
        settings_group.connect_option(option_name, self._on_settings_changed)

    def _on_spinbutton_changed(self, spin_button):
        """Callback for when the spin button value changes."""
        new_value = int(spin_button.get_value())
        setattr(self.settings_group, self.option_name, new_value)

    def _on_settings_changed(self, settings_group, changed_option_name):
        """Callback for when the corresponding setting changes externally."""
        # Ensure the spin button value matches the setting
        self.set_value(getattr(settings_group, self.option_name))