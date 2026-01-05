"""
Pytest configuration and fixtures for testing
"""
import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db, User


@pytest.fixture(scope='function')
def app():
    """Create application for testing"""
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def sample_user_data():
    """Sample user registration data"""
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'TestPass123!',
        'confirm_password': 'TestPass123!',
        'phone': '+919876543210',
        'user_type': 'buyer',
        'first_name': 'Test',
        'last_name': 'User'
    }


@pytest.fixture
def auth_user_data():
    """Separate user data for auth_headers fixture to avoid conflicts"""
    return {
        'username': 'authuser',
        'email': 'authuser@example.com',
        'password': 'AuthPass123!',
        'confirm_password': 'AuthPass123!',
        'phone': '+919876543211',
        'user_type': 'buyer',
        'first_name': 'Auth',
        'last_name': 'User'
    }


@pytest.fixture
def registered_user(app, client, sample_user_data):
    """Create a registered user and return user data with tokens"""
    response = client.post(
        '/auth/register',
        json=sample_user_data,
        content_type='application/json'
    )
    data = response.get_json()
    return {
        'user': data.get('user'),
        'access_token': data.get('access_token'),
        'refresh_token': data.get('refresh_token'),
        'password': sample_user_data['password'],
        'email': sample_user_data['email']
    }


@pytest.fixture
def admin_user(app):
    """Create an admin user"""
    with app.app_context():
        admin = User(
            username='adminuser',
            email='admin@example.com',
            phone='+919876543211',
            user_type='both',
            role='admin',
            is_active=True,
            is_verified=True,
            first_name='Admin',
            last_name='User'
        )
        admin.set_password('AdminPass123!')
        db.session.add(admin)
        db.session.commit()

        return {
            'id': admin.id,
            'email': 'admin@example.com',
            'password': 'AdminPass123!',
            'username': 'adminuser'
        }


@pytest.fixture
def admin_tokens(client, admin_user):
    """Get tokens for admin user"""
    response = client.post(
        '/auth/login',
        json={
            'email': admin_user['email'],
            'password': admin_user['password']
        },
        content_type='application/json'
    )
    data = response.get_json()
    return {
        'access_token': data.get('access_token'),
        'refresh_token': data.get('refresh_token')
    }


@pytest.fixture
def auth_headers(client, auth_user_data):
    """Get authorization headers for authenticated requests"""
    # Register fresh user and get tokens
    response = client.post(
        '/auth/register',
        json=auth_user_data,
        content_type='application/json'
    )
    data = response.get_json()
    return {
        'Authorization': f"Bearer {data['access_token']}",
        'Content-Type': 'application/json'
    }


@pytest.fixture
def admin_headers(client, admin_user):
    """Get authorization headers for admin requests"""
    # Login as admin and get tokens
    response = client.post(
        '/auth/login',
        json={
            'email': admin_user['email'],
            'password': admin_user['password']
        },
        content_type='application/json'
    )
    data = response.get_json()
    return {
        'Authorization': f"Bearer {data['access_token']}",
        'Content-Type': 'application/json'
    }
