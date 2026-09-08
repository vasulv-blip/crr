"""Pseudo-random hop helpers and adaptive hop-set updates."""

from __future__ import annotations

import hashlib


def prng_index(seed: int, step: int, modulus: int) -> int:
    if modulus <= 0:
        return 0
    raw = f"{seed}:{step}".encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    return int(digest[:8], 16) % modulus


def select_hop_channel(seed: int, step: int, hop_set: list[int]) -> int:
    if not hop_set:
        return 0
    idx = prng_index(seed, step, len(hop_set))
    return hop_set[idx]


def adapt_hop_set(
    hop_set: list[int],
    blocked: set[int],
    free_ranked: list[int],
    n_channels: int,
    target_size: int = 3,
) -> list[int]:
    """Remove persistently blocked members; fill from best free channels."""
    kept = [c for c in hop_set if c not in blocked]
    for c in free_ranked:
        if c not in kept and c not in blocked:
            kept.append(c)
        if len(kept) >= target_size:
            break
    if not kept:
        kept = [c for c in range(n_channels) if c not in blocked][:target_size] or [0]
    return kept[:target_size]
