"""
Database models for the Research Data Lifecycle Visualization project.
"""

from app import db

class LifecycleStage(db.Model):
    """Model representing a stage in the research data lifecycle."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer)
    tool_categories = db.relationship('ToolCategory', backref='stage', lazy='dynamic')

class ToolCategory(db.Model):
    """Model representing a tool category within a lifecycle stage."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    stage_id = db.Column(db.Integer, db.ForeignKey('lifecycle_stage.id'), nullable=False)
    tools = db.relationship('Tool', backref='category', lazy='dynamic')

class Tool(db.Model):
    """Model representing a specific tool within a tool category."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('tool_category.id'), nullable=False)

class LifecycleConnection(db.Model):
    """Model representing connections between lifecycle stages."""
    id = db.Column(db.Integer, primary_key=True)
    from_stage_id = db.Column(db.Integer, db.ForeignKey('lifecycle_stage.id'), nullable=False)
    to_stage_id = db.Column(db.Integer, db.ForeignKey('lifecycle_stage.id'), nullable=False)
    connection_type = db.Column(db.String(50))  # e.g., 'normal', 'alternative'

    from_stage = db.relationship('LifecycleStage', foreign_keys=[from_stage_id])
    to_stage = db.relationship('LifecycleStage', foreign_keys=[to_stage_id])