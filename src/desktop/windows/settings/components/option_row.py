# src/desktop/settings/components/option_row.py
from ignis.widgets.box import Box
from ignis.widgets.label import Label
# import Gtk # Used for Gtk.Widget type hint - removing as Gtk.Align is removed, will see if Gtk.Widget type hint requires it.

class OptionRow(Box):
    """
    A reusable component for a single option row in the settings.
    It contains a label for the option name and a control widget for its value.
    """
    def __init__(self, label_text: str, control_widget, **kwargs): # Removed Gtk.Widget type hint
        super().__init__(
            vertical=False, # Changed from Gtk.Orientation.HORIZONTAL
            spacing=10, # Adjust spacing as needed
            **kwargs,
        )
        self.set_css_classes(["option-row"]) # For easy styling

        self.label = Label(label=label_text, halign="start", hexpand=True) # Changed from Gtk.Align.START
        self.control = control_widget
        self.control.set_halign("end") # Changed from Gtk.Align.END

        self.append(self.label)
        self.append(self.control)
