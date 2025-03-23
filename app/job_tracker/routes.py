from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from app.core.db import get_db
from . import job_tracker

@job_tracker.route('/')
@login_required
def index():
    """Job Application Tracker main page."""
    return render_template('job_tracker/index.html')

@job_tracker.route('/api/applications', methods=['GET'])
@login_required
def get_applications():
    """Get all job applications for the current user."""
    db = get_db()
    applications = db.execute(
        'SELECT * FROM job_application WHERE user_id = ? ORDER BY date_applied DESC',
        (current_user.id,)
    ).fetchall()
    
    # Convert to list of dictionaries
    result = []
    for app in applications:
        result.append({
            'id': app['id'],
            'company': app['company'],
            'role': app['role'],
            'date_applied': app['date_applied'],
            'status': app['status'],
            'notes': app['notes']
        })
    
    return jsonify(result)

@job_tracker.route('/api/applications', methods=['POST'])
@login_required
def add_application():
    """Add a new job application for the current user."""
    data = request.json
    
    if not data or not all(k in data for k in ('company', 'role', 'date_applied', 'status')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = get_db()
    cursor = db.execute(
        'INSERT INTO job_application (user_id, company, role, date_applied, status, notes) VALUES (?, ?, ?, ?, ?, ?)',
        (current_user.id, data['company'], data['role'], data['date_applied'], data['status'], data.get('notes', ''))
    )
    db.commit()
    
    return jsonify({'id': cursor.lastrowid, **data}), 201

@job_tracker.route('/api/applications/<int:id>', methods=['PUT'])
@login_required
def update_application(id):
    """Update an existing job application."""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    db = get_db()
    
    # Get current application data and verify ownership
    current = db.execute(
        'SELECT * FROM job_application WHERE id = ? AND user_id = ?',
        (id, current_user.id)
    ).fetchone()
    
    if current is None:
        return jsonify({'error': 'Application not found or access denied'}), 404
    
    # Update fields that are provided
    company = data.get('company', current['company'])
    role = data.get('role', current['role'])
    date_applied = data.get('date_applied', current['date_applied'])
    status = data.get('status', current['status'])
    notes = data.get('notes', current['notes'])
    
    db.execute(
        'UPDATE job_application SET company = ?, role = ?, date_applied = ?, status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (company, role, date_applied, status, notes, id)
    )
    db.commit()
    
    return jsonify({
        'id': id,
        'company': company,
        'role': role,
        'date_applied': date_applied,
        'status': status,
        'notes': notes
    })

@job_tracker.route('/api/applications/<int:id>', methods=['DELETE'])
@login_required
def delete_application(id):
    """Delete a job application."""
    db = get_db()
    
    # Verify ownership before deleting
    if db.execute(
        'SELECT id FROM job_application WHERE id = ? AND user_id = ?',
        (id, current_user.id)
    ).fetchone() is None:
        return jsonify({'error': 'Application not found or access denied'}), 404
    
    db.execute('DELETE FROM job_application WHERE id = ?', (id,))
    db.commit()
    
    return jsonify({'message': 'Application deleted successfully'})
