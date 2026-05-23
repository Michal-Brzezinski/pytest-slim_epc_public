import pytest
from pydantic import ValidationError

class TestDataCorruption:
    def test_get_ue_with_malformed_json_raises_error(self, test_repo):
        with test_repo._conn() as conn:
            conn.execute(
                "INSERT INTO ue_state (ue_id, data) VALUES (?, ?)",
                (1, '{"ue_id": 1, "broken_json...')
            )

        with pytest.raises(ValidationError):
            test_repo.get_ue(1)

    def test_get_ue_with_missing_required_fields_raises_error(self, test_repo):
        with test_repo._conn() as conn:
            conn.execute(
                "INSERT INTO ue_state (ue_id, data) VALUES (?, ?)",
                (2, '{"bearers": {}, "stats": {}}')
            )

        with pytest.raises(ValidationError):
            test_repo.get_ue(2)