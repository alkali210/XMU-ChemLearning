import sys
import os

sys.path.insert(0, os.path.abspath("src"))

import pytest
from PySide6.QtWidgets import QApplication
from widgets.param_panel import ParamPanel


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


def test_param_panel_contract(qapp):
    """Test that ParamPanel preserves its public contract."""
    panel = ParamPanel()

    # Check attributes exist
    assert hasattr(panel, "spin_voltage")
    assert hasattr(panel, "spin_density")
    assert hasattr(panel, "spin_temp")

    # Check they act like spinboxes with expected ranges and defaults
    assert panel.spin_voltage.minimum() == 1.23
    assert panel.spin_voltage.maximum() == 3.0
    assert panel.spin_voltage.value() == 2.0
    assert panel.spin_voltage.singleStep() == 0.1

    assert panel.spin_density.minimum() == 0.0
    assert panel.spin_density.maximum() == 5.0
    assert panel.spin_density.value() == 1.0
    assert panel.spin_density.singleStep() == 0.1

    assert panel.spin_temp.minimum() == 20.0
    assert panel.spin_temp.maximum() == 90.0
    assert panel.spin_temp.value() == 25.0
    assert panel.spin_temp.singleStep() == 1.0


def test_param_panel_set_enabled(qapp):
    """Test that RUNNING-state lock behavior is identical."""
    panel = ParamPanel()

    # Should be enabled by default
    assert panel.spin_voltage.isEnabled() is True
    assert panel.spin_density.isEnabled() is True
    assert panel.spin_temp.isEnabled() is True

    # Disable them
    panel.set_enabled(False)
    assert panel.spin_voltage.isEnabled() is False
    assert panel.spin_density.isEnabled() is False
    assert panel.spin_temp.isEnabled() is False

    # Re-enable them
    panel.set_enabled(True)
    assert panel.spin_voltage.isEnabled() is True
    assert panel.spin_density.isEnabled() is True
    assert panel.spin_temp.isEnabled() is True


def test_param_panel_edge_cases(qapp):
    """Test edge case interactions with ParamPanel."""
    panel = ParamPanel()

    # Try setting value below minimum
    panel.spin_voltage.setValue(0.0)
    assert panel.spin_voltage.value() == 1.23

    # Try setting value above maximum
    panel.spin_density.setValue(10.0)
    assert panel.spin_density.value() == 5.0

    # Toggle enabled state rapidly
    panel.set_enabled(False)
    panel.set_enabled(True)
    panel.set_enabled(False)
    assert not panel.spin_voltage.isEnabled()
