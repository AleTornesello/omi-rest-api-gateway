from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from omi_rest_api_gateway.core.config import Environment, Settings
from omi_rest_api_gateway.main import create_app


@pytest.fixture
def client() -> Generator[TestClient]:
    settings = Settings(environment=Environment.test)
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client
