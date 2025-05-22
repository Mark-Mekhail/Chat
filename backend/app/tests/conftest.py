import pytest
from fastapi.testclient import TestClient

# Import patch_modules first to set up mocking before app imports
from app.tests import patch_modules
from app.main import app

# Apply service-specific patches after imports
patch_modules.apply_service_patches()

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

def pytest_sessionfinish(exitstatus: int) -> None:
    patch_modules.stop_all_patches()
