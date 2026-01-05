"""
Authentication routes and JWT token management
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt, current_user
)
from datetime import datetime, timedelta
from functools import wraps

from app.models import db, User
from app.schemas import (
    user_registration_schema, user_login_schema,
    user_update_schema, password_change_schema
)
from app import limiter, csrf
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Exempt API routes from CSRF (they use JWT authentication)
# CSRF is still required for form submissions


# ==================== HELPER FUNCTIONS ====================

def get_client_ip():
    """Get client IP address, handling proxies"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr


def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper


def active_user_required(fn):
    """Decorator to require active (non-locked) user"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({'error': 'User not found'}), 404
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        if user.is_locked():
            return jsonify({'error': 'Account is temporarily locked'}), 403
        return fn(*args, **kwargs)
    return wrapper


# ==================== API ROUTES ====================

@auth_bp.route('/register', methods=['POST'])
@csrf.exempt
@limiter.limit("5 per hour")
def register():
    """Register a new user"""
    try:
        # Validate input
        data = user_registration_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'success': False, 'errors': err.messages}), 400

    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'success': False,
            'errors': {'email': ['Email already registered']}
        }), 409

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'success': False,
            'errors': {'username': ['Username already taken']}
        }), 409

    try:
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            phone=data.get('phone'),
            user_type=data.get('user_type', 'buyer'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role='user',
            is_active=True,
            is_verified=False
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        # Create tokens (identity must be a string for PyJWT compatibility)
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role, 'user_type': user.user_type}
        )
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': user.to_dict(include_private=True),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Registration failed. Please try again.'
        }), 500


@auth_bp.route('/login', methods=['POST'])
@csrf.exempt
@limiter.limit("10 per minute")
def login():
    """Login user and return JWT tokens"""
    try:
        data = user_login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'success': False, 'errors': err.messages}), 400

    user = User.query.filter_by(email=data['email']).first()

    # Check if user exists
    if not user:
        return jsonify({
            'success': False,
            'error': 'Invalid email or password'
        }), 401

    # Check if account is locked
    if user.is_locked():
        remaining = (user.locked_until - datetime.utcnow()).seconds // 60
        return jsonify({
            'success': False,
            'error': f'Account is locked. Try again in {remaining} minutes.'
        }), 403

    # Check if account is active
    if not user.is_active:
        return jsonify({
            'success': False,
            'error': 'Account is deactivated. Contact support.'
        }), 403

    # Verify password
    if not user.check_password(data['password']):
        user.increment_failed_login()
        db.session.commit()

        attempts_left = 5 - user.failed_login_attempts
        if attempts_left > 0:
            return jsonify({
                'success': False,
                'error': f'Invalid email or password. {attempts_left} attempts remaining.'
            }), 401
        else:
            return jsonify({
                'success': False,
                'error': 'Account locked due to too many failed attempts.'
            }), 403

    # Successful login
    user.reset_failed_login()
    user.last_login = datetime.utcnow()
    user.last_login_ip = get_client_ip()
    db.session.commit()

    # Token expiry based on remember_me
    expires = timedelta(days=30) if data.get('remember_me') else timedelta(hours=1)

    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=expires,
        additional_claims={'role': user.role, 'user_type': user.user_type}
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        expires_delta=timedelta(days=30)
    )

    return jsonify({
        'success': True,
        'message': 'Login successful',
        'user': user.to_dict(include_private=True),
        'access_token': access_token,
        'refresh_token': refresh_token
    })


@auth_bp.route('/refresh', methods=['POST'])
@csrf.exempt
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user or not user.is_active:
        return jsonify({'error': 'Invalid user'}), 401

    access_token = create_access_token(
        identity=str(user_id),
        additional_claims={'role': user.role, 'user_type': user.user_type}
    )

    return jsonify({
        'success': True,
        'access_token': access_token
    })


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
@active_user_required
def get_profile():
    """Get current user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    return jsonify({
        'success': True,
        'user': user.to_dict(include_private=True)
    })


@auth_bp.route('/profile', methods=['PUT'])
@csrf.exempt
@jwt_required()
@active_user_required
@limiter.limit("10 per hour")
def update_profile():
    """Update user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    try:
        data = user_update_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'success': False, 'errors': err.messages}), 400

    # Check username uniqueness if changing
    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'success': False,
                'errors': {'username': ['Username already taken']}
            }), 409

    try:
        # Update fields
        for key, value in data.items():
            setattr(user, key, value)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': user.to_dict(include_private=True)
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Update failed. Please try again.'
        }), 500


@auth_bp.route('/change-password', methods=['POST'])
@csrf.exempt
@jwt_required()
@active_user_required
@limiter.limit("5 per hour")
def change_password():
    """Change user password"""
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    try:
        data = password_change_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'success': False, 'errors': err.messages}), 400

    # Verify current password
    if not user.check_password(data['current_password']):
        return jsonify({
            'success': False,
            'error': 'Current password is incorrect'
        }), 401

    # Check new password is different
    if user.check_password(data['new_password']):
        return jsonify({
            'success': False,
            'error': 'New password must be different from current password'
        }), 400

    try:
        user.set_password(data['new_password'])
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Password change failed. Please try again.'
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@csrf.exempt
@jwt_required()
def logout():
    """Logout user (client should discard tokens)"""
    # In a production system, you'd add the token to a blocklist
    # For now, we just return success and client discards tokens
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })


# ==================== ADMIN ROUTES ====================

@auth_bp.route('/admin/users', methods=['GET'])
@admin_required
def list_users():
    """List all users (admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'success': True,
        'users': [u.to_dict(include_private=True) for u in users.items],
        'pagination': {
            'page': users.page,
            'pages': users.pages,
            'total': users.total,
            'has_next': users.has_next,
            'has_prev': users.has_prev
        }
    })


@auth_bp.route('/admin/users/<int:user_id>/toggle-active', methods=['POST'])
@csrf.exempt
@admin_required
@limiter.limit("20 per hour")
def toggle_user_active(user_id):
    """Activate or deactivate a user (admin only)"""
    user = User.query.get_or_404(user_id)

    # Prevent admin from deactivating themselves
    current_user_id = int(get_jwt_identity())
    if user_id == current_user_id:
        return jsonify({
            'success': False,
            'error': 'Cannot deactivate your own account'
        }), 400

    user.is_active = not user.is_active
    db.session.commit()

    status = 'activated' if user.is_active else 'deactivated'
    return jsonify({
        'success': True,
        'message': f'User {status} successfully',
        'user': user.to_dict(include_private=True)
    })


@auth_bp.route('/admin/users/<int:user_id>/unlock', methods=['POST'])
@csrf.exempt
@admin_required
def unlock_user(user_id):
    """Unlock a locked user account (admin only)"""
    user = User.query.get_or_404(user_id)

    user.reset_failed_login()
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'User account unlocked successfully'
    })


# ==================== WEB ROUTES (for templates) ====================

@auth_bp.route('/login-page')
def login_page():
    """Render login page"""
    return render_template('auth/login.html')


@auth_bp.route('/register-page')
def register_page():
    """Render registration page"""
    return render_template('auth/register.html')


@auth_bp.route('/profile-page')
def profile_page():
    """Render profile page"""
    return render_template('auth/profile.html')
