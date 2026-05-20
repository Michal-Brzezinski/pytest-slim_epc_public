from epc.models import BearerConfig

def test_bearer_config_defaults():
    b = BearerConfig(bearer_id=1)
    assert b.active is False
    assert b.protocol is None
    assert b.target_bps is None
