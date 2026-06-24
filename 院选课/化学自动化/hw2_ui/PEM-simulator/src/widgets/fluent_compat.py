"""Compatibility helpers for optional qfluentwidgets integration.

This module centralizes Fluent UI imports so other modules can depend on a
stable API, even when ``qfluentwidgets`` is unavailable in the environment.
"""

from __future__ import annotations

from enum import Enum
from typing import Final

from PySide6.QtWidgets import QApplication, QDoubleSpinBox


class _FallbackTheme(Enum):
    """Fallback Theme enum used when qfluentwidgets is not installed."""

    LIGHT = "Light"
    DARK = "Dark"
    AUTO = "Auto"


try:
    from qfluentwidgets import Theme as _QFluentTheme
    from qfluentwidgets import setTheme as _qfluent_set_theme
    from qfluentwidgets import DoubleSpinBox as _DoubleSpinBox
    from qfluentwidgets import PushButton as _PushButton
    from qfluentwidgets import PrimaryPushButton as _PrimaryPushButton
    from qfluentwidgets import CardWidget as _CardWidget
    from qfluentwidgets import SubtitleLabel as _SubtitleLabel
    from qfluentwidgets import BodyLabel as _BodyLabel
    from qfluentwidgets import CaptionLabel as _CaptionLabel
    from qfluentwidgets import StrongBodyLabel as _StrongBodyLabel
    from qfluentwidgets import isDarkTheme as _isDarkTheme
    from qfluentwidgets import TextEdit as _TextEdit

    Theme = _QFluentTheme
    DoubleSpinBox = _DoubleSpinBox
    PushButton = _PushButton
    PrimaryPushButton = _PrimaryPushButton
    CardWidget = _CardWidget
    SubtitleLabel = _SubtitleLabel
    BodyLabel = _BodyLabel
    CaptionLabel = _CaptionLabel
    StrongBodyLabel = _StrongBodyLabel
    TextEdit = _TextEdit
    isDarkTheme = _isDarkTheme
    _fluent_available = True
    _fluent_import_error: str | None = None
except Exception as exc:  # pragma: no cover - defensive import path
    Theme = _FallbackTheme
    _qfluent_set_theme = None
    DoubleSpinBox = QDoubleSpinBox
    from PySide6.QtWidgets import QPushButton, QFrame, QLabel, QTextEdit

    PushButton = QPushButton
    PrimaryPushButton = QPushButton
    CardWidget = QFrame
    SubtitleLabel = QLabel
    BodyLabel = QLabel
    CaptionLabel = QLabel
    StrongBodyLabel = QLabel
    TextEdit = QTextEdit

    def isDarkTheme() -> bool:
        return False

    _fluent_available = False
    _fluent_import_error = str(exc)


STATUS_COLORS: Final[dict[str, str]] = {
    "IDLE": "#808080",
    "RUNNING": "#2e7d32",
    "PAUSED": "#f39c12",
    "STOPPED": "#c62828",
}
"""Centralized color tokens for experiment status labels."""

METRIC_COLORS: Final[dict[str, str]] = {
    "POWER": "#d35400",
    "EFFICIENCY": "#27ae60",
}
"""Centralized color tokens for key metric emphasis."""

FLUENT_AVAILABLE: Final[bool] = _fluent_available
FLUENT_IMPORT_ERROR: Final[str | None] = _fluent_import_error


def apply_app_theme(app: QApplication, theme: object = Theme.AUTO) -> bool:
    """Apply Fluent application theme when available.

    Args:
        app: The active Qt application instance.
        theme: Fluent theme value. Defaults to ``Theme.AUTO``.

    Returns:
        ``True`` if Fluent theme was applied successfully, otherwise ``False``.

    Notes:
        When qfluentwidgets is not available, this function does not raise and
        falls back to Qt Fusion style to keep startup behavior predictable.
    """

    if FLUENT_AVAILABLE and _qfluent_set_theme is not None:
        _qfluent_set_theme(theme)
        return True

    app.setStyle("Fusion")
    return False
