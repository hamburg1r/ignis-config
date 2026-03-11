# src/desktop/widgets/blinker_button.py
from ignis.widgets.button import Button
from ignis.widgets.label import Label
from desktop.windows.blinker import Blinker # Import the Blinker class
from desktop.utils.icon_manager import get_icon # New import


class BlinkerButton(Button):
    """
    A button widget that toggles the start and stop of a Blinker instance.
    """

    def __init__(self, blinker: Blinker, **kwargs):
        """
        Initializes the BlinkerButton.

        Args:
            blinker: The Blinker instance to control.
            **kwargs: Additional keyword arguments to pass to the Button constructor.
        """
        # Set a default label if not provided in kwargs
        if "child" not in kwargs:
            kwargs["child"] = Label(label=get_icon("blinker_start")) # Use get_icon
        
        super().__init__(**kwargs)
        self.blinker = blinker
        self._is_blinker_active = False

        # Set the on_click handler to our toggle method using a lambda
        # The lambda ignores the 'button' argument passed by the signal
        self.on_click = lambda _: self._toggle_blinker()

    def _toggle_blinker(self):
        """
        Toggles the Blinker's start/stop state.
        """
        if self._is_blinker_active:
            self.blinker.stop()
            self._is_blinker_active = False
            if isinstance(self.child, Label):
                self.child.label = get_icon("blinker_start") # Use get_icon
        else:
            self.blinker.start()
            self._is_blinker_active = True
            if isinstance(self.child, Label):
                self.child.label = get_icon("blinker_stop") # Use get_icon