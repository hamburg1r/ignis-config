# src/desktop/windows/blinker.py
# import Gtk # Removed as per user instruction
# import GLib # Removed as per user instruction

from ignis.widgets.window import Window
from ignis.widgets.box import Box
from ignis.utils.poll import Poll # For repeated timer calls
from ignis.utils.timeout import Timeout # For single-shot timer

from desktop.options import settings # Import the settings object
# Removed: from ignis.window_manager import WindowManager


class Blinker(Window):
    """
    A non-interactive popup window designed to "blink" or paint the screen
    without accepting any input.

    This window covers the entire screen as an overlay, ignores exclusivity,
    does not respond to keyboard events, and is pass-through for mouse clicks.
    The visual "blinking" effect can be achieved by styling the
    'blinker-window-background' CSS class of its child Box.
    """

    def __init__(self, namespace: str, **kwargs):
        super().__init__(
            namespace=namespace,
            layer="overlay",
            exclusivity="ignore",
            kb_mode="none",
            anchor=["left", "right", "top", "bottom"],
            popup=False,
            margin_bottom=0,
            margin_left=0,
            margin_right=0,
            margin_top=0,
            visible=False,
            **kwargs,
        )

        self.blinker_box = Box(
            name="blinker-box",
            vertical=True,
            css_classes=["blinker-window-background"],
            hexpand=True,
            vexpand=True,
        )
        self.set_child(self.blinker_box)

        # Removed: self.window_manager = WindowManager.get_default()

        self._blink_poll: Poll | None = None
        self._hide_timeout: Timeout | None = None
        self._is_blinking_on: bool = False

    def _hide_blinker_after_timeout(self):
        """
        Hides the blinker after the short timeout.
        """
        self.blinker_box.remove_css_class("blinker-active")
        self.visible = False # Changed from WindowManager call
        self._is_blinking_on = False
        self._hide_timeout = None

    def _blink_callback(self, poll_instance: Poll):
        """
        Callback function for the main poll timer.
        Starts the visibility phase using the configured duration.
        """
        if self._hide_timeout:
            self._hide_timeout.cancel()
            self._hide_timeout = None

        self.blinker_box.add_css_class("blinker-active")
        self.visible = True # Changed from WindowManager call
        self._is_blinking_on = True

        self._hide_timeout = Timeout(ms=settings.blinker.blink_duration_ms, target=self._hide_blinker_after_timeout)

        return True

    def start(self):
        """
        Starts the blinking effect.
        """
        if self._blink_poll:
            return

        self.blinker_box.remove_css_class("blinker-active")
        self.visible = False # Changed from WindowManager call
        self._is_blinking_on = False

        self._blink_poll = Poll(timeout=settings.blinker.blink_interval_ms, callback=self._blink_callback)

    def stop(self):
        """
        Stops the blinking effect.
        """
        if self._blink_poll:
            self._blink_poll.cancel()
            self._blink_poll = None
        
        if self._hide_timeout:
            self._hide_timeout.cancel()
            self._hide_timeout = None

        self.blinker_box.remove_css_class("blinker-active")
        self.visible = False # Changed from WindowManager call
        self._is_blinking_on = False