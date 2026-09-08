"""Receiver: measurement-based channel classification."""

from __future__ import annotations

from .models import ChannelObservation, CRRequest


class Receiver:
    """ES-style sensing: classifies from channel measurements only."""

    def build_request(
        self,
        observations: list[ChannelObservation],
        current_channel: int,
        current_power_db: float,
        max_power_db: float,
        hop_enabled: bool,
        hop_set: list[int],
    ) -> CRRequest:
        return CRRequest(
            observations=observations,
            current_channel=current_channel,
            current_power_db=current_power_db,
            max_power_db=max_power_db,
            hop_enabled=hop_enabled,
            hop_set=list(hop_set),
            n_channels=len(observations),
        )
