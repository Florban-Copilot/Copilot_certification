"""
Pytest configuration and fixtures for FastAPI tests.

This module provides shared fixtures for test isolation and setup/teardown.
"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient for making requests to the FastAPI application.
    
    Yields:
        TestClient: A test client for the FastAPI app
    """
    return TestClient(app)


@pytest.fixture
def isolated_activities(monkeypatch):
    """
    Provide an isolated copy of the activities database for each test.
    
    This fixture creates a deep copy of the activities to ensure tests
    don't interfere with each other. Uses monkeypatch to temporarily
    replace the app's activities with the isolated copy.
    
    Yields:
        dict: A deep copy of the activities database
    """
    # Create a deep copy to avoid test interference
    activities_copy = copy.deepcopy(activities)
    
    # Monkeypatch the app's activities to use the isolated copy
    monkeypatch.setattr("src.app.activities", activities_copy)
    
    yield activities_copy
