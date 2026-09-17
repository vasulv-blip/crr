"""Transmitter: applies Cognitive Radio recommendations."""

from __future__ import annotations

from .models import Action, CRResponse, SimConfig


class Transmitter:
    """Friendly ECCM actuator (software-only)."""

    def __init__(self, config: SimConfig):
        self.config = config
        self.channel = 0
        self.power_db = self._startup_power()
        self.hop_set: list[int] = list(range(min(3, config.n_channels)))
        self.hop_phase = 0

    def _startup_power(self) -> float:
        """Start high enough for a green FREE baseline, still within [min, max]."""
        p = float(getattr(self.config, "start_power_db", self.config.min_power_db))
        return min(self.config.max_power_db, max(self.config.min_power_db, p))

    def reset(self) -> None:
        self.channel = 0
        self.power_db = self._startup_power()
        n = self.config.n_channels
        self.hop_set = list(range(min(3, n))) if n else [0]
        self.hop_phase = 0

    def reconfigure(self, config: SimConfig) -> None:
        self.config = config
        self.reset()

    def apply(self, response: CRResponse, hop_enabled: bool) -> None:
        if response.hop_set:
            self.hop_set = [c for c in response.hop_set if 0 <= c < self.config.n_channels]
            if not self.hop_set:
                self.hop_set = [0]

        if response.action == Action.INCREASE_POWER:
            step = self.config.power_step_db
            self.power_db = min(self.config.max_power_db, self.power_db + step)
            return

        if response.action == Action.HOLD:
            return

        if response.action in (Action.USE_CHANNELS, Action.NO_SOLUTION):
            if response.channels:
                self.channel = int(response.channels[0])
            elif hop_enabled and self.hop_set:
                self.channel = self.hop_set[self.hop_phase % len(self.hop_set)]

    def next_hop_channel(self, hop_enabled: bool) -> int:
        if not hop_enabled or not self.hop_set:
            return self.channel
        self.hop_phase = (self.hop_phase + 1) % len(self.hop_set)
        self.channel = self.hop_set[self.hop_phase]
        return self.channel
