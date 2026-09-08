"""Cognitive Radio decision engine: rules, ML, and hybrid safety."""

from __future__ import annotations

from .hopping import adapt_hop_set
from .ml_models import ChannelRecommenderML
from .models import (
    Action,
    CRRequest,
    CRResponse,
    ChannelState,
    DecisionMode,
)


class CognitiveRadioEngine:
    def __init__(self, n_channels: int = 8, seed: int = 42):
        self.n_channels = n_channels
        self.ml = ChannelRecommenderML(n_channels=n_channels, seed=seed)
        self.ml_metrics: dict = {}

    def reconfigure(self, n_channels: int, seed: int = 42) -> None:
        self.n_channels = n_channels
        self.ml = ChannelRecommenderML(n_channels=n_channels, seed=seed)
        self.ml_metrics = {}

    def train_ml(self, n_samples: int = 1200) -> dict:
        self.ml_metrics = self.ml.train_synthetic(n_samples=n_samples)
        return self.ml_metrics

    def decide(self, request: CRRequest, mode: DecisionMode) -> CRResponse:
        if mode == DecisionMode.RULES:
            return self._rules(request, engine="RULES")
        if mode == DecisionMode.ML:
            return self._ml_with_safety(request)
        # HYBRID: ML proposes, rules validate
        ml_resp = self._ml_with_safety(request)
        if ml_resp.status_code in ("OK", "DEGRADED_OK", "INCREASE_POWER", "ALL_BLOCKED"):
            ml_resp.engine = "HYBRID"
            return ml_resp
        return self._rules(request, engine="HYBRID-FALLBACK")

    def _rank_usable(self, request: CRRequest) -> tuple[list[int], list[int], set[int]]:
        free = [o for o in request.observations if o.state == ChannelState.FREE]
        degraded = [o for o in request.observations if o.state == ChannelState.DEGRADED]
        blocked = {o.channel_id for o in request.observations if o.state == ChannelState.BLOCKED}
        free.sort(key=lambda o: o.sinr_db, reverse=True)
        degraded.sort(key=lambda o: o.sinr_db, reverse=True)
        return [o.channel_id for o in free], [o.channel_id for o in degraded], blocked

    def _rules(self, request: CRRequest, engine: str) -> CRResponse:
        free_ids, deg_ids, blocked = self._rank_usable(request)
        hop_set = list(request.hop_set)

        if free_ids:
            chosen = free_ids[0]
            if request.hop_enabled:
                hop_set = adapt_hop_set(hop_set, blocked, free_ids, request.n_channels)
            return CRResponse(
                status_code="OK",
                message=f"Channel {chosen} is FREE with best SINR; recommend CH{chosen}.",
                channels=[chosen],
                action=Action.USE_CHANNELS,
                hop_set=hop_set if request.hop_enabled else [],
                engine=engine,
            )

        if deg_ids:
            chosen = deg_ids[0]
            if request.hop_enabled:
                hop_set = adapt_hop_set(hop_set, blocked, deg_ids + free_ids, request.n_channels)
            return CRResponse(
                status_code="DEGRADED_OK",
                message=f"No FREE channels; recommend degraded CH{chosen}.",
                channels=[chosen],
                action=Action.USE_CHANNELS,
                hop_set=hop_set if request.hop_enabled else [],
                engine=engine,
            )

        if request.current_power_db + 1e-6 < request.max_power_db:
            return CRResponse(
                status_code="INCREASE_POWER",
                message="All channels blocked at current power; suggest increase transmit power.",
                channels=[],
                action=Action.INCREASE_POWER,
                power_advice_db=min(request.max_power_db, request.current_power_db + 2.0),
                hop_set=hop_set if request.hop_enabled else [],
                engine=engine,
            )

        return CRResponse(
            status_code="ALL_BLOCKED",
            message="All channels blocked and maximum power already reached; no solution within limits.",
            channels=[],
            action=Action.NO_SOLUTION,
            hop_set=hop_set if request.hop_enabled else [],
            engine=engine,
        )

    def _ml_with_safety(self, request: CRRequest) -> CRResponse:
        if not self.ml.trained:
            resp = self._rules(request, engine="RULES")
            resp.message = "ML model not trained yet; using rule baseline. " + resp.message
            resp.engine = "RULES"
            return resp

        free_ids, deg_ids, blocked = self._rank_usable(request)
        usable = set(free_ids + deg_ids)
        pred = self.ml.predict(request.observations, request.current_power_db, request.max_power_db)

        if pred.increase_power:
            if request.current_power_db + 1e-6 < request.max_power_db:
                return CRResponse(
                    status_code="INCREASE_POWER",
                    message=f"ML recommends increase power (confidence {pred.confidence:.2f}).",
                    channels=[],
                    action=Action.INCREASE_POWER,
                    power_advice_db=min(request.max_power_db, request.current_power_db + 2.0),
                    hop_set=list(request.hop_set) if request.hop_enabled else [],
                    engine="ML",
                    detail={"confidence": pred.confidence},
                )
            # Safety: cannot raise power
            return self._rules(request, engine="ML-SAFETY")

        ch = pred.channel
        if ch is None or ch in blocked or (usable and ch not in usable):
            # Safety override
            safe = self._rules(request, engine="ML-SAFETY")
            safe.message = (
                f"ML suggested CH{ch} (conf {pred.confidence:.2f}) but safety rules overrode. "
                + safe.message
            )
            return safe

        status = "OK" if ch in free_ids else "DEGRADED_OK"
        hop_set = list(request.hop_set)
        if request.hop_enabled:
            hop_set = adapt_hop_set(hop_set, blocked, free_ids + deg_ids, request.n_channels)

        return CRResponse(
            status_code=status,
            message=f"ML recommends CH{ch} (confidence {pred.confidence:.2f}).",
            channels=[ch],
            action=Action.USE_CHANNELS,
            hop_set=hop_set if request.hop_enabled else [],
            engine="ML",
            detail={"confidence": pred.confidence},
        )
