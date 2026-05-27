import pytest
from epc.models import ThroughputStats


class TestStatsTracking:

    def test_update_stats_creates_entry(self, test_repo):
        test_repo.attach_ue(1)
        stats = ThroughputStats(bearer_id=9, ue_id=1, bytes_tx=500, bytes_rx=300)
        test_repo.update_stats(1, stats)

        state = test_repo.get_ue(1)
        assert 9 in state.stats
        assert state.stats[9].bytes_tx == 500
        assert state.stats[9].bytes_rx == 300

    def test_update_stats_overwrites_previous(self, test_repo):
        test_repo.attach_ue(1)
        stats1 = ThroughputStats(bearer_id=9, ue_id=1, bytes_tx=100)
        test_repo.update_stats(1, stats1)

        stats2 = ThroughputStats(bearer_id=9, ue_id=1, bytes_tx=500)
        test_repo.update_stats(1, stats2)

        state = test_repo.get_ue(1)
        assert state.stats[9].bytes_tx == 500

    def test_update_stats_on_nonexistent_ue_raises_error(self, test_repo):
        stats = ThroughputStats(bearer_id=9, ue_id=99, bytes_tx=100)
        with pytest.raises(ValueError, match="UE not found"):
            test_repo.update_stats(99, stats)

    def test_multiple_bearer_stats_tracked_independently(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.add_bearer(1, 5)

        stats9 = ThroughputStats(bearer_id=9, ue_id=1, bytes_tx=1000, bytes_rx=500)
        stats5 = ThroughputStats(bearer_id=5, ue_id=1, bytes_tx=2000, bytes_rx=1500)

        test_repo.update_stats(1, stats9)
        test_repo.update_stats(1, stats5)

        state = test_repo.get_ue(1)
        assert state.stats[9].bytes_tx == 1000
        assert state.stats[5].bytes_tx == 2000
