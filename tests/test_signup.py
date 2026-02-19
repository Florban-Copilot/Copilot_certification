"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up for activities."""

    def test_signup_success(self, client, isolated_activities):
        """
        Test successful signup for an activity.
        
        Arrange: Prepare test data with a valid activity and email
        Act: Make POST request to signup
        Assert: Verify the student is added to participants
        """
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_count = len(isolated_activities[activity]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity}"
        assert email in isolated_activities[activity]["participants"]
        assert len(isolated_activities[activity]["participants"]) == initial_count + 1

    def test_signup_duplicate_fails(self, client, isolated_activities):
        """
        Test that signing up twice for the same activity fails.
        
        Arrange: Prepare an activity and get an existing participant
        Act: Try to signup the same student twice
        Assert: Verify the second signup is rejected with 400 error
        """
        # Arrange
        activity = "Chess Club"
        email = isolated_activities[activity]["participants"][0]  # Use existing participant
        initial_count = len(isolated_activities[activity]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
        assert len(isolated_activities[activity]["participants"]) == initial_count

    def test_signup_nonexistent_activity(self, client, isolated_activities):
        """
        Test that signing up for a non-existent activity fails.
        
        Arrange: Prepare invalid activity name
        Act: Try to signup for non-existent activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_signup_adds_to_participants_list(self, client, isolated_activities):
        """
        Test that signup correctly adds email to participants.
        
        Arrange: Prepare valid activity and new email
        Act: Sign up for activity
        Assert: Verify participants list is updated
        """
        # Arrange
        activity = "Programming Class"
        email = "alex.new@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert email in isolated_activities[activity]["participants"]

    def test_signup_multiple_different_activities(self, client, isolated_activities):
        """
        Test that a student can sign up for multiple different activities.
        
        Arrange: Prepare two different activities
        Act: Sign up the same student for both
        Assert: Verify student is in both activities
        """
        # Arrange
        email = "versatile@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email in isolated_activities[activity1]["participants"]
        assert email in isolated_activities[activity2]["participants"]
