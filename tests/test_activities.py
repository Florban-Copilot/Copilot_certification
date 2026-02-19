"""
Tests for the GET /activities endpoint.

Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_activities_returns_all_activities(self, client, isolated_activities):
        """
        Test that GET /activities returns all available activities.
        
        Arrange: Prepare the test client
        Act: Make GET request to /activities
        Assert: Verify response contains all activities
        """
        # Arrange
        expected_activity_count = len(isolated_activities)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        assert isinstance(activities, dict)

    def test_get_activities_returns_correct_structure(self, client, isolated_activities):
        """
        Test that each activity has the required fields.
        
        Arrange: Prepare the test client
        Act: Make GET request to /activities
        Assert: Verify activity structure is correct
        """
        # Arrange
        expected_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert all(field in activity_data for field in expected_fields)
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_get_activities_contains_specific_activities(self, client, isolated_activities):
        """
        Test that GET /activities contains expected activities.
        
        Arrange: Prepare the test client
        Act: Make GET request to /activities
        Assert: Verify specific activities are present
        """
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_participants_are_lists(self, client, isolated_activities):
        """
        Test that participants are returned as lists of email strings.
        
        Arrange: Prepare the test client
        Act: Make GET request to /activities
        Assert: Verify participants are email strings in lists
        """
        # Arrange
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email validation
