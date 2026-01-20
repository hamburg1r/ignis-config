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

	class Bar(OptionsGroup):
		direction: Literal['vertical', 'horizontal'] = 'horizontal'
		side: str = 'top'

	class DateTime(OptionsGroup):
		format: str = '%I:%M %p'
		tooltip_format = '%c'
		polling_time: int = 1000

	class Battery(OptionsGroup):
		max: int = 60

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

settins = Settings()
