import pytest
from epc.models import StartTrafficRequest

def test_start_traffic_valid_mbps():
    req = StartTrafficRequest(protocol="tcp", Mbps=1)
    assert req.target_bps() == 1_000_000

def test_start_traffic_valid_kbps():
    req = StartTrafficRequest(protocol="udp", kbps=500)
    assert req.target_bps() == 500_000

def test_start_traffic_valid_bps():
    req = StartTrafficRequest(protocol="tcp", bps=1234)
    assert req.target_bps() == 1234

@pytest.mark.parametrize("payload", [
    {"protocol": "tcp", "Mbps": 1, "kbps": 1},
    {"protocol": "udp", "Mbps": None, "kbps": None, "bps": None},
    {"protocol": "tcp"},
])
def test_start_traffic_invalid_units(payload):
    with pytest.raises(ValueError):
        StartTrafficRequest(**payload)

@pytest.mark.parametrize("protocol", ["", "ftp", "http"])
def test_start_traffic_invalid_protocol(protocol):
    with pytest.raises(ValueError):
        StartTrafficRequest(protocol=protocol, Mbps=1)
