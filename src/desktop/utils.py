from ignis.window_manager import WindowManager

window_manager = WindowManager.get_default()

_launcher = None
_search_list = None

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
