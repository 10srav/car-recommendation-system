"""
Email Service for sending notifications
"""
from flask import current_app, render_template_string
from flask_mail import Mail, Message
from threading import Thread
import logging

mail = Mail()
logger = logging.getLogger(__name__)


def init_mail(app):
    """Initialize Flask-Mail with the app"""
    mail.init_app(app)


def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
            logger.info(f"Email sent successfully to {msg.recipients}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")


def send_email(subject, recipients, html_body, text_body=None, async_send=True):
    """
    Send an email

    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        html_body: HTML content of the email
        text_body: Plain text content (optional)
        async_send: Send asynchronously (default True)
    """
    app = current_app._get_current_object()

    msg = Message(
        subject=subject,
        recipients=recipients if isinstance(recipients, list) else [recipients],
        html=html_body,
        body=text_body or html_body
    )

    if async_send:
        Thread(target=send_async_email, args=(app, msg)).start()
    else:
        try:
            mail.send(msg)
            logger.info(f"Email sent successfully to {recipients}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False


# ==================== EMAIL TEMPLATES ====================

def send_welcome_email(user_email, username):
    """Send welcome email to new user"""
    subject = "Welcome to Indian Automotive Marketplace!"
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Auto Marketplace!</h1>
            </div>
            <div class="content">
                <h2>Hello {username}!</h2>
                <p>Thank you for joining the Indian Automotive Marketplace. We're excited to have you on board!</p>
                <p>With your new account, you can:</p>
                <ul>
                    <li>Get personalized car recommendations</li>
                    <li>Browse and list used cars</li>
                    <li>Get instant buy-back valuations</li>
                    <li>Compare cars and calculate EMIs</li>
                </ul>
                <p style="text-align: center;">
                    <a href="#" class="button">Explore Cars</a>
                </p>
                <p>If you have any questions, feel free to reach out to our support team.</p>
                <p>Happy car shopping!</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 Indian Automotive Marketplace. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    send_email(subject, user_email, html_body)


def send_valuation_email(customer_email, customer_name, valuation_data):
    """Send valuation results email"""
    subject = "Your Car Valuation Results - Auto Marketplace"
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .price-box {{ background: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .price {{ font-size: 28px; color: #28a745; font-weight: bold; }}
            .range {{ color: #666; font-size: 14px; }}
            .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .stat {{ text-align: center; }}
            .stat-value {{ font-size: 24px; color: #667eea; font-weight: bold; }}
            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your Car Valuation</h1>
            </div>
            <div class="content">
                <h2>Hello {customer_name}!</h2>
                <p>Thank you for using our car valuation service. Here are your results:</p>

                <div class="price-box">
                    <p class="range">Estimated Value Range</p>
                    <p class="price">₹{valuation_data.get('estimated_price_min', 0):,} - ₹{valuation_data.get('estimated_price_max', 0):,}</p>
                    <p><strong>Average Estimate: ₹{valuation_data.get('estimated_price_avg', 0):,}</strong></p>
                </div>

                <div style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <div style="font-size: 24px; color: #667eea; font-weight: bold;">{valuation_data.get('condition_score', 0)}/100</div>
                        <div>Condition Score</div>
                    </div>
                    <div>
                        <div style="font-size: 24px; color: #28a745; font-weight: bold;">{int(valuation_data.get('confidence_score', 0) * 100)}%</div>
                        <div>Confidence</div>
                    </div>
                </div>

                <p style="margin-top: 20px; padding: 15px; background: #e7f3ff; border-radius: 5px;">
                    <strong>Note:</strong> This is an AI-powered estimate. Final offer may vary after physical inspection.
                    Our team will contact you within 24 hours.
                </p>
            </div>
            <div class="footer">
                <p>&copy; 2024 Indian Automotive Marketplace. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    send_email(subject, customer_email, html_body)


def send_listing_confirmation_email(seller_email, seller_name, car_details, listing_id):
    """Send confirmation email when a car is listed"""
    subject = "Your Car Has Been Listed - Auto Marketplace"
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .car-details {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Listing Confirmed!</h1>
            </div>
            <div class="content">
                <h2>Hello {seller_name}!</h2>
                <p>Your car has been successfully listed on our marketplace.</p>

                <div class="car-details">
                    <h3>{car_details.get('brand', '')} {car_details.get('model', '')}</h3>
                    <p><strong>Year:</strong> {car_details.get('registration_year', '')}</p>
                    <p><strong>Price:</strong> ₹{car_details.get('current_price', 0):,}</p>
                    <p><strong>Listing ID:</strong> #{listing_id}</p>
                </div>

                <p>Potential buyers can now see your listing and contact you directly.</p>

                <p style="text-align: center;">
                    <a href="#" class="button">View Your Listing</a>
                </p>

                <p><strong>Tips for a quick sale:</strong></p>
                <ul>
                    <li>Respond to inquiries promptly</li>
                    <li>Be honest about the car's condition</li>
                    <li>Keep your service records handy</li>
                </ul>
            </div>
            <div class="footer">
                <p>&copy; 2024 Indian Automotive Marketplace. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    send_email(subject, seller_email, html_body)


def send_password_reset_email(user_email, username, reset_token):
    """Send password reset email"""
    subject = "Password Reset Request - Auto Marketplace"
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; background: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .warning {{ background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Password Reset</h1>
            </div>
            <div class="content">
                <h2>Hello {username}!</h2>
                <p>We received a request to reset your password. Click the button below to create a new password:</p>

                <p style="text-align: center;">
                    <a href="#" class="button">Reset Password</a>
                </p>

                <p>Or copy and paste this token: <code>{reset_token}</code></p>

                <div class="warning">
                    <strong>Note:</strong> This link will expire in 1 hour. If you didn't request a password reset, please ignore this email.
                </div>
            </div>
            <div class="footer">
                <p>&copy; 2024 Indian Automotive Marketplace. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    send_email(subject, user_email, html_body)
