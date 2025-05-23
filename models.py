from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128))
    subscription_type = db.Column(db.String(20), default='free')  # free, pro, business
    subscription_reference = db.Column(db.String(100))  # Paystack reference
    subscription_expires = db.Column(db.DateTime)
    presentations = db.relationship('Presentation', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_subscription_active(self):
        if self.subscription_type == 'free':
            return True
        return bool(self.subscription_expires and self.subscription_expires > datetime.utcnow())

class Presentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SubscriptionPlan:
    PLANS = {
        'free': {
            'name': 'Starter',
            'price': 0,
            'currency': 'USD',
            'max_slides': 3,
            'presentations_limit': 3,  # per week
            'features': ['Basic themes', 'PPTX download', 'Watermark']
        },
        'pro': {
            'name': 'Creator',
            'price': 999,  # $9.99 (in cents)
            'currency': 'USD',
            'max_slides': 10,
            'presentations_limit': 20,  # per month
            'features': ['Premium themes', 'No watermark', 'PPTX + PDF export', 'Priority support']
        },
        'business': {
            'name': 'Professional',
            'price': 2499,  # $24.99 (in cents)
            'currency': 'USD',
            'max_slides': 30,
            'presentations_limit': 50,  # per month
            'features': ['Custom branding', 'Team sharing', 'Analytics dashboard', 'All Pro features']
        }
    }
