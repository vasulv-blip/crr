"""Supervised MLP recommender trained from simulator-style observation vectors."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from .models import ChannelObservation, ChannelState


@dataclass
class MLRecommendation:
    channel: int | None
    increase_power: bool
    confidence: float
    label: str


class ChannelRecommenderML:
    """MLP classifier: observation vector -> channel id or INCREASE_POWER."""

    POWER_LABEL = -1

    def __init__(self, n_channels: int = 8, seed: int = 42):
        self.n_channels = n_channels
        self.seed = seed
        self.scaler = StandardScaler()
        self.model = MLPClassifier(
            hidden_layer_sizes=(64, 32),
            activation="relu",
            solver="adam",
            max_iter=400,
            random_state=seed,
        )
        self.trained = False
        self.classes_: list[int] = []

    def _vector(self, observations: list[ChannelObservation], current_power_db: float, max_power_db: float) -> np.ndarray:
        n = self.n_channels
        vec = np.zeros(n * 3 + 2, dtype=float)
        by_id = {o.channel_id: o for o in observations}
        for i in range(n):
            o = by_id.get(i)
            if o is None:
                continue
            state_val = {"FREE": 2.0, "DEGRADED": 1.0, "BLOCKED": 0.0}[o.state.value]
            vec[i * 3] = o.sinr_db
            vec[i * 3 + 1] = state_val
            vec[i * 3 + 2] = o.jam_power
        vec[-2] = current_power_db
        vec[-1] = max_power_db - current_power_db
        return vec

    def _label_from_obs(self, observations: list[ChannelObservation], current_power_db: float, max_power_db: float) -> int:
        free = [o for o in observations if o.state == ChannelState.FREE]
        free.sort(key=lambda o: o.sinr_db, reverse=True)
        if free:
            return free[0].channel_id
        degraded = [o for o in observations if o.state == ChannelState.DEGRADED]
        degraded.sort(key=lambda o: o.sinr_db, reverse=True)
        if degraded:
            return degraded[0].channel_id
        if current_power_db + 1e-6 < max_power_db:
            return self.POWER_LABEL
        # Stay on best SINR even if blocked
        best = max(observations, key=lambda o: o.sinr_db)
        return best.channel_id

    def train_synthetic(self, n_samples: int = 1200) -> dict:
        """Generate synthetic labelled cases for current N."""
        from .channel import ChannelSimulator
        from .models import JamProfile, SimConfig

        rng = np.random.default_rng(self.seed)
        xs: list[np.ndarray] = []
        ys: list[int] = []

        for i in range(n_samples):
            cfg = SimConfig(n_channels=self.n_channels, seed=int(rng.integers(0, 1_000_000)))
            sim = ChannelSimulator(cfg)
            # Force some all-blocked / power-advice cases
            if i % 8 == 0:
                profile = JamProfile.BARRAGE
                sim.set_profile(profile)
                power = float(cfg.min_power_db)
            else:
                profile = rng.choice(list(JamProfile))
                if profile == JamProfile.SPOT:
                    sim.set_profile(profile, [int(rng.integers(0, self.n_channels))])
                elif profile == JamProfile.MULTI_SPOT:
                    k = int(rng.integers(2, max(3, self.n_channels // 2 + 1)))
                    ch = rng.choice(self.n_channels, size=min(k, self.n_channels), replace=False)
                    sim.set_profile(profile, list(map(int, ch)))
                elif profile == JamProfile.SWEEP:
                    sim.set_profile(profile)
                    sim.sweep_index = int(rng.integers(0, self.n_channels))
                elif profile == JamProfile.BARRAGE:
                    sim.set_profile(profile)
                else:
                    sim.clear_jam()
                power = float(rng.uniform(cfg.min_power_db, cfg.max_power_db))

            tx = int(rng.integers(0, self.n_channels))
            obs = sim.observe(tx, power)
            xs.append(self._vector(obs, power, cfg.max_power_db))
            ys.append(self._label_from_obs(obs, power, cfg.max_power_db))

        X = np.vstack(xs)
        y = np.asarray(ys)
        Xs = self.scaler.fit_transform(X)
        self.model.fit(Xs, y)
        self.trained = True
        self.classes_ = list(map(int, self.model.classes_))
        acc = float(self.model.score(Xs, y))
        return {"samples": n_samples, "train_accuracy": round(acc, 4), "classes": self.classes_}

    def predict(
        self,
        observations: list[ChannelObservation],
        current_power_db: float,
        max_power_db: float,
    ) -> MLRecommendation:
        if not self.trained:
            raise RuntimeError("ML model is not trained")

        x = self._vector(observations, current_power_db, max_power_db).reshape(1, -1)
        xs = self.scaler.transform(x)
        pred = int(self.model.predict(xs)[0])
        proba = self.model.predict_proba(xs)[0]
        conf = float(np.max(proba))

        if pred == self.POWER_LABEL:
            return MLRecommendation(channel=None, increase_power=True, confidence=conf, label="INCREASE_POWER")
        return MLRecommendation(channel=pred, increase_power=False, confidence=conf, label=f"CH{pred}")
