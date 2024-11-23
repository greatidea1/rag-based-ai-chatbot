from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Ensure the template and static directories exist
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    
    # Create directories if they don't exist
    os.makedirs(template_dir, exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)
    
    app.run(debug=True, port=5000)