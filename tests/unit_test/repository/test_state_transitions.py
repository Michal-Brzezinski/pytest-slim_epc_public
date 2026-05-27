import pytest
from epc.models import BearerConfig, ThroughputStats


class TestStateTransitions:

    def test_full_bearer_lifecycle(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.add_bearer(1, 5)

        # Update config
        config = BearerConfig(bearer_id=5, protocol="tcp", target_bps=1000000, active=True)
        test_repo.update_bearer(1, config)

        # Add stats
        stats = ThroughputStats(bearer_id=5, ue_id=1, bytes_tx=500)
        test_repo.update_stats(1, stats)

        state = test_repo.get_ue(1)
        assert 5 in state.bearers
        assert state.bearers[5].protocol == "tcp"
        assert 5 in state.stats

        # Delete bearer
        test_repo.delete_bearer(1, 5)
        state = test_repo.get_ue(1)
        assert 5 not in state.bearers
        assert 5 not in state.stats

    def test_multiple_ues_independent(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.attach_ue(2)

        test_repo.add_bearer(1, 5)
        test_repo.add_bearer(2, 7)

        state1 = test_repo.get_ue(1)
        state2 = test_repo.get_ue(2)

        assert 5 in state1.bearers and 5 not in state2.bearers
        assert 7 in state2.bearers and 7 not in state1.bearers

    def test_bearer_update_after_stats_tracking(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.add_bearer(1, 5)

        stats = ThroughputStats(bearer_id=5, ue_id=1, bytes_tx=1000)
        test_repo.update_stats(1, stats)

        config = BearerConfig(bearer_id=5, protocol="udp", target_bps=2000000)
        test_repo.update_bearer(1, config)

        state = test_repo.get_ue(1)
        assert state.bearers[5].protocol == "udp"
        assert state.stats[5].bytes_tx == 1000  # stats unchanged