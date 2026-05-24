from epc.models import UEState, BearerConfig

def test_ue_state_serialization_roundtrip():
    state = UEState(ue_id=1)
    state.bearers[9] = BearerConfig(bearer_id=9)

    dumped = state.model_dump_json()
    loaded = UEState.model_validate_json(dumped)

    assert loaded.ue_id == 1
    assert 9 in loaded.bearers
