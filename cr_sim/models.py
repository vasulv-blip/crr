"""Shared data models for the Cognitive Radio simulation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ChannelState(str, Enum):
    FREE = "FREE"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


class JamProfile(str, Enum):
    NONE = "NONE"
    SPOT = "SPOT"
    MULTI_SPOT = "MULTI_SPOT"
    SWEEP = "SWEEP"
    BARRAGE = "BARRAGE"


class DecisionMode(str, Enum):
    RULES = "RULES"
    ML = "ML"
    HYBRID = "HYBRID"


class Action(str, Enum):
    USE_CHANNELS = "USE_CHANNELS"
    INCREASE_POWER = "INCREASE_POWER"
    HOLD = "HOLD"
    NO_SOLUTION = "NO_SOLUTION"


@dataclass
class ChannelObservation:
    channel_id: int
    signal_power: float
    noise_power: float
    jam_power: float
    path_gain: float
    sinr_db: float
    state: ChannelState
    is_active_tx: bool = False

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["state"] = self.state.value
        return d


@dataclass
class CRRequest:
    observations: list[ChannelObservation]
    current_channel: int
    current_power_db: float
    max_power_db: float
    hop_enabled: bool
    hop_set: list[int]
    n_channels: int


@dataclass
class CRResponse:
    status_code: str
    message: str
    channels: list[int]
    action: Action
    power_advice_db: float | None = None
    hop_set: list[int] = field(default_factory=list)
    engine: str = "RULES"
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status_code": self.status_code,
            "message": self.message,
            "channels": list(self.channels),
            "action": self.action.value,
            "power_advice_db": self.power_advice_db,
            "hop_set": list(self.hop_set),
            "engine": self.engine,
            "detail": self.detail,
        }


@dataclass
class SimConfig:
    n_channels: int = 8
    noise_power: float = 1.0
    base_path_gain: float = 1.0
    jam_power: float = 40.0
    t_good_db: float = 10.0
    t_bad_db: float = 3.0
    min_power_db: float = 0.0
    max_power_db: float = 20.0
    # Benign startup TX level so active carrier begins FREE (≥ t_good) before ECM.
    start_power_db: float = 12.0
    power_step_db: float = 2.0
    seed: int = 42
    hop_enabled: bool = False
    decision_mode: DecisionMode = DecisionMode.HYBRID
