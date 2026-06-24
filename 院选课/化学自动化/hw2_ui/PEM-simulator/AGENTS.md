# AGENTS.md - PEM Water Electrolysis Experiment GUI

## Project Overview
This repository contains a PySide6-based application for simulating PEM (Proton Exchange Membrane) water electrolysis experiments. The goal is to provide a user-friendly interface for parameter control, real-time data monitoring, and automated result analysis.

## Build / Run / Test Commands
```bash
# Install dependencies
pip install PySide6 pyqtgraph numpy pytest mypy ruff

# Run the GUI application
python src/main.py

# Run all unit tests
python -m pytest tests/ -v

# Run specific test case (example)
python -m pytest tests/test_experiment.py::TestExperimentLogic::test_state_transitions -v

# Static analysis and quality checks
python -m mypy src/ --ignore-missing-imports
python -m ruff check src/
```

## Repository Rules & Automation
No repository-specific rule files (`.cursorrules`, `.cursor/rules/`, or `.github/copilot-instructions.md`) were found at the root. Standard Python and PySide6 development practices apply.

## Code Style Guidelines

### Python & PySide6 Patterns
- **Typing**: Mandatory type hints for all function and method signatures.
  ```python
  def calculate_power(voltage: float, current: float) -> float:
      return voltage * current
  ```
- **Nullability**: Use `Optional[T]` from `typing` for variables that can be `None`.
- **Naming**: 
  - `PascalCase` for class names.
  - `snake_case` for functions, methods, and variables.
  - `UPPER_SNAKE_CASE` for global constants.
- **Qt Signals**: Use `camelCase` for Signal definitions (e.g., `dataUpdated = Signal(float)`).
- **Import Structure**: 
  1. Standard library imports (e.g., `sys`, `typing`).
  2. Third-party library imports (PySide6, numpy, etc.).
  3. Local module imports.
- **Formatting**: Adhere to Black's 88-character line limit, 4-space indentation, and double quotes.

### Logging Guidance
- Use the standard `logging` module for internal state changes and simulation events.
- UI logs should be displayed in the Process Monitor's log area.
- Log levels:
  - `INFO`: State transitions, user-triggered events (Start/Stop).
  - `DEBUG`: High-frequency simulation data steps.
  - `ERROR`: Exception details and validation failures.

### Error Handling
- Use custom exceptions inheriting from a base `ExperimentError`.
- Simulation steps must be wrapped in try-except blocks.
- Errors should be propagated to the UI via signals and logged as `ERROR`.

## PEM Domain Knowledge

### Constants & Physical Ranges
| Parameter | Default/Constant | Typical Range |
|-----------|------------------|---------------|
| Theoretical Voltage | 1.23 V | Baseline at 25°C |
| Thermoneutral Voltage | 1.481 V | Efficiency baseline |
| Faraday Constant | 96485.33 C/mol | N/A |
| Membrane Area | 4.0 cm² | Constant for this cell |
| Operating Voltage | 1.5 - 2.2 V | Input setting |
| Current Density | 0 - 2.5 A/cm² | Simulated output |
| Temperature | 25 - 80 °C | Input setting |

### State Machine Logic
Managed in `src/core/experiment.py`:
- `IDLE` (未启动): Initial state. No timer, zero outputs.
- `RUNNING` (运行中): Timer active. `QTimer` triggers data updates.
- `PAUSED` (暂停): Timer frozen. State preserved.
- `STOPPED` (结束): Simulation halted. Data resets or summary displays.

### Simulation Math
The simulation logic must account for standard PEM electrochemical losses:
- **Theoretical Voltage**: Baseline $V_{rev}$ calculated at given temperature (Nernst equation).
- **Activation Loss**: Dominates at low current density ($j < 0.1$ A/cm²). Modeled using the Tafel equation: $\eta_{act} = A \cdot \ln(j/j_0)$.
- **Ohmic Loss**: Linear voltage drop proportional to current. Dominates the middle region ($0.1 < j < 1.5$ A/cm²). Calculated as $\eta_{ohm} = I \cdot R_{mem}$, where $R_{mem}$ is the membrane resistance.
- **Mass Transport Loss**: Sharp voltage increase near limiting current density ($j > 1.5$ A/cm²). Modeled as $\eta_{conc} = m \cdot \exp(n \cdot j)$.
- **Efficiency**: Calculated against both theoretical and thermoneutral baselines: `η_V = V_theoretical / V_actual`.
- **Power Calculation**: Net electrical power consumption `P = V * I` where `I = j * Membrane_Area`.

## Component Architecture

### Module Responsibilities
- `src/main.py`: Entry point; initializes `QApplication` and `MainWindow`.
- `src/core/experiment.py`: Pure logic; manages state and mathematical simulation.
- `src/widgets/`: UI-specific implementations.
  - `info_panel.py`: Displays name, state, and timer.
  - `param_panel.py`: Handles spinboxes/inputs for V, j, and T.
  - `control_panel.py`: Manages the 5-button control set.
  - `monitor_panel.py`: Integrates `pyqtgraph` for real-time plotting.
  - `result_panel.py`: Shows efficiency and summary metrics.

### Signal Flow
1. User interacts with `param_panel` or `control_panel`.
2. Widgets emit signals to the `Experiment` logic.
3. `Experiment` updates internal state and performs calculations.
4. `Experiment` emits `dataUpdated` or `stateChanged` signals.
5. UI panels receive signals and update displays (plots, labels).

## Development Practices

### Testing Checklist
- [ ] Transition from `IDLE` to `RUNNING` via Start button.
- [ ] Transition from `RUNNING` to `PAUSED` via Pause button.
- [ ] Transition from `PAUSED` back to `RUNNING` via Resume button.
- [ ] Transition from `RUNNING` or `PAUSED` to `STOPPED` via Stop button.
- [ ] Transition from `STOPPED` or `IDLE` to `IDLE` via Reset button.
- [ ] Verify `STOPPED` state resets or finalizes result calculations.
- [ ] Mock `QTimer` to test simulation step frequency (default 100ms).
- [ ] Validate power calculation: `P = V * I`.
- [ ] Ensure `RESET` clears all historical plot data and resets timer.
- [ ] Verify `RESUME` correctly restarts the simulation timer from previous value.
- [ ] Check validation: Ensure inputs are within physical ranges before starting.
- [ ] Verify efficiency calculations against baseline theoretical values.
- [ ] Test real-time plot updates and data point appending in `monitor_panel`.

### Common Pitfalls & Anti-patterns
- **UI Blocking**: Do not perform heavy computations on the main thread; keep simulation steps lean.
- **State Mismatch**: Ensure Pause is only enabled when Running.
- **Floating Point Errors**: Use appropriate precision when displaying metrics in result panels.
- **Signal Loops**: Avoid circular updates between spinboxes and simulation parameters.
- **Tight Coupling**: Keep widgets from accessing `Experiment` internals directly; use signals.
- **Unmanaged Timers**: Always stop and delete timers when the application closes.

## Project Structure Reference
- `src/main.py`: Entry point.
- `src/core/`: Simulation and state machine logic.
- `src/widgets/`: Modular UI component implementations.
- `tests/`: Unit and integration test suites.
- `assets/`: UI resources, icons, and theme files.
- `docs/`: Technical specifications and user manuals.
