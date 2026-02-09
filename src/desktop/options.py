import os
from pathlib import Path
from typing import Literal
from ignis.options_manager import OptionsManager, OptionsGroup

class Settings(OptionsManager):
	_file = os.path.expanduser('~/.config/ignis.conf')
	def __init__(self):
		os.makedirs(os.path.dirname(self._file), exist_ok=True)
		if not os.path.exists(self._file):
			with open(self._file, 'w') as f:
				_ = f.write('{}')
		super().__init__(file=self._file)

	def save_to_file(self):
		super().save_to_file(file=self._file)


	class Bar(OptionsGroup):
		direction: Literal['vertical', 'horizontal'] = 'vertical'
		side: Literal['left', 'right', 'top', 'bottom'] = 'left'

	class DateTime(OptionsGroup):
		horizontal_format: str = '%I:%M %p'
		vertical_format: str = '%I\n%M\n%p'
		tooltip_format = '%c'
		polling_time: int = 1000
		display_mode: Literal["icon_only", "text_only", "icon_and_text"] = "text_only"
		icon_name: str = "accessories-calculator-symbolic"

	class Battery(OptionsGroup):
		max: int = 60
		show_battery: bool = False
		format_string: str = "{percent}%"

	class User(OptionsGroup):

		class Colors(OptionsGroup):
			dark_mode: bool = True
			colors: dict[str, str] = {}

		terminal_command: str = "kitty %command%"
		colors: Colors = Colors()

	bar: Bar = Bar() # type: ignore[reportUnknownMemberType]
	date_time: DateTime = DateTime()
	battery: Battery = Battery()
	user: User = User()

settings = Settings()
