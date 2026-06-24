import sys
import os

sys.path.insert(0, os.path.abspath("src"))

import pytest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication
from widgets.monitor_panel import MonitorPanel


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_monitor_panel_update_contract(qapp):
    panel = MonitorPanel()

    # Check initial state
    assert len(panel.history_v) == 0
    assert len(panel.history_i) == 0
    assert panel.lbl_v.text() == "电压: 0.000 V"
    assert panel.lbl_i.text() == "电流: 0.000 A"
    assert panel.lbl_t.text() == "温度: 25.0 °C"

    # Call update_data
    panel.update_data(1.5, 0.5, 25.0)

    # Check updated state
    assert len(panel.history_v) == 1
    assert len(panel.history_i) == 1
    assert panel.history_v[0] == 1.5
    assert panel.history_i[0] == 0.5
    assert panel.lbl_v.text() == "电压: 1.500 V"
    assert panel.lbl_i.text() == "电流: 0.500 A"
    assert panel.lbl_t.text() == "温度: 25.0 °C"

    # Check that curve was updated (Curve should have 1 point)
    x_data, y_data = panel.curve.getData()
    assert list(x_data) == [0.5]
    assert list(y_data) == [1.5]


def test_monitor_panel_reset_contract(qapp):
    panel = MonitorPanel()

    # Add some data
    panel.update_data(1.5, 0.5, 55.0)
    assert len(panel.history_v) == 1
    assert panel.lbl_t.text() == "温度: 55.0 °C"

    # Call reset
    panel.reset()

    # Verify everything is cleared
    assert len(panel.history_v) == 0
    assert len(panel.history_i) == 0
    assert panel.lbl_v.text() == "电压: 0.000 V"
    assert panel.lbl_i.text() == "电流: 0.000 A"
    assert panel.lbl_t.text() == "温度: 25.0 °C"

    x_data, y_data = panel.curve.getData()
    # It might be None if empty, or an empty list/array
    if x_data is not None:
        assert len(x_data) == 0


@patch("widgets.monitor_panel.isDarkTheme")
def test_monitor_panel_theme_readability_dark(mock_isDarkTheme, qapp):
    mock_isDarkTheme.return_value = True
    panel = MonitorPanel()

    # Check that background is not white (dark theme applies a dark color)
    bg_brush = panel.plot_widget.backgroundBrush()
    color = bg_brush.color()
    # Verify dark theme applies a dark background (not white)
    assert color.name().lower() != "#ffffff"


@patch("widgets.monitor_panel.isDarkTheme")
def test_monitor_panel_theme_readability_light(mock_isDarkTheme, qapp):
    mock_isDarkTheme.return_value = False
    panel = MonitorPanel()

    # Check that background is white or light (light theme applies a light background)
    bg_brush = panel.plot_widget.backgroundBrush()
    color = bg_brush.color()
    # Verify light theme applies a light background (not dark)
    assert color.name().lower() != "#272727"
