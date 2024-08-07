"""
Unit tests for database models.
"""

import pytest
from app import create_app, db
from app.models import LifecycleStage, ToolCategory, Tool, LifecycleConnection

@pytest.fixture
def test_app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_lifecycle_stage_creation(test_app):
    """Test LifecycleStage model creation."""
    with test_app.app_context():
        stage = LifecycleStage(name="Test Stage", description="Test Description", order=1)
        db.session.add(stage)
        db.session.commit()
        
        assert stage.id is not None
        assert LifecycleStage.query.filter_by(name="Test Stage").first() is not None

def test_tool_category_creation(test_app):
    """Test ToolCategory model creation."""
    with test_app.app_context():
        stage = LifecycleStage(name="Test Stage", description="Test Description", order=1)
        db.session.add(stage)
        db.session.commit()
        
        category = ToolCategory(name="Test Category", description="Test Description", stage=stage)
        db.session.add(category)
        db.session.commit()
        
        assert category.id is not None
        assert ToolCategory.query.filter_by(name="Test Category").first() is not None

def test_tool_creation(test_app):
    """Test Tool model creation."""
    with test_app.app_context():
        stage = LifecycleStage(name="Test Stage", description="Test Description", order=1)
        category = ToolCategory(name="Test Category", description="Test Description", stage=stage)
        db.session.add_all([stage, category])
        db.session.commit()
        
        tool = Tool(name="Test Tool", description="Test Description", url="http://test.com", category=category)
        db.session.add(tool)
        db.session.commit()
        
        assert tool.id is not None
        assert Tool.query.filter_by(name="Test Tool").first() is not None

def test_lifecycle_connection_creation(test_app):
    """Test LifecycleConnection model creation."""
    with test_app.app_context():
        stage1 = LifecycleStage(name="Stage 1", description="Description 1", order=1)
        stage2 = LifecycleStage(name="Stage 2", description="Description 2", order=2)
        db.session.add_all([stage1, stage2])
        db.session.commit()
        
        connection = LifecycleConnection(from_stage=stage1, to_stage=stage2, connection_type="normal")
        db.session.add(connection)
        db.session.commit()
        
        assert connection.id is not None
        assert LifecycleConnection.query.filter_by(from_stage_id=stage1.id, to_stage_id=stage2.id).first() is not None