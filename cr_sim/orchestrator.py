"""Closed-loop orchestrator for the Cognitive Radio simulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .channel import ChannelSimulator
from .cr_engine import CognitiveRadioEngine
from .hopping import select_hop_channel
from .models import CRResponse, DecisionMode, JamProfile, SimConfig
from .receiver import Receiver
from .transmitter import Transmitter


@dataclass
class StepResult:
    step: int
    observations: list[dict[str, Any]]
    response: dict[str, Any]
    tx_channel: int
    tx_power_db: float
    hop_set: list[int]
    jam_profile: str


@dataclass
class SimulationState:
    config: SimConfig
    history: list[StepResult] = field(default_factory=list)
    last_response: dict[str, Any] | None = None
    ml_metrics: dict[str, Any] = field(default_factory=dict)


class Orchestrator:
    def __init__(self, config: SimConfig | None = None):
        self.config = config or SimConfig()
        self.channel = ChannelSimulator(self.config)
        self.receiver = Receiver()
        self.transmitter = Transmitter(self.config)
        self.engine = CognitiveRadioEngine(n_channels=self.config.n_channels, seed=self.config.seed)
        self.history: list[StepResult] = []
        self.last_response: CRResponse | None = None

    def reset(self, config: SimConfig | None = None) -> None:
        if config is not None:
            self.config = config
        self.channel = ChannelSimulator(self.config)
        self.transmitter.reconfigure(self.config)
        self.engine.reconfigure(self.config.n_channels, self.config.seed)
        self.history.clear()
        self.last_response = None

    def train_ml(self, n_samples: int = 1200) -> dict:
        metrics = self.engine.train_ml(n_samples=n_samples)
        return metrics

    def set_jam(self, profile: JamProfile, channels: list[int] | None = None) -> None:
        self.channel.set_profile(profile, channels)

    def clear_jam(self) -> None:
        self.channel.clear_jam()

    def toggle_jam_channel(self, channel_id: int) -> None:
        self.channel.toggle_channel_jam(channel_id)

    def step(self) -> StepResult:
        hop_enabled = self.config.hop_enabled
        if hop_enabled and self.transmitter.hop_set:
            self.transmitter.channel = select_hop_channel(
                self.config.seed,
                self.channel.step,
                self.transmitter.hop_set,
            )

        observations = self.channel.observe(self.transmitter.channel, self.transmitter.power_db)
        request = self.receiver.build_request(
            observations=observations,
            current_channel=self.transmitter.channel,
            current_power_db=self.transmitter.power_db,
            max_power_db=self.config.max_power_db,
            hop_enabled=hop_enabled,
            hop_set=self.transmitter.hop_set,
        )
        response = self.engine.decide(request, self.config.decision_mode)
        self.transmitter.apply(response, hop_enabled=hop_enabled)
        self.last_response = response

        result = StepResult(
            step=self.channel.step,
            observations=[o.to_dict() for o in observations],
            response=response.to_dict(),
            tx_channel=self.transmitter.channel,
            tx_power_db=self.transmitter.power_db,
            hop_set=list(self.transmitter.hop_set),
            jam_profile=self.channel.profile.value,
        )
        self.history.append(result)
        self.channel.advance()
        return result
