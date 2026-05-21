import pytest
from pydantic import ValidationError

class TestDatabaseValidation:
    def test_attach_ue_out_of_bounds_raises_error(self, test_repo):
        with pytest.raises(ValidationError):
            test_repo.attach_ue(101)

        with pytest.raises(ValidationError):
            test_repo.attach_ue(0)

    def test_add_bearer_out_of_bounds_raises_error(self, test_repo):
        test_repo.attach_ue(1)

        with pytest.raises(ValidationError):
            test_repo.add_bearer(1, 10)

        with pytest.raises(ValidationError):
            test_repo.add_bearer(1, -1)