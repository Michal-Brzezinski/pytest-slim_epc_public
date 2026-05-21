import pytest
from epc.models import BearerConfig


class TestUpdateBearer:

    def test_update_bearer_modifies_config(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.add_bearer(1, 5)
        new_config = BearerConfig(bearer_id=5, protocol="tcp", target_bps=1000000, active=True)
        test_repo.update_bearer(1, new_config)

        state = test_repo.get_ue(1)
        bearer = state.bearers[5]
        assert bearer.protocol == "tcp"
        assert bearer.target_bps == 1000000
        assert bearer.active is True

    def test_update_nonexistent_ue_raises_error(self, test_repo):
        new_config = BearerConfig(bearer_id=5, protocol="udp")
        with pytest.raises(ValueError, match="UE not found"):
            test_repo.update_bearer(99, new_config)

    def test_update_bearer_preserves_other_bearers(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.add_bearer(1, 3)
        test_repo.add_bearer(1, 5)

        new_config = BearerConfig(bearer_id=3, protocol="tcp", target_bps=5000000)
        test_repo.update_bearer(1, new_config)

        state = test_repo.get_ue(1)
        assert state.bearers[3].protocol == "tcp"
        assert state.bearers[3].target_bps == 5000000
        assert 5 in state.bearers
        assert state.bearers[5].protocol is None
