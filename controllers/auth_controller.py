from flask import render_template, request, redirect, url_for, flash, session, current_app
from services.auth_service import AuthService

class AuthController:
    @staticmethod
    def show_login():
        if 'user_email' in session:
            return redirect(url_for('dashboard'))
        sent_email = request.args.get('sent_email')
        magic_token = request.args.get('token')
        return render_template('login.html', sent_email=sent_email, magic_token=magic_token)

    @staticmethod
    def send_magic_link():
        email = request.form.get('email')
        if not email or '@' not in email:
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for('login'))
        
        token = AuthService.generate_magic_link(email)
        flash(f"A secure authentication link has been issued for {email}.", "success")
        return redirect(url_for('login', sent_email=email, token=token))

    @staticmethod
    def verify_magic_link(token):
        email, error = AuthService.verify_token(token)
        if error:
            flash(error, "danger")
            return redirect(url_for('login'))
        
        session['user_email'] = email
        flash(f"Welcome back, {email}! You have successfully authenticated.", "success")
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard'))

    @staticmethod
    def logout():
        user = session.pop('user_email', None)
        flash("You have been safely signed out.", "info")
        return redirect(url_for('login'))
