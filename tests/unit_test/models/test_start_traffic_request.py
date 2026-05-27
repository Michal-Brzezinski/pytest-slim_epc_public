"""Tests for StartTrafficRequest model validation and throughput conversion logic."""

import pytest
from pydantic import ValidationError

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
    {"protocol": "tcp", "Mbps": 1, "kbps": 1},   # multiple values not allowed
    {"protocol": "udp", "Mbps": None, "kbps": None, "bps": None},  # no value provided
    {"protocol": "tcp"},  # missing throughput
])
def test_start_traffic_invalid_units(payload):
    with pytest.raises(ValidationError):
        StartTrafficRequest(**payload)


@pytest.mark.parametrize("protocol", ["", "ftp", "http"])
def test_start_traffic_invalid_protocol(protocol):
    with pytest.raises(ValidationError):
        StartTrafficRequest(protocol=protocol, Mbps=1)


def test_target_bps_uses_mbps_conversion():
    req = StartTrafficRequest(protocol="tcp", Mbps=2.5)
    assert req.target_bps() == 2_500_000


def test_negative_throughput_is_accepted_as_input():
    req = StartTrafficRequest(protocol="tcp", Mbps=-1)
    assert req.Mbps == -1


def test_start_traffic_float_conversion():
    req = StartTrafficRequest(protocol="tcp", Mbps=1.5)
    assert req.target_bps() == 1_500_000


@pytest.mark.parametrize("protocol", ["TCP", "UDP"])
def test_start_traffic_uppercase_protocol_rejected(protocol):
    with pytest.raises(ValidationError):
        StartTrafficRequest(protocol=protocol, Mbps=1)


def test_target_bps_consistency_across_calls():
    req = StartTrafficRequest(protocol="tcp", Mbps=1)
    assert req.target_bps() == req.target_bps()