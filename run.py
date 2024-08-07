"""
Entry point for running the Flask application.
"""
import sys
print("Python version:", sys.version)
print("Python path:", sys.path)

try:
    from app import create_app
    print("Successfully imported create_app")
except ImportError as e:
    print("Failed to import create_app")
    print("Error:", str(e))
    print("Traceback:")
    import traceback
    traceback.print_exc()
    sys.exit(1)

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'LifecycleStage': LifecycleStage, 'Substage': Substage, 'Tool': Tool}

if __name__ == '__main__':
    app.run(debug=True)
