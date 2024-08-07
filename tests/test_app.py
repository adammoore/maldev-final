"""
Unit tests for the Flask application.
"""

import pytest
from app import create_app

def test_app_creation():
    """Test that the app can be created."""
    app = create_app('testing')
    assert app is not None
    assert app.config['TESTING'] == True

# Add more app-related tests as needed