import pytest


class TestListOperations:

    def test_list_ues_empty_initially(self, test_repo):
        assert list(test_repo.list_ues()) == []

    def test_list_ues_returns_attached(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.attach_ue(5)
        test_repo.attach_ue(3)
        ues = list(test_repo.list_ues())
        assert sorted(ues) == [1, 3, 5]

    def test_list_ues_ordered_by_ue_id(self, test_repo):
        for ue_id in [50, 10, 30, 20]:
            test_repo.attach_ue(ue_id)
        ues = list(test_repo.list_ues())
        assert ues == [10, 20, 30, 50]

    def test_list_ues_excludes_detached(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.attach_ue(5)
        test_repo.detach_ue(1)
        ues = list(test_repo.list_ues())
        assert ues == [5]

    def test_reset_all_clears_repository(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.attach_ue(5)
        test_repo.reset_all()
        assert list(test_repo.list_ues()) == []
