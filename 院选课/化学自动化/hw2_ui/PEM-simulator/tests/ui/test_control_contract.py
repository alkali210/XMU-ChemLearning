import sys
import os

sys.path.insert(0, os.path.abspath("src"))

import pytest
from PySide6.QtWidgets import QApplication
from core.experiment import ExperimentController, ExperimentState
from widgets.control_panel import ControlPanel


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


@pytest.fixture
def controller(qapp):
    ctrl = ExperimentController()
    return ctrl


@pytest.fixture
def control_panel(qapp, controller):
    panel = ControlPanel(controller)
    return panel


def test_control_happy_path(controller, control_panel):
    # Initial state (IDLE)
    assert controller.state == ExperimentState.IDLE
    assert control_panel.btn_start.isEnabled()
    assert not control_panel.btn_pause.isEnabled()
    assert not control_panel.btn_resume.isEnabled()
    assert not control_panel.btn_stop.isEnabled()
    assert not control_panel.btn_reset.isEnabled()

    # START
    control_panel.btn_start.click()
    assert controller.state == ExperimentState.RUNNING
    assert not control_panel.btn_start.isEnabled()
    assert control_panel.btn_pause.isEnabled()
    assert not control_panel.btn_resume.isEnabled()
    assert control_panel.btn_stop.isEnabled()
    assert control_panel.btn_reset.isEnabled()

    # PAUSE
    control_panel.btn_pause.click()
    assert controller.state == ExperimentState.PAUSED
    assert not control_panel.btn_start.isEnabled()
    assert not control_panel.btn_pause.isEnabled()
    assert control_panel.btn_resume.isEnabled()
    assert control_panel.btn_stop.isEnabled()
    assert control_panel.btn_reset.isEnabled()

    # RESUME
    control_panel.btn_resume.click()
    assert controller.state == ExperimentState.RUNNING
    assert not control_panel.btn_start.isEnabled()
    assert control_panel.btn_pause.isEnabled()
    assert not control_panel.btn_resume.isEnabled()
    assert control_panel.btn_stop.isEnabled()
    assert control_panel.btn_reset.isEnabled()

    # STOP
    control_panel.btn_stop.click()
    assert controller.state == ExperimentState.STOPPED
    assert control_panel.btn_start.isEnabled()
    assert not control_panel.btn_pause.isEnabled()
    assert not control_panel.btn_resume.isEnabled()
    assert not control_panel.btn_stop.isEnabled()
    assert control_panel.btn_reset.isEnabled()

    # RESET
    control_panel.btn_reset.click()
    assert controller.state == ExperimentState.IDLE
    assert control_panel.btn_start.isEnabled()
    assert not control_panel.btn_pause.isEnabled()
    assert not control_panel.btn_resume.isEnabled()
    assert not control_panel.btn_stop.isEnabled()
    assert not control_panel.btn_reset.isEnabled()


def test_control_edge_cases(controller, control_panel):
    # IDLE -> Pause (Invalid, should not change state or should be disabled)
    assert not control_panel.btn_pause.isEnabled()
    # Force click programmatically
    control_panel.controller.pause()
    assert (
        controller.state == ExperimentState.IDLE
    )  # Assuming experiment controller ignores invalid transitions

    # IDLE -> Resume
    assert not control_panel.btn_resume.isEnabled()
    control_panel.controller.resume()
    assert controller.state == ExperimentState.IDLE

    # RUNNING -> Resume
    control_panel.btn_start.click()
    assert controller.state == ExperimentState.RUNNING
    assert not control_panel.btn_resume.isEnabled()
    control_panel.controller.resume()
    assert controller.state == ExperimentState.RUNNING

    # IDLE -> Stop (from stopped state)
    control_panel.btn_stop.click()
    assert controller.state == ExperimentState.STOPPED
    # Try invalid action from STOPPED
    control_panel.controller.pause()
    assert controller.state == ExperimentState.STOPPED
    assert control_panel.btn_start.isEnabled()
    assert not control_panel.btn_pause.isEnabled()
    assert not control_panel.btn_resume.isEnabled()
    assert not control_panel.btn_stop.isEnabled()
    assert control_panel.btn_reset.isEnabled()

    # RESET
    control_panel.btn_reset.click()
    assert controller.state == ExperimentState.IDLE
    assert control_panel.btn_start.isEnabled()
    assert not control_panel.btn_pause.isEnabled()
    assert not control_panel.btn_resume.isEnabled()
    assert not control_panel.btn_stop.isEnabled()
    assert not control_panel.btn_reset.isEnabled()


def test_control_invalid_transition_sequence_does_not_corrupt_state_or_buttons(
    controller, control_panel
):
    def button_matrix() -> tuple[bool, bool, bool, bool, bool]:
        return (
            control_panel.btn_start.isEnabled(),
            control_panel.btn_pause.isEnabled(),
            control_panel.btn_resume.isEnabled(),
            control_panel.btn_stop.isEnabled(),
            control_panel.btn_reset.isEnabled(),
        )

    initial_matrix = button_matrix()

    # Explicit invalid sequence from IDLE should be rejected and keep contract stable.
    assert controller.state == ExperimentState.IDLE
    assert controller.pause() is False
    assert controller.resume() is False
    assert controller.stop() is False
    assert controller.reset() is False

    assert controller.state == ExperimentState.IDLE
    assert button_matrix() == initial_matrix
