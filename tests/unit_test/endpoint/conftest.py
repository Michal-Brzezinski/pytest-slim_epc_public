import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def mock_tm():
    with patch("epc.api.get_traffic_manager") as mock_gtm:
        tm = MagicMock()
        mock_gtm.return_value = tm
        yield tm
