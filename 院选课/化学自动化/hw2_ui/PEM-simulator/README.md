# PEM Water Electrolysis Experiment GUI

This repository contains a PySide6-based application for simulating PEM (Proton Exchange Membrane) water electrolysis experiments. It provides a user-friendly interface for parameter control, real-time data monitoring, and automated result analysis.

## Project Overview

The application simulates standard PEM electrochemical losses, including:
- Theoretical and thermoneutral voltage calculations.
- Activation, ohmic, and mass transport losses.
- Real-time efficiency and power consumption monitoring.

![img](screenshot.png)

![img](screenshot_dark.png)

## Getting Started

### Prerequisites

- Python 3.11 or higher.

### Installation

Install the required dependencies using pip:

```bash
pip install PySide6 pyqtgraph numpy
```

### Running the Application

Launch the GUI with the following command:

```bash
python src/main.py
```

## Development and Quality Assurance

### Testing

Install the required dependencies for testing:

```bash
pip install pytest mypy ruff
```

Run all unit tests to ensure system stability:

```bash
python -m pytest tests/ -v
```

To run only UI tests:

```bash
python -m pytest tests/ui -q
```

### Static Analysis

Ensure code quality with type checking and linting:

```bash
# Type checking
python -m mypy src/ --ignore-missing-imports

# Linting
python -m ruff check src/
```

## Project Structure

- `src/`: Core application logic and UI components.
  - `core/`: Simulation and state machine logic.
  - `widgets/`: Modular UI component implementations.
- `tests/`: Unit and integration test suites.
- `scripts/`: Utility scripts for development and automation.

## UML Class Diagram

The following diagram summarizes the class relationships inside `src/`.

```mermaid
classDiagram
direction LR

class ExperimentState {
  <<enumeration>>
  IDLE
  RUNNING
  PAUSED
  STOPPED
}

class ExperimentController {
  <<QObject>>
  +stateChanged: Signal(ExperimentState)
  -_state: ExperimentState
  +state: ExperimentState
  +start() bool
  +pause() bool
  +resume() bool
  +stop() bool
  +reset() bool
  -_set_state(new_state: ExperimentState) void
}

class PEMSimulator {
  <<QObject>>
  +data_updated: Signal(float,float,float)
  +finished: Signal()
  +controller: ExperimentController
  +timer: QTimer
  +time_elapsed: float
  +current_time_ms: float
  +max_time_ms: float
  +update_interval: int
  +set_temperature: float
  +target_voltage: float
  +target_current_density: float
  +reset() void
  +set_parameters(voltage: float, density: float, temp: float) void
  +start_simulation() void
  +pause_simulation() void
  -_on_state_changed(state: ExperimentState) void
  -_step() void
}

class MainWindow {
  <<QMainWindow>>
  +controller: ExperimentController
  +simulator: PEMSimulator
  +info_panel: InfoPanel
  +param_panel: ParamPanel
  +control_panel: ControlPanel
  +result_panel: ResultPanel
  +monitor_panel: MonitorPanel
  -_setup_ui() void
  -_connect_signals() void
  -_on_state_changed(state: ExperimentState) void
  -_read_parameters() tuple
  -_on_data_updated(time_s: float, current: float, voltage: float) void
}

class CardWidget {
  <<UI Base>>
}

class InfoPanel {
  +update_state(state: ExperimentState) void
  +update_time(time_s: float) void
}

class ParamPanel {
  +spin_voltage: DoubleSpinBox
  +spin_density: DoubleSpinBox
  +spin_temp: DoubleSpinBox
  +set_enabled(enabled: bool) void
}

class ControlPanel {
  +controller: ExperimentController
  -_setup_ui() void
  -_connect_signals() void
  -_update_buttons(state: ExperimentState) void
}

class MonitorPanel {
  +history_v: list
  +history_i: list
  +log_message(msg: str) void
  +update_data(v: float, i: float, temp: float) void
  +reset() void
}

class ResultPanel {
  +max_i: float
  +max_v: float
  +update_results(v: float, i: float) void
  +reset() void
}

CardWidget <|-- InfoPanel
CardWidget <|-- MonitorPanel
CardWidget <|-- ResultPanel

MainWindow *-- ExperimentController
MainWindow *-- PEMSimulator
MainWindow *-- InfoPanel
MainWindow *-- ParamPanel
MainWindow *-- ControlPanel
MainWindow *-- ResultPanel
MainWindow *-- MonitorPanel

ControlPanel --> ExperimentController : invokes start/pause/resume/stop/reset
PEMSimulator --> ExperimentController : listens stateChanged
InfoPanel --> ExperimentState : display mapping
ControlPanel --> ExperimentState : button rules
ExperimentController --> ExperimentState : manages
MainWindow ..> ExperimentState : reacts to state
MainWindow ..> PEMSimulator : set_parameters()
PEMSimulator ..> MainWindow : data_updated/finished
MainWindow ..> InfoPanel : update_time/update_state
MainWindow ..> MonitorPanel : update_data/log_message
MainWindow ..> ResultPanel : update_results/reset
MainWindow ..> ParamPanel : read values / enable-disable
```
