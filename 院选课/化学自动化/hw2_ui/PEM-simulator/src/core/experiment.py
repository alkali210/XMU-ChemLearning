# src/core/experiment.py
from enum import Enum, auto
from PySide6.QtCore import QObject, Signal


class ExperimentState(Enum):
    IDLE = auto()  # 未启动
    RUNNING = auto()  # 运行中
    PAUSED = auto()  # 暂停
    STOPPED = auto()  # 结束


class ExperimentController(QObject):
    stateChanged = Signal(ExperimentState)

    def __init__(self) -> None:
        super().__init__()
        self._state = ExperimentState.IDLE

    @property
    def state(self) -> ExperimentState:
        return self._state

    def start(self) -> bool:
        if self._state in (ExperimentState.IDLE, ExperimentState.STOPPED):
            self._set_state(ExperimentState.RUNNING)
            return True
        return False

    def pause(self) -> bool:
        if self._state == ExperimentState.RUNNING:
            self._set_state(ExperimentState.PAUSED)
            return True
        return False

    def resume(self) -> bool:
        if self._state == ExperimentState.PAUSED:
            self._set_state(ExperimentState.RUNNING)
            return True
        return False

    def stop(self) -> bool:
        if self._state in (ExperimentState.RUNNING, ExperimentState.PAUSED):
            self._set_state(ExperimentState.STOPPED)
            return True
        return False

    def reset(self) -> bool:
        if self._state in (
            ExperimentState.STOPPED,
            ExperimentState.PAUSED,
            ExperimentState.RUNNING,
        ):
            self._set_state(ExperimentState.IDLE)
            return True
        return False

    def _set_state(self, new_state: ExperimentState) -> None:
        if self._state != new_state:
            self._state = new_state
            self.stateChanged.emit(self._state)
