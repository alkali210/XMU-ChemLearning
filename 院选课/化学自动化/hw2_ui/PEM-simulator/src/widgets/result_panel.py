# src/widgets/result_panel.py
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Slot

from utils.constants import THERMONEUTRAL_VOLTAGE
from widgets.fluent_compat import (
    CardWidget,
    SubtitleLabel,
    BodyLabel,
    StrongBodyLabel,
    METRIC_COLORS,
    FLUENT_AVAILABLE,
)


class ResultPanel(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Title
        self.lbl_title = SubtitleLabel("输出结果")
        layout.addWidget(self.lbl_title)

        # Power
        p_layout = QHBoxLayout()
        p_layout.addWidget(BodyLabel("瞬时功率 (P = V × I):"))
        self.lbl_power = StrongBodyLabel("0.000 W")
        color_power = METRIC_COLORS.get("POWER", "#d35400")
        if FLUENT_AVAILABLE:
            self.lbl_power.setStyleSheet(f"color: {color_power};")
        else:
            self.lbl_power.setStyleSheet(f"color: {color_power}; font-weight: bold;")
        p_layout.addWidget(self.lbl_power)
        p_layout.addStretch()
        layout.addLayout(p_layout)

        # Efficiency
        e_layout = QHBoxLayout()
        e_layout.addWidget(BodyLabel(f"电压效率 (η = {THERMONEUTRAL_VOLTAGE} / V):"))
        self.lbl_efficiency = StrongBodyLabel("0.00 %")
        color_eff = METRIC_COLORS.get("EFFICIENCY", "#27ae60")
        if FLUENT_AVAILABLE:
            self.lbl_efficiency.setStyleSheet(f"color: {color_eff};")
        else:
            self.lbl_efficiency.setStyleSheet(f"color: {color_eff}; font-weight: bold;")
        e_layout.addWidget(self.lbl_efficiency)
        e_layout.addStretch()
        layout.addLayout(e_layout)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Data summary
        self.lbl_summary = BodyLabel("汇总:\n  最大电流: 0.000 A\n  最大电压: 0.000 V")
        layout.addWidget(self.lbl_summary)

        self.max_i = 0.0
        self.max_v = 0.0

    @Slot(float, float)
    def update_results(self, v: float, i: float):
        if v <= 0:
            return

        # Power calculation
        power = v * i
        self.lbl_power.setText(f"{power:.3f} W")

        # Voltage efficiency (η = 1.481 / V)
        efficiency = (THERMONEUTRAL_VOLTAGE / v) * 100
        self.lbl_efficiency.setText(f"{efficiency:.2f} %")

        # Summary tracking
        if i > self.max_i:
            self.max_i = i
        if v > self.max_v:
            self.max_v = v

        self.lbl_summary.setText(
            f"汇总:\n  最大电流: {self.max_i:.3f} A\n  最大电压: {self.max_v:.3f} V"
        )

    def reset(self):
        self.max_i = 0.0
        self.max_v = 0.0
        self.lbl_power.setText("0.000 W")
        self.lbl_efficiency.setText("0.00 %")
        self.lbl_summary.setText("汇总:\n  最大电流: 0.000 A\n  最大电压: 0.000 V")
