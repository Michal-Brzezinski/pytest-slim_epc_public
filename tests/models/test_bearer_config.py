"""Tests for BearerConfig model defaults and validation."""

import pytest
from pydantic import ValidationError

from epc.models import BearerConfig


def test_bearer_config_defaults():
    """Ensure default values are correctly initialized."""
    b = BearerConfig(bearer_id=1)

    assert b.active is False
    assert b.protocol is None
    assert b.target_bps is None


@pytest.mark.parametrize("protocol", ["icmp", "ftp", ""])
def test_bearer_config_invalid_protocol(protocol):
    """BearerConfig should only accept 'tcp' or 'udp' as valid protocols."""
    with pytest.raises(ValidationError):
        BearerConfig(bearer_id=1, protocol=protocol)


def test_bearer_config_protocol_case_sensitivity():
    with pytest.raises(ValidationError):
        BearerConfig(bearer_id=1, protocol="TCP")