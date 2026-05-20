# tests/test_repository.py
import pytest

def test_cannot_delete_default_bearer(test_repo):
    test_repo.attach_ue(1)
    with pytest.raises(ValueError):
        test_repo.delete_bearer(1, 9)
