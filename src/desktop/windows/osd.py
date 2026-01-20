from typing import Any, Callable

from gi.repository import Gtk
from ignis import utils, widgets
from ignis.gobject import Binding
from ignis.services.audio import AudioService
from ignis.services.backlight import BacklightService

audio = AudioService.get_default()
backlight = BacklightService.get_default()


class Osd(widgets.Window):
    def __init__(self):
        self.osds = {
            "speaker": self._generate_child(
                self.set_speaker_volume,
                icon=audio.speaker.bind("icon_name"),
                value=audio.speaker.bind("volume"),
            ),
            "microphone": self._generate_child(
                self.set_mic_volume,
                icon=audio.microphone.bind("icon_name"),
                value=audio.microphone.bind("volume"),
            ),
            "brightness": self._generate_child(
                self.set_brightness,
                icon=backlight.bind("brightness", transform=self._get_brightness_icon),
                value=backlight.bind(
                    "brightness", lambda v: int((v / backlight.max_brightness) * 100)
                ),
            ),
        }
        super().__init__(
            layer="overlay",
            anchor=["bottom"],
            namespace="ignis_OSD",
            visible=False,
            css_classes=["osd"],
            setup=self._setup,
        )

    def _setup(self, _):
        connections = {
            "speaker": (audio.speaker, ["is-muted", "volume"]),
            "microphone": (audio.microphone, ["is-muted", "volume"]),
            "brightness": (backlight, ["brightness"]),
        }

        for name, (service, props) in connections.items():
            for prop in props:
                service.connect(f"notify::{prop}", lambda *_, n=name: self.toggle(n))

    def toggle(self, osd: str):
        self.set_child(self.osds[osd])
        self.visible = True
        self._hide()

    @utils.debounce(3000)
    def _hide(self) -> None:
        self.visible = False

    def _generate_child(
        self,
        callback: Callable[[widgets.Scale], None] | None,
        *,
        icon: str | widgets.Icon | Binding | None = None,
        value: int | Binding | None = None,
        widget: Gtk.Widget | None = None,
    ):
        children = []
        if icon:
            children.append(widgets.Icon(css_classes=["icon"], image=icon))
        if value is not None:
            children.append(
                widgets.Scale(
                    vertical=False,
                    css_classes=["material-slider"],
                    min=0,
                    max=100,
                    value=value,
                    hexpand=True,
                    on_change=callback,
                )
            )
        if widget:
            children.append(widget)
        return widgets.Box(child=children)

    def _get_brightness_icon(self, brightness_value: int) -> str:
        if backlight.max_brightness == 0:
            return "display-brightness-off-symbolic" # Or a suitable default

        percentage = (brightness_value / backlight.max_brightness) * 100
        if percentage > 66:
            return "display-brightness-high-symbolic"
        elif percentage > 33:
            return "display-brightness-medium-symbolic"
        else:
            return "display-brightness-low-symbolic"

    def set_speaker_volume(self, value: widgets.Scale):
        audio.speaker.set_volume(value.value)

    def set_mic_volume(self, value: widgets.Scale):
        audio.microphone.set_volume(value.value)

    def set_brightness(self, value: widgets.Scale):
        backlight.set_brightness(backlight.max_brightness * value.value / 100)
