import os
from flask import Flask, render_template, redirect, url_for, flash, session

from config import Config
from db import get_db
from services.seed_data import seed_initial_data
from services.auth_service import login_required

from controllers.auth_controller import AuthController
from controllers.document_controller import DocumentController
from controllers.onboarding_controller import OnboardingController
from controllers.data_quality_controller import DataQualityController
from controllers.analytics_controller import AnalyticsController

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    db = get_db(app)
    if db.documents.count_documents({}) == 0:
        seed_initial_data(db)
    return db

# Inject role into all templates
@app.context_processor
def inject_role():
    email = session.get('user_email', '')
    is_linar = email.lower().endswith('@linar.co.za') or email.lower() == 'admin'
    return dict(is_linar=is_linar)

# --- Authentication Routes ---

@app.route('/login')
def login():
    return AuthController.show_login()

@app.route('/send-magic-link', methods=['POST'])
def send_magic_link():
    return AuthController.send_magic_link()

@app.route('/auth/magic-link/<token>')
def verify_magic_link(token):
    return AuthController.verify_magic_link(token)

@app.route('/logout')
def logout():
    return AuthController.logout()

# --- MVC Protected Routes & Endpoints ---

@app.route('/')
def index():
    if 'user_email' in session:
        email = session.get('user_email', '')
        if email.lower().endswith('@linar.co.za'):
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('onboarding'))
    return redirect(url_for('login'))

@app.route('/onboarding')
@login_required
def onboarding():
    return OnboardingController.show_onboarding_form()

@app.route('/api/upload-document', methods=['POST'])
@login_required
def upload_document():
    return OnboardingController.process_document_upload_ajax()

@app.route('/api/complete-liveness/<doc_id>', methods=['POST'])
@login_required
def complete_liveness(doc_id):
    return OnboardingController.complete_liveness_ajax(doc_id)

@app.route('/dashboard')
@login_required
def dashboard():
    email = session.get('user_email', '')
    if not (email.lower().endswith('@linar.co.za') or email.lower() == 'admin'):
        flash('Brokers only have access to the onboarding portal.', 'warning')
        return redirect(url_for('onboarding'))
    init_db()
    return DocumentController.show_dashboard()

@app.route('/verify/<doc_id>')
@login_required
def visual_verification(doc_id):
    email = session.get('user_email', '')
    if not (email.lower().endswith('@linar.co.za') or email.lower() == 'admin'):
        return redirect(url_for('onboarding'))
    init_db()
    return DocumentController.show_visual_verification(doc_id)

@app.route('/api/verify/<doc_id>', methods=['POST'])
@login_required
def api_verify(doc_id):
    return DocumentController.update_verification_status(doc_id)

@app.route('/data-quality')
@login_required
def data_quality():
    email = session.get('user_email', '')
    if not (email.lower().endswith('@linar.co.za') or email.lower() == 'admin'):
        return redirect(url_for('onboarding'))
    init_db()
    return DataQualityController.show_data_quality_portal()

@app.route('/analytics')
@login_required
def analytics():
    email = session.get('user_email', '')
    if not (email.lower().endswith('@linar.co.za') or email.lower() == 'admin'):
        return redirect(url_for('onboarding'))
    return AnalyticsController.show_analytics_dashboard()

@app.route('/seed')
@login_required
def seed_data_route():
    db = get_db(app)
    seed_initial_data(db)
    flash("Initial demo dataset re-seeded successfully!", "info")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)
