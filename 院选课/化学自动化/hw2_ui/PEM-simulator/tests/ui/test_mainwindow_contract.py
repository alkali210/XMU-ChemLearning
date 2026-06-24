import os
import sys

sys.path.insert(0, os.path.abspath("src"))

import pytest
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout

from core.experiment import ExperimentState
from main_window import MainWindow
from widgets.control_panel import ControlPanel
from widgets.info_panel import InfoPanel
from widgets.monitor_panel import MonitorPanel
from widgets.param_panel import ParamPanel
from widgets.result_panel import ResultPanel


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


@pytest.fixture
def main_window(qapp):
    window = MainWindow()
    return window


def test_mainwindow_layout_contract_structure_and_stretch(main_window):
    central = main_window.centralWidget()
    assert central is not None

    main_layout = central.layout()
    assert isinstance(main_layout, QHBoxLayout)
    assert main_layout.count() == 2

    left_item = main_layout.itemAt(0)
    right_item = main_layout.itemAt(1)

    left_layout = left_item.layout()
    right_layout = right_item.layout()

    assert isinstance(left_layout, QVBoxLayout)
    assert isinstance(right_layout, QVBoxLayout)

    # Left column order: Info -> Param -> Control -> Result
    assert left_layout.itemAt(0).widget() is main_window.info_panel
    assert left_layout.itemAt(1).widget() is main_window.param_panel
    assert left_layout.itemAt(2).widget() is main_window.control_panel
    assert left_layout.itemAt(3).widget() is main_window.result_panel

    # Right column contains Monitor panel
    assert right_layout.itemAt(0).widget() is main_window.monitor_panel

    # Main split ratio contract remains 1:3
    assert main_layout.stretch(0) == 1
    assert main_layout.stretch(1) == 3


def test_mainwindow_panel_instance_contract(main_window):
    assert isinstance(main_window.info_panel, InfoPanel)
    assert isinstance(main_window.param_panel, ParamPanel)
    assert isinstance(main_window.control_panel, ControlPanel)
    assert isinstance(main_window.result_panel, ResultPanel)
    assert isinstance(main_window.monitor_panel, MonitorPanel)


def test_mainwindow_running_reads_param_spin_contract(main_window):
    captured = {}

    def capture_parameters(v, j, t):
        captured["v"] = v
        captured["j"] = j
        captured["t"] = t

    main_window.simulator.set_parameters = capture_parameters

    main_window.param_panel.spin_voltage.setValue(2.2)
    main_window.param_panel.spin_density.setValue(1.7)
    main_window.param_panel.spin_temp.setValue(66.0)

    main_window._on_state_changed(ExperimentState.RUNNING)

    assert captured == {"v": 2.2, "j": 1.7, "t": 66.0}


def test_mainwindow_reset_clears_monitor_and_result_contract(main_window):
    # Populate monitor and result with non-default state
    main_window.monitor_panel.update_data(1.85, 2.5, 55.0)
    main_window.result_panel.update_results(1.85, 2.5)
    main_window.info_panel.update_time(3.4)

    assert len(main_window.monitor_panel.history_i) > 0
    assert len(main_window.monitor_panel.history_v) > 0
    assert main_window.result_panel.max_i > 0.0
    assert main_window.result_panel.max_v > 0.0

    # IDLE state in MainWindow performs reset flow
    main_window._on_state_changed(ExperimentState.IDLE)

    assert main_window.monitor_panel.history_i == []
    assert main_window.monitor_panel.history_v == []
    assert main_window.monitor_panel.lbl_v.text() == "电压: 0.000 V"
    assert main_window.monitor_panel.lbl_i.text() == "电流: 0.000 A"

    assert main_window.result_panel.max_i == 0.0
    assert main_window.result_panel.max_v == 0.0
    assert main_window.result_panel.lbl_power.text() == "0.000 W"
    assert main_window.result_panel.lbl_efficiency.text() == "0.00 %"
    assert (
        main_window.result_panel.lbl_summary.text()
        == "汇总:\n  最大电流: 0.000 A\n  最大电压: 0.000 V"
    )
    assert main_window.info_panel.lbl_time.text() == "0.0 s"
