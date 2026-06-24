import pytest
from PySide6.QtWidgets import QApplication
import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from widgets.info_panel import InfoPanel
from core.experiment import ExperimentState
from widgets.fluent_compat import STATUS_COLORS

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

def test_info_panel_state_mapping(qapp):
    panel = InfoPanel()
    
    panel.update_state(ExperimentState.IDLE)
    assert panel.lbl_state.text() == "未启动"
    assert STATUS_COLORS["IDLE"] in panel.lbl_state.styleSheet()

    panel.update_state(ExperimentState.RUNNING)
    assert panel.lbl_state.text() == "运行中"
    assert STATUS_COLORS["RUNNING"] in panel.lbl_state.styleSheet()

    panel.update_state(ExperimentState.PAUSED)
    assert panel.lbl_state.text() == "暂停"
    assert STATUS_COLORS["PAUSED"] in panel.lbl_state.styleSheet()

    panel.update_state(ExperimentState.STOPPED)
    assert panel.lbl_state.text() == "结束"
    assert STATUS_COLORS["STOPPED"] in panel.lbl_state.styleSheet()

def test_info_panel_time_format(qapp):
    panel = InfoPanel()
    panel.update_time(1.234)
    assert panel.lbl_time.text() == "1.2 s"

def test_info_panel_fluent_labels(qapp):
    panel = InfoPanel()
    # verify StrongBodyLabel or QLabel is used
    assert hasattr(panel, "lbl_state")
    assert hasattr(panel, "lbl_time")
    assert hasattr(panel, "lbl_name")

