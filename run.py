# Main file to run the Flask app
# Run this file: python run.py

from app import create_app
from app.models import db

app = create_app('development')

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

    print("\n" + "="*60)
    print("MyCar - Starting Server")
    print("="*60)
    print("\nAccess the application at: http://127.0.0.1:5000")
    print("\nPress CTRL+C to stop the server\n")

    # Start the Flask development server
    # For production, use a proper WSGI server like gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)
