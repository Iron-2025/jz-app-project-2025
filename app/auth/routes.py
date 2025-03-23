from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app.core.models import User
from app.core.db import get_db
from . import auth
from .forms import LoginForm, RegistrationForm, EditProfileForm, ChangePasswordForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    # Redirect if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Get user by email
        user = User.get_by_email(form.email.data)
        
        # Check if user exists and password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        # Log in the user
        login_user(user, remember=form.remember_me.data)
        
        # Redirect to the next page or index
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('core.index')
        
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@auth.route('/logout')
def logout():
    """User logout route."""
    logout_user()
    return redirect(url_for('core.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    # Redirect if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user
        user = User.create(
            email=form.email.data,
            password=form.password.data,
            name=form.name.data
        )
        
        if user is None:
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/profile')
@login_required
def profile():
    """User profile route."""
    # Get job application statistics
    db = get_db()
    
    # Total job applications
    job_count = db.execute(
        'SELECT COUNT(*) as count FROM job_application WHERE user_id = ?',
        (current_user.id,)
    ).fetchone()['count']
    
    # Active applications (not rejected)
    active_count = db.execute(
        'SELECT COUNT(*) as count FROM job_application WHERE user_id = ? AND status != ?',
        (current_user.id, 'Rejected')
    ).fetchone()['count']
    
    # Success rate (offers / total)
    offers_count = db.execute(
        'SELECT COUNT(*) as count FROM job_application WHERE user_id = ? AND (status = ? OR status = ?)',
        (current_user.id, 'Offer', 'Accepted')
    ).fetchone()['count']
    
    success_rate = '0%'
    if job_count > 0:
        success_rate = f"{(offers_count / job_count) * 100:.1f}%"
    
    return render_template(
        'auth/profile.html', 
        title='Profile',
        job_count=job_count,
        active_count=active_count,
        success_rate=success_rate
    )

@auth.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile route."""
    form = EditProfileForm(original_email=current_user.email)
    
    if form.validate_on_submit():
        # Update user profile
        success, message = current_user.update_profile(
            name=form.name.data,
            email=form.email.data
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash(message, 'danger')
    
    # Pre-populate form with current user data
    if request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    
    return render_template('auth/edit_profile.html', title='Edit Profile', form=form)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password route."""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Change user password
        success, message = current_user.change_password(
            current_password=form.current_password.data,
            new_password=form.new_password.data
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash(message, 'danger')
    
    return render_template('auth/change_password.html', title='Change Password', form=form)
