"""
Define the database models for the application.
"""
from app import db

class LifecycleStage(db.Model):
    """Model representing a stage in the research data lifecycle."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    substages = db.relationship('Substage', backref='stage', lazy='dynamic')
    tools = db.relationship('Tool', backref='stage', lazy='dynamic')

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Substage(db.Model):
    """Model representing a substage within a lifecycle stage."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    stage_id = db.Column(db.Integer, db.ForeignKey('lifecycle_stage.id'), nullable=False)

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'stage_id': self.stage_id
        }

class Tool(db.Model):
    """Model representing a research tool."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(200))
    stage_id = db.Column(db.Integer, db.ForeignKey('lifecycle_stage.id'), nullable=False)

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'stage_id': self.stage_id
        }
