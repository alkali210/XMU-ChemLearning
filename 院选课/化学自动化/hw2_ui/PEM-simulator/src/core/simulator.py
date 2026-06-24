# src/core/simulator.py
import numpy as np
from PySide6.QtCore import QObject, Signal, QTimer

from core.experiment import ExperimentController, ExperimentState
from utils.constants import THEORETICAL_VOLTAGE, MEMBRANE_AREA


class PEMSimulator(QObject):
    data_updated = Signal(float, float, float)  # time_s, current, voltage
    finished = Signal()

    def __init__(self, controller: ExperimentController) -> None:
        super().__init__()
        self.controller = controller
        self.controller.stateChanged.connect(self._on_state_changed)

        self.timer = QTimer()
        self.timer.timeout.connect(self._step)

        # Base experimental data
        self.i_points = np.array([0.0, 0.1, 0.2, 0.5, 1.0, 4.0, 6.0, 8.0])
        self.v_points = np.array(
            [THEORETICAL_VOLTAGE, 1.48, 1.50, 1.54, 1.58, 1.81, 2.07, 2.31]
        )

        self.reset()

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.current_time_ms = 0.0
        self.max_time_ms = 7000.0  # Total simulation time 7 seconds
        self.update_interval = 100  # ms

        # User parameters
        self.set_temperature = 25.0
        self.target_voltage = 2.0
        self.target_current_density = 2.0

    def set_parameters(self, voltage: float, density: float, temp: float) -> None:
        self.target_voltage = voltage
        self.target_current_density = density
        self.set_temperature = temp

    def start_simulation(self) -> None:
        self.timer.start(self.update_interval)

    def pause_simulation(self) -> None:
        self.timer.stop()

    def _on_state_changed(self, state: ExperimentState) -> None:
        if state == ExperimentState.RUNNING:
            self.start_simulation()
        elif state == ExperimentState.PAUSED:
            self.pause_simulation()
        elif state == ExperimentState.STOPPED:
            self.pause_simulation()
        elif state == ExperimentState.IDLE:
            self.pause_simulation()
            self.reset()

    def _step(self) -> None:
        self.current_time_ms += self.update_interval
        self.time_elapsed = self.current_time_ms / 1000.0

        if self.current_time_ms >= self.max_time_ms:
            self.controller.stop()
            self.finished.emit()
            return

        # Calculate interpolated values based on progress
        progress = self.current_time_ms / self.max_time_ms
        current_idx = progress * (len(self.i_points) - 1)

        idx = int(current_idx)
        if idx >= len(self.i_points) - 1:
            idx = len(self.i_points) - 2

        fraction = current_idx - idx

        # Linear interpolation
        i_val = (
            self.i_points[idx]
            + (self.i_points[idx + 1] - self.i_points[idx]) * fraction
        )
        v_val = (
            self.v_points[idx]
            + (self.v_points[idx + 1] - self.v_points[idx]) * fraction
        )

        # Apply parameter scaling
        target_max_i = self.target_current_density * MEMBRANE_AREA
        i_scale = target_max_i / 8.0 if 8.0 > 0 else 1.0
        i_val = i_val * i_scale

        v_scale = (
            (self.target_voltage - THEORETICAL_VOLTAGE) / (2.31 - THEORETICAL_VOLTAGE)
            if 2.31 > THEORETICAL_VOLTAGE
            else 1.0
        )
        v_val = THEORETICAL_VOLTAGE + (v_val - THEORETICAL_VOLTAGE) * v_scale

        # Temperature effect: higher temp lowers overpotential (approx 0.2% per degree above 25)
        temp_effect = 1.0 - (self.set_temperature - 25.0) * 0.002
        v_val = THEORETICAL_VOLTAGE + (v_val - THEORETICAL_VOLTAGE) * temp_effect

        # Add a tiny bit of noise for realism
        i_noise = np.random.normal(0, 0.005)
        v_noise = np.random.normal(0, 0.002)

        final_i = max(0.0, i_val + i_noise)
        final_v = max(THEORETICAL_VOLTAGE, v_val + v_noise)

        self.data_updated.emit(self.time_elapsed, final_i, final_v)
