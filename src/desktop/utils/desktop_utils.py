from ignis.window_manager import WindowManager
from ignis.exceptions import WindowNotFoundError
from ignis.command_manager import CommandManager
from desktop.windows.settings import SettingsWindow

window_manager = WindowManager.get_default()
command_manager = CommandManager.get_default()

_launcher = None
_search_list = None
_settings_window = None# removed

@command_manager.command("settings")
def toggle_settigs():
    """
    Gets the SettingsWindow instance, creating it if it doesn't exist,
    and then toggles its visibility.
    """
    try:
        window = window_manager.get_window("settings")
    except WindowNotFoundError:
        _settings_window = SettingsWindow()
    finally:
        window_manager.toggle_window("settings")

def toggle_launcher():
    """
    Gets the Launcher instance, creating it if it doesn't exist,
    and then toggles its visibility.
    """
    global _launcher
    if _launcher is None:
        from desktop.windows.launcher import Launcher
        _launcher = Launcher()
    window_manager.toggle_window("Launcher")


def toggle_search_list():
    """
    Gets the SearchList instance, creating it if it doesn't exist,
    and then toggles its visibility.
    """
    global _search_list
    if _search_list is None:
        from desktop.windows.search import SearchList
        _search_list = SearchList()
    window_manager.toggle_window("search")
