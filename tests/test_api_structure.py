# Test to verify API routes are correctly defined
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_auth_routes_exist():
    """Test that all auth routes are defined."""
    # Test that the routes exist by checking the OpenAPI schema
    openapi_schema = app.openapi()
    paths = openapi_schema["paths"]
    
    # Check that the expected routes exist
    assert "/auth/signup" in paths
    assert "/auth/login" in paths
    assert "/auth/refresh" in paths
    assert "/auth/logout" in paths
    assert "/auth/me" in paths
    
    # Check that the methods are correct
    assert "post" in paths["/auth/signup"]
    assert "post" in paths["/auth/login"]
    assert "post" in paths["/auth/refresh"]
    assert "post" in paths["/auth/logout"]
    assert "get" in paths["/auth/me"]