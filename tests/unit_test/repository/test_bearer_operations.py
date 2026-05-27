import pytest
from epc.models import ThroughputStats


class TestBearerOperations:

    def test_add_bearer_creates_new_bearer(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.add_bearer(1, 5)
        state = test_repo.get_ue(1)
        assert 5 in state.bearers
        assert state.bearers[5].bearer_id == 5

    def test_add_multiple_bearers(self, test_repo):
        test_repo.attach_ue(1)
        for bearer_id in [1, 2, 3, 5, 8]:
            test_repo.add_bearer(1, bearer_id)
        state = test_repo.get_ue(1)
        assert len(state.bearers) == 6
        assert all(b in state.bearers for b in [1, 2, 3, 5, 8, 9])

    def test_add_duplicate_bearer_raises_error(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.add_bearer(1, 5)
        with pytest.raises(ValueError, match="Bearer already exists"):
            test_repo.add_bearer(1, 5)

    def test_add_bearer_on_nonexistent_ue_raises_error(self, test_repo):
        with pytest.raises(ValueError, match="UE not found"):
            test_repo.add_bearer(99, 5)

    def test_delete_bearer_removes_it(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.add_bearer(1, 5)
        test_repo.delete_bearer(1, 5)
        state = test_repo.get_ue(1)
        assert 5 not in state.bearers
        assert 9 in state.bearers

    def test_cannot_delete_default_bearer(self, test_repo):
        test_repo.attach_ue(1)
        with pytest.raises(ValueError, match="Cannot remove default bearer"):
            test_repo.delete_bearer(1, 9)

    def test_delete_nonexistent_bearer_raises_error(self, test_repo):
        test_repo.attach_ue(1)
        with pytest.raises(ValueError, match="Bearer not found"):
            test_repo.delete_bearer(1, 5)

    def test_delete_bearer_on_nonexistent_ue_raises_error(self, test_repo):
        with pytest.raises(ValueError, match="UE not found"):
            test_repo.delete_bearer(99, 5)

    def test_delete_bearer_also_removes_its_stats(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.add_bearer(1, 5)
        stats = ThroughputStats(bearer_id=5, ue_id=1, bytes_tx=100)
        test_repo.update_stats(1, stats)
        assert 5 in test_repo.get_ue(1).stats

        test_repo.delete_bearer(1, 5)
        state = test_repo.get_ue(1)
        assert 5 not in state.stats
