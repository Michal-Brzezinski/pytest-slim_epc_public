"""Tests for UEState model: serialization, initialization logic, and immutability guarantees."""

from epc.models import UEState, BearerConfig


def test_ue_state_serialization_roundtrip():
    state = UEState(ue_id=1)
    state.bearers[9] = BearerConfig(bearer_id=9)

    dumped = state.model_dump_json()
    loaded = UEState.model_validate_json(dumped)

    assert loaded.ue_id == 1
    assert 9 in loaded.bearers
    assert loaded.bearers[9].bearer_id == 9


def test_ue_state_initializes_missing_dicts():
    """Ensure None values are converted into empty dictionaries."""
    state = UEState(
        ue_id=1,
        bearers=None,
        stats=None,
    )

    assert state.bearers == {}
    assert state.stats == {}


def test_ue_state_instances_do_not_share_mutable_defaults():
    """Ensure each UEState instance has independent dictionaries."""
    a = UEState(ue_id=1)
    b = UEState(ue_id=2)

    a.bearers[9] = BearerConfig(bearer_id=9)

    assert b.bearers == {}