# src/widgets/monitor_panel.py
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Slot
import pyqtgraph as pg
import datetime

from .fluent_compat import (
    CardWidget,
    SubtitleLabel,
    StrongBodyLabel,
    TextEdit,
    isDarkTheme,
)


class MonitorPanel(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Data history for plotting
        self.history_v = []
        self.history_i = []

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Title
        self.title_lbl = SubtitleLabel("过程监视")
        layout.addWidget(self.title_lbl)

        # Real-time values
        val_layout = QHBoxLayout()
        self.lbl_v = StrongBodyLabel("电压: 0.000 V")
        self.lbl_i = StrongBodyLabel("电流: 0.000 A")
        self.lbl_t = StrongBodyLabel("温度: 25.0 °C")

        for lbl in (self.lbl_v, self.lbl_i, self.lbl_t):
            font = lbl.font()
            font.setFamily("monospace")
            lbl.setFont(font)
            val_layout.addWidget(lbl)

        layout.addLayout(val_layout)

        # Plot
        self.plot_widget = pg.PlotWidget(title="V-I 极化曲线")
        self.plot_widget.setLabel("left", "电压", units="V")
        self.plot_widget.setLabel("bottom", "电流", units="A")
        self.plot_widget.showGrid(x=True, y=True)

        self._apply_theme_to_plot()

        # Setup curve
        self.curve = self.plot_widget.plot(
            pen=pg.mkPen("b", width=2), symbol="o", symbolSize=5, symbolBrush="b"
        )
        layout.addWidget(self.plot_widget, stretch=2)

        # Log output
        self.log_text = TextEdit()
        self.log_text.setReadOnly(True)

        log_font = self.log_text.font()
        log_font.setFamily("monospace")
        log_font.setPointSize(10)
        self.log_text.setFont(log_font)

        layout.addWidget(self.log_text, stretch=1)

        self.log_message("系统初始化完成。")

    def _apply_theme_to_plot(self):
        if isDarkTheme():
            self.plot_widget.setBackground("#272727")
            # Set grid and axis colors for dark mode
            axis_pen = pg.mkPen("#E0E0E0")
            title_color = "#E0E0E0"
        else:
            self.plot_widget.setBackground("w")
            # Set grid and axis colors for light mode
            axis_pen = pg.mkPen("#000000")
            title_color = "#000000"

        # Update title color
        if self.plot_widget.plotItem.titleLabel.text:
            self.plot_widget.setTitle(
                self.plot_widget.plotItem.titleLabel.text, color=title_color
            )

        # Update axes
        for axis_name in ["left", "bottom", "right", "top"]:
            axis = self.plot_widget.getAxis(axis_name)
            axis.setPen(axis_pen)
            axis.setTextPen(axis_pen)
            # Update grid lines via axis
            axis.setGrid(axis.grid)

            # Use undocumented internal property or recreate labels with correct color
            # Alternatively, we can just let PyQtGraph handle labels, or set CSS
            label_style = {"color": title_color}
            axis.setLabel(axis.labelText, units=axis.labelUnits, **label_style)

    def log_message(self, msg: str):
        time_str = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.log_text.append(f"[{time_str}] {msg}")
        # Scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    @Slot(float, float, float)
    def update_data(self, v: float, i: float, temp: float):
        self.lbl_v.setText(f"电压: {v:.3f} V")
        self.lbl_i.setText(f"电流: {i:.3f} A")
        self.lbl_t.setText(f"温度: {temp:.1f} °C")

        self.history_v.append(v)
        self.history_i.append(i)

        # Sort data for proper V-I plotting
        # Normally V-I curve sorts by current
        sorted_pairs = sorted(zip(self.history_i, self.history_v))
        sorted_i = [p[0] for p in sorted_pairs]
        sorted_v = [p[1] for p in sorted_pairs]

        self.curve.setData(sorted_i, sorted_v)

    def reset(self):
        self.history_v.clear()
        self.history_i.clear()
        self.curve.setData([], [])
        self.lbl_v.setText("电压: 0.000 V")
        self.lbl_i.setText("电流: 0.000 A")
        self.lbl_t.setText("温度: 25.0 °C")
        self.log_message("监视器重置。")
