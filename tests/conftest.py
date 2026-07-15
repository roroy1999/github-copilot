import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module
from src.app import app


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))
