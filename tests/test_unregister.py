"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.

Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering from activities."""

    def test_unregister_success(self, client, isolated_activities):
        """
        Test successful unregistration from an activity.
        
        Arrange: Prepare test data with an activity and existing participant
        Act: Make DELETE request to unregister
        Assert: Verify the student is removed from participants
        """
        # Arrange
        activity = "Chess Club"
        email = isolated_activities[activity]["participants"][0]  # Use existing participant
        initial_count = len(isolated_activities[activity]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity}"
        assert email not in isolated_activities[activity]["participants"]
        assert len(isolated_activities[activity]["participants"]) == initial_count - 1

    def test_unregister_not_signed_up(self, client, isolated_activities):
        """
        Test that unregistering a non-signed-up student fails.
        
        Arrange: Prepare an activity and an email not in participants
        Act: Try to unregister a student who isn't signed up
        Assert: Verify 400 error is returned
        """
        # Arrange
        activity = "Basketball Team"
        email = "not.registered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_nonexistent_activity(self, client, isolated_activities):
        """
        Test that unregistering from a non-existent activity fails.
        
        Arrange: Prepare invalid activity name
        Act: Try to unregister from non-existent activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_unregister_removes_from_participants(self, client, isolated_activities):
        """
        Test that unregister correctly removes email from participants.
        
        Arrange: Prepare activity and signed-up participant
        Act: Unregister from activity
        Assert: Verify participants list is updated
        """
        # Arrange
        activity = "Programming Class"
        email = isolated_activities[activity]["participants"][0]
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert email not in isolated_activities[activity]["participants"]

    def test_unregister_then_signup_again(self, client, isolated_activities):
        """
        Test that unregistering and then signing up again works correctly.
        
        Arrange: Prepare activity and participant
        Act: Unregister and then sign up again
        Assert: Verify the student can re-sign up after unregistering
        """
        # Arrange
        activity = "Gym Class"
        email = isolated_activities[activity]["participants"][0]
        
        # Act
        unregister_response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        assert email in isolated_activities[activity]["participants"]

    def test_unregister_participant_count_decreases(self, client, isolated_activities):
        """
        Test that max_participants limits are properly tracked after unregister.
        
        Arrange: Prepare activity with participants
        Act: Unregister a student
        Assert: Verify participant count decreases correctly
        """
        # Arrange
        activity = "Art Studio"
        email = isolated_activities[activity]["participants"][0]
        initial_count = len(isolated_activities[activity]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        final_count = len(isolated_activities[activity]["participants"])
        
        # Assert
        assert response.status_code == 200
        assert final_count == initial_count - 1
