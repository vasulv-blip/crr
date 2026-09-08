"""Channel and ECM jam simulation."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np

from .models import ChannelObservation, ChannelState, JamProfile, SimConfig


def _db(linear: float) -> float:
    return 10.0 * math.log10(max(linear, 1e-12))


def _lin(db: float) -> float:
    return 10.0 ** (db / 10.0)


class ChannelSimulator:
    """Models N logical channels with configurable jam profiles."""

    def __init__(self, config: SimConfig):
        self.config = config
        self.rng = np.random.default_rng(config.seed)
        self.step = 0
        self.profile = JamProfile.NONE
        self.manual_jammed: set[int] = set()
        self.sweep_index = 0
        self.path_gains = np.full(config.n_channels, config.base_path_gain, dtype=float)

    def reset(self, seed: int | None = None) -> None:
        if seed is not None:
            self.config.seed = seed
        self.rng = np.random.default_rng(self.config.seed)
        self.step = 0
        self.profile = JamProfile.NONE
        self.manual_jammed.clear()
        self.sweep_index = 0
        self.path_gains = np.full(self.config.n_channels, self.config.base_path_gain, dtype=float)

    def set_profile(self, profile: JamProfile, channels: Iterable[int] | None = None) -> None:
        self.profile = profile
        self.manual_jammed = set(int(c) for c in (channels or []) if 0 <= int(c) < self.config.n_channels)
        if profile == JamProfile.SWEEP:
            self.sweep_index = 0
        if profile == JamProfile.NONE:
            self.manual_jammed.clear()

    def toggle_channel_jam(self, channel_id: int) -> None:
        if channel_id in self.manual_jammed:
            self.manual_jammed.remove(channel_id)
        else:
            self.manual_jammed.add(channel_id)
        if self.manual_jammed:
            self.profile = JamProfile.MULTI_SPOT if len(self.manual_jammed) > 1 else JamProfile.SPOT
        else:
            self.profile = JamProfile.NONE

    def clear_jam(self) -> None:
        self.profile = JamProfile.NONE
        self.manual_jammed.clear()

    def _jam_powers(self) -> np.ndarray:
        n = self.config.n_channels
        jam = np.zeros(n, dtype=float)
        jp = self.config.jam_power

        if self.profile == JamProfile.NONE and not self.manual_jammed:
            return jam

        if self.profile == JamProfile.BARRAGE:
            jam[:] = jp
            return jam

        if self.profile == JamProfile.SWEEP:
            jam[self.sweep_index % n] = jp
            # Mild bleed on neighbours for realism
            jam[(self.sweep_index - 1) % n] = jp * 0.15
            jam[(self.sweep_index + 1) % n] = jp * 0.15
            return jam

        targets = self.manual_jammed
        if self.profile == JamProfile.SPOT and not targets:
            targets = {0}
        if self.profile == JamProfile.MULTI_SPOT and not targets:
            targets = {0, 1, n // 2}

        for c in targets:
            if 0 <= c < n:
                jam[c] = jp
        return jam

    def advance(self) -> None:
        self.step += 1
        # Slow fading
        fade = 1.0 + 0.08 * self.rng.normal(0.0, 1.0, size=self.config.n_channels)
        self.path_gains = np.clip(self.path_gains * fade, 0.4, 1.6)
        if self.profile == JamProfile.SWEEP:
            self.sweep_index = (self.sweep_index + 1) % self.config.n_channels

    def observe(
        self,
        tx_channel: int,
        tx_power_db: float,
    ) -> list[ChannelObservation]:
        jam = self._jam_powers()
        noise = self.config.noise_power
        tx_lin = _lin(tx_power_db)
        out: list[ChannelObservation] = []

        for k in range(self.config.n_channels):
            gain = float(self.path_gains[k])
            signal = tx_lin * gain if k == tx_channel else 1e-6
            jam_p = float(jam[k])
            interference = noise + jam_p
            sinr_db = _db(signal / interference)

            if sinr_db >= self.config.t_good_db:
                state = ChannelState.FREE
            elif sinr_db >= self.config.t_bad_db:
                state = ChannelState.DEGRADED
            else:
                state = ChannelState.BLOCKED

            # Non-TX channels: treat as sensing quality for occupancy
            if k != tx_channel:
                # Sensing proxy: high jam => blocked/degraded even without friendly signal
                sense_signal = 0.5 * gain
                sense_sinr = _db(sense_signal / interference)
                if jam_p >= self.config.jam_power * 0.5:
                    state = ChannelState.BLOCKED if sense_sinr < self.config.t_bad_db else ChannelState.DEGRADED
                    sinr_db = sense_sinr
                else:
                    state = ChannelState.FREE if sense_sinr >= self.config.t_good_db else ChannelState.DEGRADED
                    sinr_db = sense_sinr

            out.append(
                ChannelObservation(
                    channel_id=k,
                    signal_power=float(signal),
                    noise_power=float(noise),
                    jam_power=jam_p,
                    path_gain=gain,
                    sinr_db=float(sinr_db),
                    state=state,
                    is_active_tx=(k == tx_channel),
                )
            )
        return out
