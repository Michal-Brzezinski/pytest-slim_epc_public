"""Tests for ThroughputStats model: defaults, invariants, and serialization."""

import time
from epc.models import ThroughputStats


def test_throughput_stats_basic():
    now = time.time()

    stats = ThroughputStats(
        bearer_id=1,
        ue_id=1,
        bytes_tx=8000,
        bytes_rx=8000,
        start_ts=now - 1,
        last_update_ts=now,
    )

    assert stats.bytes_tx == 8000
    assert stats.bytes_rx == 8000
    assert stats.last_update_ts > stats.start_ts


def test_throughput_stats_serialization_roundtrip():
    """Ensure model can be safely serialized and restored without data loss."""
    stats = ThroughputStats(
        bearer_id=1,
        ue_id=1,
        bytes_tx=100,
        bytes_rx=200,
    )

    dumped = stats.model_dump_json()
    loaded = ThroughputStats.model_validate_json(dumped)

    assert loaded == stats


def test_throughput_stats_optional_fields_default_to_none():
    stats = ThroughputStats(
        bearer_id=1,
        ue_id=1,
    )

    assert stats.protocol is None
    assert stats.target_bps is None
    assert stats.start_ts is None


def test_throughput_stats_duration_invariant():
    stats = ThroughputStats(
        bearer_id=1,
        ue_id=1,
        bytes_tx=1000,
        bytes_rx=1000,
        start_ts=10,
        last_update_ts=11,
    )

    assert stats.last_update_ts >= stats.start_ts