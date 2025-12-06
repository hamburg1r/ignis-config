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
			anchor = ['left', options.bar.side, 'right',]

		print(fetch.os_logo_dark)
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
			child = [
				Tray(),
				Battery(),
				# DeviceBattery(),
				DateTime(),
			]
		)

		super().__init__(
			visible = True,
			namespace = f'{options.bar.direction}-bar',
			monitor = monitor,
			anchor = anchor,
			exclusivity = "exclusive",
			layer = "top",
			# kb_mode: str = "none",
			# popup: bool = False,
			# margin_bottom: int = 0,
			# margin_left: int = 0,
			# margin_right: int = 0,
			# margin_top: int = 0,
			# dynamic_input_region: bool = False,
			child = CenterBox(
				start_widget = start_children,
				center_widget = center_children,
				end_widget = end_children,
			)
		)
