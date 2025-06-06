"""
Pytest configuration and shared fixtures for the insurance fraud detection system.
"""
import pytest
import os
import json
import tempfile
from datetime import datetime
import uuid

# Add the parent directory to Python path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.claim import Claim
from models.event import Event


@pytest.fixture
def sample_claim_data():
    """Sample claim data for testing"""
    return {
        "claim_id": f"test-{uuid.uuid4()}",
        "claim_amount": 1500.0,
        "description": "Vehicle accident on Highway 101",
        "submission_time": datetime.now().isoformat(),
        "status": "pending",
        "fraud_score": None,
        "uploaded_files": []
    }


@pytest.fixture
def sample_event_data():
    """Sample event data for testing"""
    return {
        "event_id": str(uuid.uuid4()),
        "entity_id": f"test-{uuid.uuid4()}",
        "event_type": "submitted",
        "timestamp": datetime.now().isoformat(),
        "data": {"source": "web_portal", "user_agent": "test"}
    }


@pytest.fixture
def sample_claim_object(sample_claim_data):
    """Sample Claim object for testing"""
    return Claim.from_dict(sample_claim_data)


@pytest.fixture
def sample_event_object(sample_event_data):
    """Sample Event object for testing"""
    return Event.from_dict(sample_event_data)


@pytest.fixture
def temp_data_dir():
    """Temporary directory for test data files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_cosmos_config():
    """Mock Cosmos DB configuration for testing"""
    return {
        "cosmos_db": {
            "endpoint": "https://test-cosmosdb.documents.azure.com:443/",
            "key": "test-key",
            "database_name": "test-insurance-db",
            "container_name": "test-claims"
        }
    }


@pytest.fixture
def app_config():
    """Application configuration for testing"""
    return {
        "app": {
            "debug": True,
            "testing": True,
            "upload_folder": "test_uploads",
            "max_content_length": 16 * 1024 * 1024
        },
        "cosmos_db": {
            "endpoint": os.getenv("COSMOS_DB_ENDPOINT", ""),
            "key": os.getenv("COSMOS_DB_KEY", ""),
            "database_name": "test-insurance-db",
            "container_name": "test-claims"
        }
    }


@pytest.fixture
def flask_app():
    """Flask application instance for testing"""
    # Import here to avoid circular imports
    from app import create_app
    
    app = create_app(testing=True)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        yield app


@pytest.fixture
def client(flask_app):
    """Flask test client"""
    return flask_app.test_client()


# Configure pytest
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (deselect with '-m \"not integration\"')"
    )
    config.addinivalue_line(
        "markers", "cosmos: marks tests that require Cosmos DB connection"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
