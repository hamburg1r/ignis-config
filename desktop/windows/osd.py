from typing import Any, Callable
from ignis import utils, widgets
from ignis.gobject import Binding
from ignis.services.audio import AudioService
from ignis.services.backlight import BacklightService
from gi.repository import Gtk

audio = AudioService.get_default()
backlight = BacklightService.get_default()

class Osd(widgets.Window):
	def __init__(self):
		# self.debug_brightness()
		# self.wow()
		self.osds = {
			"speaker": self.genrateChild(
				self.set_speaker_volume,
				icon=audio.speaker.bind("icon_name"),
				value=audio.speaker.bind("volume"),
			),
			"microphone": self.genrateChild(
				self.set_mic_volume,
				icon=audio.microphone.bind("icon_name"),
				value=audio.microphone.bind("volume")
			),
			"brightness": self.genrateChild(
				self.set_brightness,
				# icon="brightness",
				value=backlight.bind("brightness", lambda v: (v/backlight.max_brightness)*100)
			)
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
		audio.speaker.connect("notify::is-muted", lambda *_: self.toggle("speaker"))
		audio.speaker.connect("notify::volume", lambda *_: self.toggle("speaker"))
		audio.microphone.connect("notify::is-muted", lambda *_: self.toggle("microphone"))
		audio.microphone.connect("notify::volume", lambda *_: self.toggle("microphone"))
		backlight.connect("notify::brightness", lambda *_: self.toggle("brightness"))

	def toggle(self, osd: str):
		self.set_child(self.osds[osd])
		self.visible = True
		self.__hide()
		# print("yes", osd)
	
	@utils.debounce(3000)
	def __hide(self) -> None:
		self.visible = False

	def genrateChild(self,
		callback: Callable[[widgets.Scale],None] | None,
		icon: str | widgets.Icon | Binding | None = None,
		value: int | Binding | None = None,
		widget: Any = None # pyright: ignore[reportAny, reportExplicitAny]
	):
		return widgets.Box(
			child = [
				widgets.Icon(
					css_classes = ["icon"],
					image = icon
				) if icon is not None else None,
				widgets.Scale(
					vertical=False,
					css_classes=["material-slider"],
					min=0,
					max=100,
					value=value,
					hexpand=True,
					on_change=callback,
				) if value is not None else None,
				widget
			]
		)

	def set_speaker_volume(self, value: widgets.Scale):
		self.toggle("speaker")
		audio.speaker.set_volume(value.value)

	def set_mic_volume(self, value: widgets.Scale):
		self.toggle("microphone")
		audio.microphone.set_volume(value.value)
	
	def set_brightness(self, value: widgets.Scale):
		self.toggle("brightness")
		backlight.set_brightness(backlight.max_brightness*value.value/100)
	
	def wow(self):
		print(dir(Gtk.IconTheme))
		print(Gtk.IconTheme.get_search_path)
	# def debug_brightness(self):
	# 	print("{ devices: [", *[f"device_name: {device.device_name}, max_brightness: {device.max_brightness}, brightness: {device.brightness}" for device in backlight.devices],"] }")
