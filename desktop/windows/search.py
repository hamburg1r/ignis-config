from ignis.utils import open_inspector
from ignis.widgets import Box, Button, Entry, EventBox, Label, Overlay, Window
from ignis.window_manager import WindowManager

window_manager = WindowManager.get_default()

class SearchList(Window):
	def __init__(self):
		self._child: Box = Box(
			vertical = True,
			# vexpand = False,
			# hexpand = False,
            valign="start",
            halign="center",
			child = [
				Entry(
					placeholder_text="Search..."
				),
				Label(label="Oh wow")
			]
		)
		super().__init__(
			namespace="search",
			css_classes=["border"],
			anchor=["left", "right", "top", "bottom"],
			kb_mode="on_demand",
			layer="bottom",
			child=Overlay(
				# css_classes=["unset"],
				child=Button(
					css_classes=["unset"],
					vexpand=True,
					hexpand=True,
					can_focus=False,
					on_click=lambda x: window_manager.close_window("search")
				),
				overlays=[self._child],
			),
		)
		# open_inspector()
