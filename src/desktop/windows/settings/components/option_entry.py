# src/desktop/settings/components/option_entry.py
from ignis.widgets.entry import Entry
from ignis.options_manager import OptionsGroup

class OptionEntry(Entry):
    """
    A reusable component for a string option, backed by an ignis.widgets.Entry.
    It automatically binds to a string property in an OptionsGroup.
    """
    def __init__(self, settings_group: OptionsGroup, option_name: str, **kwargs):
        super().__init__(**kwargs)
        self.settings_group = settings_group
        self.option_name = option_name

        # Set initial state from settings
        self.set_text(str(getattr(settings_group, option_name)))

        # Connect to the entry's 'on_change' signal to update settings
        self.on_change = lambda e: self._on_entry_changed(e)

        # Connect to the settings_group's 'changed' signal to update entry if settings change externally
        settings_group.connect_option(option_name, self._on_settings_changed)

    def _on_entry_changed(self, entry):
        """Callback for when the entry text changes."""
        new_value = entry.get_text()
        setattr(self.settings_group, self.option_name, new_value)

    def _on_settings_changed(self, settings_group, changed_option_name):
        """Callback for when the corresponding setting changes externally."""
        # Ensure the entry text matches the setting
        self.set_text(str(getattr(settings_group, self.option_name)))
