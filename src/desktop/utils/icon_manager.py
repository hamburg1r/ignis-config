# src/desktop/utils/icon_manager.py
from desktop.options import settings
from typing import Literal

IconType = Literal["material", "fontawesome", "codicons", "image"]

def get_icon(icon_key: str, icon_type: IconType | None = None) -> str:
    """
    Retrieves the appropriate icon string based on the global icon theme
    or a specified icon type.

    Args:
        icon_key: The key for the desired icon (e.g., "blinker_start", "blinker_stop").
        icon_type: Optional. If provided, overrides the global icon theme.

    Returns:
        The icon string (e.g., a Unicode character or a GTK symbolic icon name).
    """
    if icon_type is None:
        icon_type = settings.icons.icon_theme

    # Dynamically get the icon dictionary for the given key (e.g., settings.icons.blinker_start)
    icon_map: dict[str, str] = getattr(settings.icons, icon_key, {})

    return icon_map.get(icon_type, "")
