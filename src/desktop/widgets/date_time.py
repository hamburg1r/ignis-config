from datetime import datetime
from ignis.widgets import Button, Label
from ignis.utils import Poll

from desktop.options import Settings

options = Settings()

class DateTime(Button):
	def __init__(self):
		super().__init__(
			css_classes = ['date-time']
		)
		Poll(
			options.date_time.polling_time,
			self.update,
	   )

	def update(self, object):
		self.label = datetime.now().strftime(options.date_time.format)
		self.tooltip_text = datetime.now().strftime(options.date_time.tooltip_format)
