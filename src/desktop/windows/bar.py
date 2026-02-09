from typing import Literal
from ignis.widgets import Box, Button, CenterBox, Icon, Label, Window
from ignis.services.fetch import FetchService

from desktop.options import Settings
from desktop.widgets.apps import Apps
from desktop.widgets.battery import Battery, DeviceBattery
from desktop.widgets.date_time import DateTime
from desktop.widgets.tray import Tray

options = Settings()

class Bar(Window):
	def __init__(
		self,
		monitor: int,
	):
		anchor: list[str]
		fetch = FetchService.get_default()

		if options.bar.direction == 'horizontal':
			anchor = ['left', options.bar.side, 'right',]
		else:
			anchor = ['top', options.bar.side, 'bottom',]

		applauncher = Button(
			child = Icon(
				image = fetch.os_logo
			)
		)

		start_children = Box(
			child = [applauncher]
		)

		center_children = Box(
			child = [Apps(),]
		)

		end_children = Box(
			orientation = options.bar.direction,
			child = [
				Tray(direction = options.bar.direction),
				Battery(),
				DateTime(orientation = options.bar.direction),
			]
		)

		super().__init__(
			visible = True,
			namespace = f'{options.bar.direction}-bar',
			monitor = monitor,
			anchor = anchor,
			exclusivity = "exclusive",
			layer = "top",
			child = CenterBox(
				start_widget = start_children,
				center_widget = center_children,
				end_widget = end_children,
				orientation = options.bar.direction,
			)
		)
