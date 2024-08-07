"""
Define the routes for the Flask application.
"""
from flask import Blueprint, render_template, jsonify
from app.models import LifecycleStage, Substage, Tool

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@main.route('/api/lifecycle')
def get_lifecycle():
    """Get all lifecycle stages."""
    stages = LifecycleStage.query.all()
    return jsonify([stage.to_dict() for stage in stages])

@main.route('/api/substages/<int:stage_id>')
def get_substages(stage_id):
    """Get substages for a specific lifecycle stage."""
    substages = Substage.query.filter_by(stage_id=stage_id).all()
    return jsonify([substage.to_dict() for substage in substages])

@main.route('/api/tools/<int:stage_id>')
def get_tools(stage_id):
    """Get tools for a specific lifecycle stage."""
    tools = Tool.query.filter_by(stage_id=stage_id).all()
    return jsonify([tool.to_dict() for tool in tools])
