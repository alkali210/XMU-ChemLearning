import sys
import os
import pytest
sys.path.insert(0, os.path.abspath("src"))

from PySide6.QtWidgets import QApplication
from widgets.result_panel import ResultPanel
from utils.constants import THERMONEUTRAL_VOLTAGE

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

@pytest.fixture
def result_panel(qapp):
    panel = ResultPanel()
    return panel

def test_result_panel_initial_state_contract(result_panel):
    assert result_panel.lbl_power.text() == "0.000 W"
    assert result_panel.lbl_efficiency.text() == "0.00 %"
    assert result_panel.max_i == 0.0
    assert result_panel.max_v == 0.0

def test_result_panel_happy_path_update_contract(result_panel):
    v = 2.0
    i = 1.5
    result_panel.update_results(v, i)
    
    expected_power = v * i
    expected_eff = (THERMONEUTRAL_VOLTAGE / v) * 100
    
    assert result_panel.lbl_power.text() == f"{expected_power:.3f} W"
    assert result_panel.lbl_efficiency.text() == f"{expected_eff:.2f} %"
    assert result_panel.max_v == 2.0
    assert result_panel.max_i == 1.5
    
    # Test tracking max
    result_panel.update_results(1.5, 2.5) # lower V, higher I
    assert result_panel.max_v == 2.0
    assert result_panel.max_i == 2.5

def test_result_panel_edge_case_zero_v_contract(result_panel):
    # if v <= 0, it should early return and not divide by zero
    result_panel.update_results(2.0, 1.5)
    result_panel.update_results(0.0, 0.0)
    
    # should not change from previous state
    assert result_panel.max_v == 2.0
    assert result_panel.max_i == 1.5
    assert result_panel.lbl_power.text() == "3.000 W"

def test_result_panel_reset_contract(result_panel):
    result_panel.update_results(2.0, 1.5)
    result_panel.reset()
    
    assert result_panel.lbl_power.text() == "0.000 W"
    assert result_panel.lbl_efficiency.text() == "0.00 %"
    assert result_panel.max_i == 0.0
    assert result_panel.max_v == 0.0
    assert "0.000" in result_panel.lbl_summary.text()
