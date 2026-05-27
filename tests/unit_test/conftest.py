import sys
import os
import tempfile
import shutil
import pytest
from fastapi.testclient import TestClient

# Dodaj katalog główny projektu do PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from epc.db import EPCRepository
from epc.api import get_repo


@pytest.fixture
def test_repo():
    # Tworzymy tymczasowy katalog
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test.db")

    repo = EPCRepository(db_path=db_path)
    yield repo

    # Usuwamy cały katalog (Windows pozwala)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def client(test_repo):
    app.dependency_overrides[get_repo] = lambda: test_repo
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
