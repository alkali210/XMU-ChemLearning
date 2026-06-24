# src/widgets/param_panel.py
from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QHBoxLayout,
)

from widgets.fluent_compat import DoubleSpinBox


class ParamPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("参数设置", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Voltage
        v_layout = QHBoxLayout()
        v_layout.addWidget(QLabel("电压 (V):"))
        self.spin_voltage = DoubleSpinBox()
        self.spin_voltage.setRange(1.23, 3.0)
        self.spin_voltage.setSingleStep(0.1)
        self.spin_voltage.setValue(2.0)
        v_layout.addWidget(self.spin_voltage)
        v_layout.addStretch()
        layout.addLayout(v_layout)

        # Current Density
        j_layout = QHBoxLayout()
        j_layout.addWidget(QLabel("电流密度 (A/cm²):"))
        self.spin_density = DoubleSpinBox()
        self.spin_density.setRange(0.0, 5.0)
        self.spin_density.setSingleStep(0.1)
        self.spin_density.setValue(1.0)
        j_layout.addWidget(self.spin_density)
        j_layout.addStretch()
        layout.addLayout(j_layout)

        # Temperature
        t_layout = QHBoxLayout()
        t_layout.addWidget(QLabel("温度 (°C):"))
        self.spin_temp = DoubleSpinBox()
        self.spin_temp.setRange(20.0, 90.0)
        self.spin_temp.setSingleStep(1.0)
        self.spin_temp.setValue(25.0)
        t_layout.addWidget(self.spin_temp)
        t_layout.addStretch()
        layout.addLayout(t_layout)

    def set_enabled(self, enabled: bool):
        self.spin_voltage.setEnabled(enabled)
        self.spin_density.setEnabled(enabled)
        self.spin_temp.setEnabled(enabled)
