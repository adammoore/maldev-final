"""
Entry point for running the Flask application.
"""

from app import create_app, db
from app.models import LifecycleStage, Substage, Tool

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'LifecycleStage': LifecycleStage, 'Substage': Substage, 'Tool': Tool}

if __name__ == '__main__':
    app.run(debug=True)
