# src/main_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

from core.experiment import ExperimentController, ExperimentState
from core.simulator import PEMSimulator

from widgets.info_panel import InfoPanel
from widgets.param_panel import ParamPanel
from widgets.control_panel import ControlPanel
from widgets.monitor_panel import MonitorPanel
from widgets.result_panel import ResultPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PEM 电解水实验系统")
        self.resize(1000, 700)

        # Core logic
        self.controller = ExperimentController()
        self.simulator = PEMSimulator(self.controller)

        # UI setup
        self._setup_ui()
        self._connect_signals()

        self.monitor_panel.log_message("欢迎使用 PEM 电解水实验仿真系统。")

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Left Panel
        left_layout = QVBoxLayout()

        self.info_panel = InfoPanel()
        left_layout.addWidget(self.info_panel)

        self.param_panel = ParamPanel()
        left_layout.addWidget(self.param_panel)

        self.control_panel = ControlPanel(self.controller)
        left_layout.addWidget(self.control_panel)

        self.result_panel = ResultPanel()
        left_layout.addWidget(self.result_panel)

        left_layout.addStretch()

        # Right Panel
        right_layout = QVBoxLayout()
        self.monitor_panel = MonitorPanel()
        right_layout.addWidget(self.monitor_panel)

        # Add to main
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=3)

    def _connect_signals(self):
        # Experiment state changes
        self.controller.stateChanged.connect(self.info_panel.update_state)
        self.controller.stateChanged.connect(self._on_state_changed)

        # Simulator data updates
        self.simulator.data_updated.connect(self._on_data_updated)
        self.simulator.finished.connect(
            lambda: self.monitor_panel.log_message("仿真测试完成。")
        )

    def _on_state_changed(self, state: ExperimentState):
        state_map = {
            ExperimentState.IDLE: "系统已重置，处于空闲状态。",
            ExperimentState.RUNNING: "实验运行中...",
            ExperimentState.PAUSED: "实验已暂停。",
            ExperimentState.STOPPED: "实验已停止。",
        }
        self.monitor_panel.log_message(state_map[state])

        if state == ExperimentState.RUNNING:
            v, j, t = self._read_parameters()
            self.simulator.set_parameters(v, j, t)

        # Disable params if running
        self.param_panel.set_enabled(
            state in (ExperimentState.IDLE, ExperimentState.STOPPED)
        )

        if state == ExperimentState.IDLE:
            self.monitor_panel.reset()
            self.result_panel.reset()
            self.info_panel.update_time(0.0)

    def _read_parameters(self) -> tuple[float, float, float]:
        """Read parameters via the public spin_* contract."""
        voltage = self.param_panel.spin_voltage.value()
        density = self.param_panel.spin_density.value()
        temperature = self.param_panel.spin_temp.value()
        return voltage, density, temperature

    def _on_data_updated(self, time_s: float, current: float, voltage: float):
        temp = self.param_panel.spin_temp.value()

        # Update Info
        self.info_panel.update_time(time_s)

        # Update Monitor
        self.monitor_panel.update_data(voltage, current, temp)

        # Update Results
        self.result_panel.update_results(voltage, current)
