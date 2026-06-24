# src/widgets/control_panel.py
from PySide6.QtWidgets import QGroupBox, QHBoxLayout
from PySide6.QtCore import Slot

from core.experiment import ExperimentController, ExperimentState
from widgets.fluent_compat import PushButton, PrimaryPushButton


class ControlPanel(QGroupBox):
    def __init__(self, controller: ExperimentController, parent=None):
        super().__init__("运行控制", parent)
        self.controller = controller
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QHBoxLayout(self)

        self.btn_start = PrimaryPushButton("启动")
        self.btn_pause = PushButton("暂停")
        self.btn_resume = PrimaryPushButton("继续")
        self.btn_stop = PushButton("停止")
        self.btn_reset = PushButton("重置")

        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_pause)
        layout.addWidget(self.btn_resume)
        layout.addWidget(self.btn_stop)
        layout.addWidget(self.btn_reset)

        self._update_buttons(ExperimentState.IDLE)

    def _connect_signals(self):
        self.btn_start.clicked.connect(self.controller.start)
        self.btn_pause.clicked.connect(self.controller.pause)
        self.btn_resume.clicked.connect(self.controller.resume)
        self.btn_stop.clicked.connect(self.controller.stop)
        self.btn_reset.clicked.connect(self.controller.reset)

        self.controller.stateChanged.connect(self._update_buttons)

    @Slot(ExperimentState)
    def _update_buttons(self, state: ExperimentState):
        self.btn_start.setEnabled(
            state in (ExperimentState.IDLE, ExperimentState.STOPPED)
        )
        self.btn_pause.setEnabled(state == ExperimentState.RUNNING)
        self.btn_resume.setEnabled(state == ExperimentState.PAUSED)
        self.btn_stop.setEnabled(
            state in (ExperimentState.RUNNING, ExperimentState.PAUSED)
        )
        self.btn_reset.setEnabled(
            state
            in (
                ExperimentState.STOPPED,
                ExperimentState.PAUSED,
                ExperimentState.RUNNING,
            )
        )
