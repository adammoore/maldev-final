"""
Define the routes for the Flask application.
"""
from flask import Blueprint, render_template, jsonify
from app.models import LifecycleStage, ToolCategory, Tool

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@main.route('/api/lifecycle')
def get_lifecycle():
    """API endpoint to retrieve the lifecycle stages and their connections."""
    stages = LifecycleStage.query.all()
    return jsonify([stage.to_dict() for stage in stages])

@main.route('/api/tool_categories/<int:stage_id>')
def get_tool_categories(stage_id):
    """API endpoint to retrieve tool categories for a given stage."""
    categories = ToolCategory.query.filter_by(stage_id=stage_id).all()
    return jsonify([category.to_dict() for category in categories])

@main.route('/api/tools/<int:category_id>')
def get_tools(category_id):
    """API endpoint to retrieve tools for a given category."""
    tools = Tool.query.filter_by(category_id=category_id).all()
    return jsonify([tool.to_dict() for tool in tools])