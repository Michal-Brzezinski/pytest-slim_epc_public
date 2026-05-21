import json
import pytest
from epc.models import BearerConfig, ThroughputStats


class TestPersistence:

    def test_data_persisted_after_save_ue(self, test_repo):
        test_repo.attach_ue(1)
        state = test_repo.get_ue(1)
        state.bearers[5] = BearerConfig(bearer_id=5)
        test_repo.save_ue(state)

        # Fetch again to verify persisted
        state2 = test_repo.get_ue(1)
        assert 5 in state2.bearers

    def test_uestate_serialized_as_json(self, test_repo):
        test_repo.attach_ue(1)
        test_repo.add_bearer(1, 5)
        stats = ThroughputStats(bearer_id=9, ue_id=1, bytes_tx=100)
        test_repo.update_stats(1, stats)

        # Fetch from DB directly and verify JSON structure
        conn = test_repo._conn()
        cursor = conn.execute("SELECT data FROM ue_state WHERE ue_id = ?", (1,))
        row = cursor.fetchone()
        conn.close()

        data = json.loads(row[0])
        assert data["ue_id"] == 1
        assert "9" in data["bearers"]  # Dict keys are strings in JSON
        assert "5" in data["bearers"]
        assert "9" in data["stats"]

    def test_bearer_config_persisted_with_all_fields(self, test_repo):
        test_repo.attach_ue(1)
        config = BearerConfig(bearer_id=5, protocol="tcp", target_bps=5000000, active=True)
        test_repo.add_bearer(1, 5)
        test_repo.update_bearer(1, config)

        state = test_repo.get_ue(1)
        bearer = state.bearers[5]
        assert bearer.bearer_id == 5
        assert bearer.protocol == "tcp"
        assert bearer.target_bps == 5000000
        assert bearer.active is True

    def test_stats_persisted_with_all_fields(self, test_repo):
        test_repo.attach_ue(1)
        import time
        ts = time.time()
        stats = ThroughputStats(
            bearer_id=9,
            ue_id=1,
            bytes_tx=1000,
            bytes_rx=500,
            start_ts=ts,
            last_update_ts=ts,
            protocol="tcp",
            target_bps=10000000
        )
        test_repo.update_stats(1, stats)

        state = test_repo.get_ue(1)
        retrieved = state.stats[9]
        assert retrieved.bytes_tx == 1000
        assert retrieved.bytes_rx == 500
        assert retrieved.start_ts == ts
        assert retrieved.protocol == "tcp"
        assert retrieved.target_bps == 10000000
