import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import session, redirect, url_for, flash, request, current_app
from db import get_db

class AuthService:
    TOKEN_EXPIRATION_MINUTES = 15

    @staticmethod
    def generate_magic_link(email, app=None):
        app_obj = app or current_app
        db = get_db(app_obj)
        token = secrets.token_urlsafe(32)
        now = datetime.utcnow()
        expires_at = now + timedelta(minutes=AuthService.TOKEN_EXPIRATION_MINUTES)
        
        doc = {
            "email": email.strip().lower(),
            "token": token,
            "created_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
            "used": False
        }
        
        db.magic_links.insert_one(doc)
        return token

    @staticmethod
    def verify_token(token, app=None):
        app_obj = app or current_app
        db = get_db(app_obj)
        link = db.magic_links.find_one({"token": token, "used": False})
        
        if not link:
            return None, "Invalid or already used authentication link."
        
        expires_at = datetime.fromisoformat(link["expires_at"])
        if datetime.utcnow() > expires_at:
            return None, "Authentication link has expired. Please request a new one."
        
        # Mark token as used
        db.magic_links.update_one({"_id": link["_id"]}, {"$set": {"used": True, "used_at": datetime.utcnow().isoformat()}})
        return link["email"], None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash("Please sign in with your email link to access InsureAI.", "warning")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
