"""
Unit tests for authentication routes
"""
import pytest
import json
from app.models import db, User


class TestUserRegistration:
    """Tests for user registration endpoint"""

    def test_register_success(self, client, sample_user_data):
        """Test successful user registration"""
        response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 201
        assert data['success'] is True
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['username'] == sample_user_data['username']
        assert data['user']['email'] == sample_user_data['email']

    def test_register_duplicate_email(self, client, sample_user_data, registered_user):
        """Test registration with duplicate email fails"""
        # Try to register with same email
        new_user_data = sample_user_data.copy()
        new_user_data['username'] = 'differentuser'

        response = client.post(
            '/auth/register',
            json=new_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 409
        assert data['success'] is False
        assert 'email' in data['errors']

    def test_register_duplicate_username(self, client, sample_user_data, registered_user):
        """Test registration with duplicate username fails"""
        new_user_data = sample_user_data.copy()
        new_user_data['email'] = 'different@example.com'

        response = client.post(
            '/auth/register',
            json=new_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 409
        assert data['success'] is False
        assert 'username' in data['errors']

    def test_register_weak_password_no_uppercase(self, client, sample_user_data):
        """Test registration fails with password missing uppercase"""
        sample_user_data['password'] = 'testpass123!'
        sample_user_data['confirm_password'] = 'testpass123!'

        response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False
        assert 'password' in data['errors']

    def test_register_weak_password_no_lowercase(self, client, sample_user_data):
        """Test registration fails with password missing lowercase"""
        sample_user_data['password'] = 'TESTPASS123!'
        sample_user_data['confirm_password'] = 'TESTPASS123!'

        response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    def test_register_weak_password_no_digit(self, client, sample_user_data):
        """Test registration fails with password missing digit"""
        sample_user_data['password'] = 'TestPassword!'
        sample_user_data['confirm_password'] = 'TestPassword!'

        response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    def test_register_weak_password_no_special(self, client, sample_user_data):
        """Test registration fails with password missing special char"""
        sample_user_data['password'] = 'TestPassword123'
        sample_user_data['confirm_password'] = 'TestPassword123'

        response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    def test_register_password_mismatch(self, client, sample_user_data):
        """Test registration fails when passwords don't match"""
        sample_user_data['confirm_password'] = 'DifferentPass123!'

        response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False
        assert 'confirm_password' in data['errors']

    def test_register_invalid_email(self, client, sample_user_data):
        """Test registration fails with invalid email format"""
        sample_user_data['email'] = 'invalid-email'

        response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False
        assert 'email' in data['errors']

    def test_register_short_username(self, client, sample_user_data):
        """Test registration fails with username too short"""
        sample_user_data['username'] = 'ab'

        response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False
        assert 'username' in data['errors']

    def test_register_invalid_username_chars(self, client, sample_user_data):
        """Test registration fails with invalid characters in username"""
        sample_user_data['username'] = 'test@user!'

        response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    def test_register_missing_required_fields(self, client):
        """Test registration fails with missing required fields"""
        response = client.post(
            '/auth/register',
            json={},
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False
        assert 'username' in data['errors'] or 'email' in data['errors']


class TestUserLogin:
    """Tests for user login endpoint"""

    def test_login_success(self, client, registered_user):
        """Test successful login"""
        response = client.post(
            '/auth/login',
            json={
                'email': registered_user['email'],
                'password': registered_user['password']
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['email'] == registered_user['email']

    def test_login_with_remember_me(self, client, registered_user):
        """Test login with remember_me option"""
        response = client.post(
            '/auth/login',
            json={
                'email': registered_user['email'],
                'password': registered_user['password'],
                'remember_me': True
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert 'access_token' in data

    def test_login_wrong_password(self, client, registered_user):
        """Test login with wrong password fails"""
        response = client.post(
            '/auth/login',
            json={
                'email': registered_user['email'],
                'password': 'WrongPassword123!'
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 401
        assert data['success'] is False
        assert 'Invalid email or password' in data['error']

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email fails"""
        response = client.post(
            '/auth/login',
            json={
                'email': 'nonexistent@example.com',
                'password': 'SomePassword123!'
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 401
        assert data['success'] is False

    def test_login_invalid_email_format(self, client):
        """Test login with invalid email format fails"""
        response = client.post(
            '/auth/login',
            json={
                'email': 'invalid-email',
                'password': 'SomePassword123!'
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    def test_login_account_lockout(self, app, client, registered_user):
        """Test account gets locked after multiple failed attempts"""
        # Attempt 5 failed logins
        for i in range(5):
            response = client.post(
                '/auth/login',
                json={
                    'email': registered_user['email'],
                    'password': 'WrongPassword123!'
                },
                content_type='application/json'
            )

        # 6th attempt should show locked
        response = client.post(
            '/auth/login',
            json={
                'email': registered_user['email'],
                'password': 'WrongPassword123!'
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 403
        assert 'locked' in data['error'].lower()

    def test_login_deactivated_account(self, app, client, sample_user_data):
        """Test login fails for deactivated account"""
        # Register user first
        client.post('/auth/register', json=sample_user_data, content_type='application/json')

        # Deactivate user
        with app.app_context():
            user = User.query.filter_by(email=sample_user_data['email']).first()
            user.is_active = False
            db.session.commit()

        # Try to login
        response = client.post(
            '/auth/login',
            json={
                'email': sample_user_data['email'],
                'password': sample_user_data['password']
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 403
        assert data['success'] is False
        assert 'deactivated' in data['error'].lower()


class TestTokenRefresh:
    """Tests for token refresh endpoint"""

    def test_refresh_token_success(self, client, registered_user):
        """Test successful token refresh"""
        response = client.post(
            '/auth/refresh',
            headers={
                'Authorization': f"Bearer {registered_user['refresh_token']}"
            }
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert 'access_token' in data

    def test_refresh_with_access_token_fails(self, client, registered_user):
        """Test refresh fails when using access token instead of refresh token"""
        response = client.post(
            '/auth/refresh',
            headers={
                'Authorization': f"Bearer {registered_user['access_token']}"
            }
        )

        # Should fail because access token is not a refresh token
        assert response.status_code == 422 or response.status_code == 401

    def test_refresh_without_token_fails(self, client):
        """Test refresh fails without token"""
        response = client.post('/auth/refresh')
        data = response.get_json()

        assert response.status_code == 401
        assert data['success'] is False

    def test_refresh_with_invalid_token_fails(self, client):
        """Test refresh fails with invalid token"""
        response = client.post(
            '/auth/refresh',
            headers={
                'Authorization': 'Bearer invalid-token-here'
            }
        )
        data = response.get_json()

        assert response.status_code == 422 or response.status_code == 401
        assert data['success'] is False


class TestUserProfile:
    """Tests for profile endpoints"""

    def test_get_profile_success(self, client, auth_headers, auth_user_data):
        """Test getting user profile"""
        response = client.get('/auth/profile', headers=auth_headers)
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert data['user']['email'] == auth_user_data['email']

    def test_get_profile_unauthorized(self, client):
        """Test getting profile without auth fails"""
        response = client.get('/auth/profile')
        data = response.get_json()

        assert response.status_code == 401
        assert data['success'] is False

    def test_update_profile_success(self, client, auth_headers):
        """Test updating user profile"""
        response = client.put(
            '/auth/profile',
            headers=auth_headers,
            json={
                'first_name': 'Updated',
                'last_name': 'Name',
                'phone': '+919999999999'
            }
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert data['user']['first_name'] == 'Updated'
        assert data['user']['last_name'] == 'Name'

    def test_update_profile_change_username(self, client, auth_headers):
        """Test changing username"""
        response = client.put(
            '/auth/profile',
            headers=auth_headers,
            json={'username': 'newusername'}
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert data['user']['username'] == 'newusername'

    def test_update_profile_duplicate_username(self, app, client, auth_headers, admin_user):
        """Test changing to existing username fails"""
        response = client.put(
            '/auth/profile',
            headers=auth_headers,
            json={'username': admin_user['username']}
        )
        data = response.get_json()

        assert response.status_code == 409
        assert data['success'] is False
        assert 'username' in data['errors']

    def test_update_profile_invalid_username(self, client, auth_headers):
        """Test updating with invalid username fails"""
        response = client.put(
            '/auth/profile',
            headers=auth_headers,
            json={'username': 'ab'}  # Too short
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    def test_update_profile_unauthorized(self, client):
        """Test updating profile without auth fails"""
        response = client.put(
            '/auth/profile',
            json={'first_name': 'Test'},
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 401
        assert data['success'] is False


class TestPasswordChange:
    """Tests for password change endpoint"""

    def test_change_password_success(self, client, auth_headers, auth_user_data):
        """Test successful password change"""
        response = client.post(
            '/auth/change-password',
            headers=auth_headers,
            json={
                'current_password': auth_user_data['password'],
                'new_password': 'NewSecurePass123!',
                'confirm_new_password': 'NewSecurePass123!'
            }
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True

        # Verify can login with new password
        login_response = client.post(
            '/auth/login',
            json={
                'email': auth_user_data['email'],
                'password': 'NewSecurePass123!'
            },
            content_type='application/json'
        )
        assert login_response.status_code == 200

    def test_change_password_wrong_current(self, client, auth_headers):
        """Test password change fails with wrong current password"""
        response = client.post(
            '/auth/change-password',
            headers=auth_headers,
            json={
                'current_password': 'WrongPassword123!',
                'new_password': 'NewSecurePass123!',
                'confirm_new_password': 'NewSecurePass123!'
            }
        )
        data = response.get_json()

        assert response.status_code == 401
        assert data['success'] is False
        assert 'incorrect' in data['error'].lower()

    def test_change_password_mismatch(self, client, auth_headers, auth_user_data):
        """Test password change fails when new passwords don't match"""
        response = client.post(
            '/auth/change-password',
            headers=auth_headers,
            json={
                'current_password': auth_user_data['password'],
                'new_password': 'NewSecurePass123!',
                'confirm_new_password': 'DifferentPass123!'
            }
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    def test_change_password_same_as_current(self, client, auth_headers, auth_user_data):
        """Test password change fails when new password same as current"""
        response = client.post(
            '/auth/change-password',
            headers=auth_headers,
            json={
                'current_password': auth_user_data['password'],
                'new_password': auth_user_data['password'],
                'confirm_new_password': auth_user_data['password']
            }
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False
        assert 'different' in data['error'].lower()

    def test_change_password_weak_new_password(self, client, auth_headers, auth_user_data):
        """Test password change fails with weak new password"""
        response = client.post(
            '/auth/change-password',
            headers=auth_headers,
            json={
                'current_password': auth_user_data['password'],
                'new_password': 'weak',
                'confirm_new_password': 'weak'
            }
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    def test_change_password_unauthorized(self, client):
        """Test password change without auth fails"""
        response = client.post(
            '/auth/change-password',
            json={
                'current_password': 'any',
                'new_password': 'NewSecurePass123!',
                'confirm_new_password': 'NewSecurePass123!'
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 401
        assert data['success'] is False


class TestLogout:
    """Tests for logout endpoint"""

    def test_logout_success(self, client, auth_headers):
        """Test successful logout"""
        response = client.post('/auth/logout', headers=auth_headers)
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True

    def test_logout_unauthorized(self, client):
        """Test logout without auth fails"""
        response = client.post('/auth/logout')
        data = response.get_json()

        assert response.status_code == 401
        assert data['success'] is False


class TestAdminEndpoints:
    """Tests for admin-only endpoints"""

    def test_list_users_as_admin(self, client, admin_headers, registered_user):
        """Test admin can list users"""
        response = client.get('/auth/admin/users', headers=admin_headers)
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert 'users' in data
        assert 'pagination' in data
        assert len(data['users']) >= 1

    def test_list_users_as_regular_user(self, client, auth_headers):
        """Test regular user cannot list users"""
        response = client.get('/auth/admin/users', headers=auth_headers)
        data = response.get_json()

        assert response.status_code == 403
        assert 'admin' in data['error'].lower()

    def test_list_users_unauthorized(self, client):
        """Test listing users without auth fails"""
        response = client.get('/auth/admin/users')
        data = response.get_json()

        assert response.status_code == 401
        assert data['success'] is False

    def test_toggle_user_active_as_admin(self, app, client, admin_headers, sample_user_data):
        """Test admin can toggle user active status"""
        # Create a user to toggle
        client.post('/auth/register', json=sample_user_data, content_type='application/json')

        with app.app_context():
            user = User.query.filter_by(email=sample_user_data['email']).first()
            user_id = user.id

        response = client.post(
            f'/auth/admin/users/{user_id}/toggle-active',
            headers=admin_headers
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert data['user']['is_active'] is False  # Was True, now False

    def test_toggle_user_active_as_regular_user(self, client, auth_headers):
        """Test regular user cannot toggle user status"""
        response = client.post(
            '/auth/admin/users/1/toggle-active',
            headers=auth_headers
        )
        data = response.get_json()

        assert response.status_code == 403

    def test_admin_cannot_deactivate_self(self, app, client, admin_headers, admin_user):
        """Test admin cannot deactivate their own account"""
        response = client.post(
            f'/auth/admin/users/{admin_user["id"]}/toggle-active',
            headers=admin_headers
        )
        data = response.get_json()

        assert response.status_code == 400
        assert 'own account' in data['error'].lower()

    def test_unlock_user_as_admin(self, app, client, admin_headers, sample_user_data):
        """Test admin can unlock a locked user"""
        # Create and lock a user
        client.post('/auth/register', json=sample_user_data, content_type='application/json')

        with app.app_context():
            user = User.query.filter_by(email=sample_user_data['email']).first()
            user.failed_login_attempts = 5
            from datetime import datetime, timedelta
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            db.session.commit()
            user_id = user.id

        # Admin unlocks the user
        response = client.post(
            f'/auth/admin/users/{user_id}/unlock',
            headers=admin_headers
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True

        # Verify user can now login
        login_response = client.post(
            '/auth/login',
            json={
                'email': sample_user_data['email'],
                'password': sample_user_data['password']
            },
            content_type='application/json'
        )
        assert login_response.status_code == 200

    def test_unlock_user_as_regular_user(self, client, auth_headers):
        """Test regular user cannot unlock users"""
        response = client.post(
            '/auth/admin/users/1/unlock',
            headers=auth_headers
        )
        data = response.get_json()

        assert response.status_code == 403


class TestClientIP:
    """Tests for client IP detection"""

    def test_login_records_direct_ip(self, client, sample_user_data):
        """Test login records IP when no X-Forwarded-For header"""
        # Register user first
        client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )

        # Login without X-Forwarded-For header (uses remote_addr)
        response = client.post(
            '/auth/login',
            json={
                'email': sample_user_data['email'],
                'password': sample_user_data['password']
            },
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_login_records_forwarded_ip(self, client, sample_user_data):
        """Test login records IP from X-Forwarded-For header"""
        # Register user first
        client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )

        # Login with X-Forwarded-For header
        response = client.post(
            '/auth/login',
            json={
                'email': sample_user_data['email'],
                'password': sample_user_data['password']
            },
            content_type='application/json',
            headers={'X-Forwarded-For': '203.0.113.195, 70.41.3.18'}
        )

        assert response.status_code == 200


class TestInputValidation:
    """Tests for input validation edge cases"""

    def test_register_with_empty_json(self, client):
        """Test registration with empty JSON"""
        response = client.post(
            '/auth/register',
            json={},
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    def test_login_with_empty_json(self, client):
        """Test login with empty JSON"""
        response = client.post(
            '/auth/login',
            json={},
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    def test_register_phone_validation(self, client, sample_user_data):
        """Test phone number validation"""
        sample_user_data['phone'] = 'invalid-phone'

        response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    def test_register_user_type_validation(self, client, sample_user_data):
        """Test user_type must be valid option"""
        sample_user_data['user_type'] = 'invalid_type'

        response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False


class TestActiveUserRequired:
    """Tests for active_user_required decorator edge cases"""

    def test_deleted_user_cannot_access_profile(self, app, client, sample_user_data):
        """Test deleted user (with valid token) cannot access protected endpoints"""
        # Register user and get tokens
        reg_response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        tokens = reg_response.get_json()
        access_token = tokens['access_token']

        # Delete the user from database
        with app.app_context():
            user = User.query.filter_by(email=sample_user_data['email']).first()
            db.session.delete(user)
            db.session.commit()

        # Try to access profile with token for deleted user
        response = client.get(
            '/auth/profile',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        data = response.get_json()

        assert response.status_code == 404
        assert 'not found' in data['error'].lower()

    def test_deactivated_user_cannot_access_profile(self, app, client, sample_user_data):
        """Test deactivated user cannot access protected endpoints"""
        # Register user and get tokens
        reg_response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        tokens = reg_response.get_json()
        access_token = tokens['access_token']

        # Deactivate the user
        with app.app_context():
            user = User.query.filter_by(email=sample_user_data['email']).first()
            user.is_active = False
            db.session.commit()

        # Try to access profile with deactivated account
        response = client.get(
            '/auth/profile',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        data = response.get_json()

        assert response.status_code == 403
        assert 'deactivated' in data['error'].lower()

    def test_locked_user_cannot_access_profile(self, app, client, sample_user_data):
        """Test locked user cannot access protected endpoints"""
        # Register user and get tokens
        reg_response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        tokens = reg_response.get_json()
        access_token = tokens['access_token']

        # Lock the user
        with app.app_context():
            from datetime import datetime, timedelta
            user = User.query.filter_by(email=sample_user_data['email']).first()
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            db.session.commit()

        # Try to access profile with locked account
        response = client.get(
            '/auth/profile',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        data = response.get_json()

        assert response.status_code == 403
        assert 'locked' in data['error'].lower()

    def test_deactivated_user_cannot_update_profile(self, app, client, sample_user_data):
        """Test deactivated user cannot update profile"""
        # Register user and get tokens
        reg_response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        tokens = reg_response.get_json()
        access_token = tokens['access_token']

        # Deactivate the user
        with app.app_context():
            user = User.query.filter_by(email=sample_user_data['email']).first()
            user.is_active = False
            db.session.commit()

        # Try to update profile with deactivated account
        response = client.put(
            '/auth/profile',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            },
            json={'first_name': 'Updated'}
        )
        data = response.get_json()

        assert response.status_code == 403
        assert 'deactivated' in data['error'].lower()

    def test_locked_user_cannot_change_password(self, app, client, sample_user_data):
        """Test locked user cannot change password"""
        # Register user and get tokens
        reg_response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        tokens = reg_response.get_json()
        access_token = tokens['access_token']

        # Lock the user
        with app.app_context():
            from datetime import datetime, timedelta
            user = User.query.filter_by(email=sample_user_data['email']).first()
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            db.session.commit()

        # Try to change password with locked account
        response = client.post(
            '/auth/change-password',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            },
            json={
                'current_password': sample_user_data['password'],
                'new_password': 'NewSecure123!',
                'confirm_new_password': 'NewSecure123!'
            }
        )
        data = response.get_json()

        assert response.status_code == 403
        assert 'locked' in data['error'].lower()


class TestTokenRefreshEdgeCases:
    """Tests for token refresh edge cases"""

    def test_refresh_token_deactivated_user(self, app, client, sample_user_data):
        """Test token refresh fails for deactivated user"""
        # Register user and get tokens
        reg_response = client.post(
            '/auth/register',
            json=sample_user_data,
            content_type='application/json'
        )
        tokens = reg_response.get_json()
        refresh_token = tokens['refresh_token']

        # Deactivate the user after they have a refresh token
        with app.app_context():
            user = User.query.filter_by(email=sample_user_data['email']).first()
            user.is_active = False
            db.session.commit()

        # Try to refresh token with deactivated account
        response = client.post(
            '/auth/refresh',
            headers={
                'Authorization': f'Bearer {refresh_token}',
                'Content-Type': 'application/json'
            }
        )
        data = response.get_json()

        assert response.status_code == 401
        assert 'invalid' in data['error'].lower()
