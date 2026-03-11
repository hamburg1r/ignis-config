# src/desktop/settings/components/option_dropdown.py
from ignis.widgets.dropdown import DropDown
from ignis.options_manager import OptionsGroup
from typing import get_args, Literal

class OptionDropdown(DropDown):
    """
    A reusable component for an option with a fixed set of choices (Literal type),
    backed by an ignis.widgets.DropDown.
    It automatically binds to a Literal property in an OptionsGroup.
    """
    def __init__(self, settings_group: OptionsGroup, option_name: str, **kwargs):
        self.settings_group = settings_group
        self.option_name = option_name

        # Get the Literal arguments (choices) from the option's type annotation
        # This assumes the OptionsGroup properties are directly annotated.
        option_type = settings_group.__class__.__annotations__.get(option_name)
        
        choices = []
        if option_type and hasattr(option_type, '__origin__') and option_type.__origin__ is Literal:
            choices = [str(c) for c in get_args(option_type)]
        else:
            # Fallback or error if type annotation is not Literal or not found
            print(f"Warning: Could not determine Literal choices for {option_name} from annotations. Using explicit kwarg 'items' or current value.")
            if 'items' in kwargs: # Allow explicit items to be passed
                choices = kwargs.pop('items')
            else:
                choices = [str(getattr(settings_group, option_name))] # Fallback to current value

        super().__init__(
            items=choices, # DropDown items must be strings
            **kwargs
        )
        
        # Set initial state from settings
        current_value = getattr(settings_group, option_name)
        try:
            self.set_selected(str(current_value))
        except ValueError:
            print(f"Warning: Current value '{current_value}' not in dropdown items for {option_name}. Setting to first item.")
            if self.items:
                self.set_selected(self.items[0])


        # Connect to the dropdown's 'on_selected' signal to update settings
        self.on_selected = lambda dd, selected_item: self._on_dropdown_selected(selected_item)

        # Connect to the settings_group's 'changed' signal to update dropdown if settings change externally
        settings_group.connect_option(option_name, self._on_settings_changed)

    def _on_dropdown_selected(self, selected_item: str):
        """Callback for when a dropdown item is selected."""
        # Convert selected_item back to original type if necessary (e.g., int, bool)
        # For Literal, it's usually just string conversion.
        setattr(self.settings_group, self.option_name, selected_item)

    def _on_settings_changed(self, settings_group, changed_option_name):
        """Callback for when the corresponding setting changes externally."""
        # Ensure the dropdown selection matches the setting
        self.set_selected(str(getattr(settings_group, self.option_name)))
