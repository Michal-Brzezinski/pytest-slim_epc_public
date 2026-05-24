import time
from epc.models import ThroughputStats

def test_throughput_stats_basic():
    now = time.time()
    stats = ThroughputStats(
        bearer_id=1,
        ue_id=1,
        bytes_tx=8000,
        bytes_rx=8000,
        start_ts=now - 1,
        last_update_ts=now,
    )
    assert stats.tx_bps > 0
    assert stats.rx_bps > 0
