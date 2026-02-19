"""
Tests for the GET / redirect endpoint.

Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest


class TestRootRedirect:
    """Test suite for the root endpoint."""

    def test_root_redirects_to_index(self, client):
        """
        Test that GET / redirects to /static/index.html.
        
        Arrange: Prepare the test client
        Act: Make GET request to /
        Assert: Verify redirect to index.html
        """
        # Arrange
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]

    def test_root_redirect_follows_to_html(self, client):
        """
        Test that following the redirect from / reaches index.html.
        
        Arrange: Prepare the test client
        Act: Make GET request to / and follow redirects
        Assert: Verify HTML content is returned
        """
        # Arrange
        # Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Mergington High School" in response.text

    def test_root_uses_correct_redirect_method(self, client):
        """
        Test that the root endpoint uses 307 Temporary Redirect.
        
        Arrange: Prepare the test client
        Act: Make GET request to /
        Assert: Verify correct HTTP status code
        """
        # Arrange
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
