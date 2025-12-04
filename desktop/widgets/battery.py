from ignis import widgets
from ignis.widgets import Box, Label
from ignis.services.upower import UPowerService, UPowerDevice

from desktop.options import Settings

upower = UPowerService.get_default()
options = Settings()

class BatteryItem(widgets.Box):
	def __init__(self, device: UPowerDevice):
		super().__init__(
			css_classes=["battery-item"],
			setup=lambda self: device.connect("removed", lambda x: self.unparent()),
			child=[
				widgets.Icon(
					icon_name=device.bind("icon_name"), css_classes=["battery-icon"]
				),
				widgets.Label(
					label=device.bind("percent", lambda x: f"{int(x)}%"),
					css_classes=["battery-percent"],
				),
				# widgets.Scale(
				# 	min=0,
				# 	max=options.battery.max,
				# 	value=device.bind("percent"),
				# 	sensitive=False,
				# 	css_classes=["battery-scale"],
				# ),
			],
		)
		self.tooltip_text = device.bind('time_remaining', lambda v: str(v))


class Battery(widgets.Box):
	def __init__(self):
		super().__init__(
			setup=lambda self: upower.connect(
				"battery-added", lambda x, device: self.append(BatteryItem(device))
			),
		)

### UNDER CONSTRUCTION
class DeviceBattery(Box):
	def __init__(self):
		super().__init__()
		upower.connect('notify::display-device', self.bruh)
		self.append(Label(label='sex'))
	
	def bruh(self, **kwargs):
		print(kwargs)
