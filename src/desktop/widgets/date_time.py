from typing import Literal
from datetime import datetime
from ignis.widgets import Button, Label, Icon, Box
from ignis.utils import Poll
from ignis.services.upower.service import UPowerService

from desktop.options import Settings

options = Settings()
upower = UPowerService.get_default()

class DateTime(Button):
	def __init__(self, orientation: Literal["horizontal", "vertical"] = "horizontal"):
		super().__init__(
			css_classes = ['date-time']
		)
		self.orientation = orientation

		self._icon = Icon(
			css_classes = ['icon'],
			image = options.date_time.icon_name
		)
		self._label = Label(
			css_classes = ['label'],
			label = ""
		)

		self._box = Box(
			child = [self._icon, self._label],
			vertical = orientation == "vertical"
		)
		self.set_child(self._box)

		Poll(
			options.date_time.polling_time,
			self.update,
	   )

	def _get_battery_text(self) -> str:
		if not options.battery.show_battery:
			return ""

		if not upower.is_available or not upower.display_device:
			return ""

		percent = int(upower.display_device.percent)
		return options.battery.format_string.format(percent=percent)

	def update(self, object):
		display_mode = options.date_time.display_mode
		icon_name = options.date_time.icon_name

		# Update icon visibility
		if display_mode == "icon_only" or display_mode == "icon_and_text":
			self._icon.set_visible(True)
			self._icon.image = icon_name
		else:
			self._icon.set_visible(False)

		# Update label visibility and content
		if display_mode == "text_only" or display_mode == "icon_and_text":
			self._label.set_visible(True)
			if self.orientation == "vertical":
				time_format = options.date_time.vertical_format
			else:
				time_format = options.date_time.horizontal_format
			
			time_text = datetime.now().strftime(time_format)
			battery_text = self._get_battery_text()

			if battery_text:
				self._label.label = f"{time_text} {battery_text}" # Combine time and battery text
			else:
				self._label.label = time_text
		else:
			self._label.set_visible(False)

		self.tooltip_text = datetime.now().strftime(options.date_time.tooltip_format)

