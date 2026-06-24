from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Slot

from core.experiment import ExperimentState
from widgets.fluent_compat import (
    STATUS_COLORS,
    CardWidget,
    SubtitleLabel,
    BodyLabel,
    StrongBodyLabel,
    FLUENT_AVAILABLE,
)


class InfoPanel(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Title
        title_lbl = SubtitleLabel("实验信息")
        layout.addWidget(title_lbl)

        # Row 1: Experiment Name
        name_layout = QHBoxLayout()
        lbl_name_title = BodyLabel("实验名称:")
        name_layout.addWidget(lbl_name_title)
        self.lbl_name = StrongBodyLabel("PEM 电解水实验")
        if not FLUENT_AVAILABLE:
            self.lbl_name.setStyleSheet("font-weight: bold;")
        name_layout.addWidget(self.lbl_name)
        name_layout.addStretch()
        layout.addLayout(name_layout)

        # Row 2: State
        state_layout = QHBoxLayout()
        lbl_state_title = BodyLabel("当前状态:")
        state_layout.addWidget(lbl_state_title)
        self.lbl_state = StrongBodyLabel("未启动")

        # initial color
        color = STATUS_COLORS.get("IDLE", "gray")
        if FLUENT_AVAILABLE:
            self.lbl_state.setStyleSheet(f"color: {color};")
        else:
            self.lbl_state.setStyleSheet(f"color: {color}; font-weight: bold;")

        state_layout.addWidget(self.lbl_state)
        state_layout.addStretch()
        layout.addLayout(state_layout)

        # Row 3: Running Time
        time_layout = QHBoxLayout()
        lbl_time_title = BodyLabel("运行时间:")
        time_layout.addWidget(lbl_time_title)
        self.lbl_time = BodyLabel("0.0 s")

        font = self.lbl_time.font()
        font.setFamily("monospace")
        self.lbl_time.setFont(font)

        time_layout.addWidget(self.lbl_time)
        time_layout.addStretch()
        layout.addLayout(time_layout)

    @Slot(ExperimentState)
    def update_state(self, state: ExperimentState):
        state_map = {
            ExperimentState.IDLE: ("未启动", STATUS_COLORS.get("IDLE", "gray")),
            ExperimentState.RUNNING: ("运行中", STATUS_COLORS.get("RUNNING", "green")),
            ExperimentState.PAUSED: ("暂停", STATUS_COLORS.get("PAUSED", "orange")),
            ExperimentState.STOPPED: ("结束", STATUS_COLORS.get("STOPPED", "red")),
        }
        text, color = state_map[state]
        self.lbl_state.setText(text)
        if FLUENT_AVAILABLE:
            self.lbl_state.setStyleSheet(f"color: {color};")
        else:
            self.lbl_state.setStyleSheet(f"color: {color}; font-weight: bold;")

    @Slot(float)
    def update_time(self, time_s: float):
        self.lbl_time.setText(f"{time_s:.1f} s")
