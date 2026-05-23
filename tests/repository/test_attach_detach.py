import pytest

class TestAttachDetach:

    def test_attach_ue_creates_default_bearer(self, test_repo):
        test_repo.attach_ue(1)
        assert test_repo.ue_exists(1)
        state = test_repo.get_ue(1)
        assert 9 in state.bearers

    def test_attach_ue_initializes_bearers_with_only_default_bearer(self, test_repo):
        test_repo.attach_ue(5)
        state = test_repo.get_ue(5)
        assert len(state.bearers) == 1
        assert state.bearers[9].bearer_id == 9

    def test_attach_ue_initializes_empty_stats_dict(self, test_repo):
        test_repo.attach_ue(10)
        state = test_repo.get_ue(10)
        assert state.stats == {}

    def test_duplicate_attach_raises_error(self, test_repo):
        test_repo.attach_ue(1)
        with pytest.raises(ValueError, match="UE already attached"):
            test_repo.attach_ue(1)

    def test_detach_removes_ue(self, test_repo):
        test_repo.attach_ue(1)
        assert test_repo.ue_exists(1)
        test_repo.detach_ue(1)
        assert not test_repo.ue_exists(1)

    def test_detach_nonexistent_raises_error(self, test_repo):
        with pytest.raises(ValueError, match="UE not found"):
            test_repo.detach_ue(99)

    def test_get_nonexistent_ue_raises_error(self, test_repo):
        with pytest.raises(ValueError, match="UE not found"):
            test_repo.get_ue(99)

    def test_ue_exists_returns_false_initially(self, test_repo):
        assert not test_repo.ue_exists(1)

    def test_ue_exists_returns_true_after_attach(self, test_repo):
        test_repo.attach_ue(1)
        assert test_repo.ue_exists(1)

    def test_ue_exists_returns_false_after_detach(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.detach_ue(1)
        assert not test_repo.ue_exists(1)
