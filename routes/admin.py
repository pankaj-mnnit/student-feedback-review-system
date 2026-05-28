from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from functools import wraps
from database import get_db_connection

import re

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def clean_username(val):
    if not val:
        return ""
    val = val.strip().upper()
    result = ""
    for char in val:
        if len(result) < 6:
            if len(result) < 3:
                if char.isalpha():
                    result += char
            else:
                if char.isdigit():
                    result += char
    return result

# ──────────────────────────────────────────────────────────────────────────────
#  AUTH DECORATORS
# ──────────────────────────────────────────────────────────────────────────────

def login_required_any(f):
    """Require any authenticated user (admin or teacher)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Require authenticated user with role == 'admin'."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('main.index'))
        if session.get('role') != 'admin':
            flash('Access denied. Redirected to teacher dashboard.', 'danger')
            return redirect(url_for('admin.teacher_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    """Require authenticated user with role == 'teacher' or a teacher promoted to admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        role = session.get('role')
        if not user_id:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('main.index'))
            
        is_teacher = False
        if role == 'teacher':
            is_teacher = True
        elif role == 'admin' and not user_id.upper().startswith('ADM'):
            is_teacher = True
                
        if not is_teacher:
            flash('Admins have access to the main dashboard.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ──────────────────────────────────────────────────────────────────────────────
#  CACHE CONTROL - Prevent back-button from showing protected pages
# ──────────────────────────────────────────────────────────────────────────────

@admin_bp.after_request
def add_no_cache_headers(response):
    """Add no-cache headers to all admin blueprint responses."""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# ──────────────────────────────────────────────────────────────────────────────
#  LOGIN
# ──────────────────────────────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Invalid request format."}), 400
            
        user_id = (data.get('user_id') or '').strip()
        password = (data.get('password') or '').strip()

        # Validation: empty fields
        if not user_id or not password:
            return jsonify({"success": False, "message": "User ID and Password are required."}), 400

        print(f"[AUTH] Login attempt: user_id={user_id}")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM teachers WHERE user_id = ? COLLATE NOCASE",
            (user_id,)
        ).fetchone()
        conn.close()

        if not user:
            print(f"[AUTH] Login failed: user_id={user_id} - user not found")
            return jsonify({"success": False, "message": "Invalid User ID or password."}), 401

        if user['password'] != password:
            print(f"[AUTH] Login failed: user_id={user_id} - incorrect password")
            return jsonify({"success": False, "message": "Incorrect Password"}), 401

        # Determine role from admin column
        role = 'admin' if user['admin'] == 'yes' else 'teacher'

        # Set session - browser-specific, no global state
        session.permanent = False
        session['user_id'] = user['user_id']
        session['user_name'] = user['name']
        session['role'] = role

        # Role-based redirect
        if role == 'admin':
            redirect_url = url_for('admin.dashboard')
        else:
            redirect_url = url_for('admin.teacher_dashboard')

        print(f"[AUTH] Login success: user_id={user_id}, role={role}, redirect={redirect_url}")
        return jsonify({"success": True, "redirect": redirect_url}), 200
            
    except Exception as e:
        print(f"[AUTH] Login error: {e}")
        return jsonify({"success": False, "message": "A system error occurred. Please try again."}), 500

# ──────────────────────────────────────────────────────────────────────────────
#  LOGOUT
# ──────────────────────────────────────────────────────────────────────────────

@admin_bp.route('/logout')
@login_required_any
def logout():
    print(f"[AUTH] Logout: user_id={session.get('user_id')}, role={session.get('role')}")
    session.clear()
    return redirect(url_for('main.index'))

# ──────────────────────────────────────────────────────────────────────────────
#  PROFILE & PASSWORD
# ──────────────────────────────────────────────────────────────────────────────

@admin_bp.route('/profile')
@login_required_any
def profile():
    user_id = session.get('user_id')
    role = session.get('role')
    
    conn = get_db_connection()
    user_data = conn.execute("SELECT * FROM teachers WHERE user_id = ?", (user_id,)).fetchone()
    
    stats = {}
    assigned_subjects = []
    
    if user_data:
        user_dict = dict(user_data)
        user_dict['role'] = 'admin' if user_data['admin'] == 'yes' or user_id.startswith('ADM') else 'teacher'
        user_data = user_dict
        
        if role == 'teacher' or user_dict['role'] == 'teacher':
            subs = conn.execute('''
                SELECT s.subject_name 
                FROM subject_teachers st 
                JOIN subjects s ON st.subject_code = s.subject_code 
                WHERE st.teacher_id = ?
                ORDER BY s.subject_code ASC
            ''', (user_id,)).fetchall()
            assigned_subjects = [sub['subject_name'] for sub in subs]
                
            stats_row = conn.execute('''
                SELECT 
                    COUNT(*) as total_feedbacks,
                    COALESCE(AVG(rating_star), 0) as avg_rating
                FROM feedback
                WHERE teacher = ?
            ''', (user_id,)).fetchone()
            
            stats['total_feedbacks'] = stats_row['total_feedbacks']
            stats['avg_rating'] = round(stats_row['avg_rating'], 1)
    
    conn.close()
    
    return render_template('admin/profile.html', user=user_data, subjects=assigned_subjects, stats=stats)

@admin_bp.route('/change-password', methods=['POST'])
@login_required_any
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    user_id = session.get('user_id')
    
    if not current_password or not new_password or not confirm_password:
        return jsonify({"success": False, "message": "All fields are required."}), 400
        
    if new_password != confirm_password:
        return jsonify({"success": False, "message": "New passwords do not match."}), 400
        
    if len(new_password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters."}), 400

    conn = get_db_connection()
    user = conn.execute("SELECT password FROM teachers WHERE user_id = ?", (user_id,)).fetchone()
    
    if not user or user['password'] != current_password:
        conn.close()
        return jsonify({"success": False, "message": "Incorrect current password."}), 401
        
    conn.execute("UPDATE teachers SET password = ? WHERE user_id = ?", (new_password, user_id))
    conn.commit()
    conn.close()
    
    flash('Password changed successfully!', 'success')
    return jsonify({"success": True, "redirect": url_for('admin.profile')}), 200

# ══════════════════════════════════════════════════════════════════════════════
#  TEACHER DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

@admin_bp.route('/teacher/dashboard')
@teacher_required
def teacher_dashboard():
    user_id = session.get('user_id')
    conn = get_db_connection()

    # Teacher info
    teacher = conn.execute("SELECT * FROM teachers WHERE user_id = ?", (user_id,)).fetchone()

    # Assigned subjects
    subject_raw = conn.execute("""
        SELECT s.subject_code, s.subject_name
        FROM subjects s
        JOIN subject_teachers st ON s.subject_code = st.subject_code
        WHERE st.teacher_id = ?
        ORDER BY s.subject_code ASC
    """, (user_id,)).fetchall()
    subject_name = ", ".join([f"{row['subject_code']} - {row['subject_name']}" for row in subject_raw]) if subject_raw else ""
    subject = {'subject_name': subject_name}

    # Feedback for this teacher
    feedbacks_raw = conn.execute("""
        SELECT f.*, s.subject_name
        FROM feedback f
        LEFT JOIN subjects s ON f.subject = s.subject_code
        WHERE f.teacher = ?
        ORDER BY f.id DESC
    """, (user_id,)).fetchall()
    feedbacks = [dict(f) for f in feedbacks_raw]
    for f in feedbacks:
        if f.get('date'):
            f['date'] = str(f['date']).split(' ')[0]

    total_feedbacks = len(feedbacks)

    avg_rating_val = conn.execute(
        "SELECT AVG(rating_star) FROM feedback WHERE teacher = ?", (user_id,)
    ).fetchone()[0]
    avg_rating = round(avg_rating_val, 1) if avg_rating_val else 0.0

    # Sentiment counts
    sentiments = conn.execute("""
        SELECT sentiment_analysis, COUNT(*) as count
        FROM feedback WHERE teacher = ?
        GROUP BY sentiment_analysis
    """, (user_id,)).fetchall()

    pos = neu = neg = 0
    for s in sentiments:
        if s['sentiment_analysis'] == 'positive': pos = s['count']
        elif s['sentiment_analysis'] == 'neutral': neu = s['count']
        elif s['sentiment_analysis'] == 'negative': neg = s['count']

    # Rating Distribution (1 to 5) for this teacher
    chart_rating_counts = [0, 0, 0, 0, 0]
    ratings = conn.execute("""
        SELECT rating_star, COUNT(*) as count 
        FROM feedback 
        WHERE teacher = ? 
        GROUP BY rating_star
    """, (user_id,)).fetchall()
    for r in ratings:
        if 1 <= r['rating_star'] <= 5:
            chart_rating_counts[r['rating_star']-1] = r['count']

    conn.close()

    # Build teacher data object for template
    subjects_list = []
    if subject and subject['subject_name']:
        subjects_list = [s.strip() for s in subject['subject_name'].split(',') if s.strip()]

    teacher_data = {
        'name': teacher['name'],
        'user_id': teacher['user_id'],
        'subject': {
            'name': subject['subject_name'] if subject and subject['subject_name'] else 'Not Assigned'
        },
        'subjects': subjects_list
    }

    recent_feedbacks = feedbacks[:10]

    return render_template('teacher/dashboard.html',
                           teacher=teacher_data,
                           feedbacks=recent_feedbacks,
                           total_feedbacks=total_feedbacks,
                           avg_rating=avg_rating,
                           pos=pos, neu=neu, neg=neg,
                           chart_rating_counts=chart_rating_counts,
                           active_page='teacher_dashboard',
                           hide_navbar=True,
                           hide_footer=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TEACHER FEEDBACKS
# ══════════════════════════════════════════════════════════════════════════════

@admin_bp.route('/teacher/feedbacks')
@teacher_required
def teacher_feedbacks():
    user_id = session.get('user_id')
    conn = get_db_connection()
    
    # Extract query parameters
    subject_code = request.args.get('subject_id', '').strip()
    rating = request.args.get('rating', '').strip()

    # Build query dynamically, bound strictly to this teacher
    query = """
        SELECT f.*, s.subject_name
        FROM feedback f
        LEFT JOIN subjects s ON f.subject = s.subject_code
        WHERE f.teacher = ?
    """
    params = [user_id]

    if subject_code:
        query += " AND f.subject = ?"
        params.append(subject_code)
    if rating:
        query += " AND f.rating_star = ?"
        params.append(int(rating))

    query += " ORDER BY f.id DESC"

    feedbacks_raw = conn.execute(query, params).fetchall()
    feedbacks = [dict(f) for f in feedbacks_raw]
    for f in feedbacks:
        if f.get('date'):
            f['date'] = str(f['date']).split(' ')[0]
    
    # Retrieve only the subjects taught by this teacher for the dropdown filter
    subjects = conn.execute("""
        SELECT DISTINCT s.subject_code as id, s.subject_name as name 
        FROM subjects s
        JOIN subject_teachers st ON s.subject_code = st.subject_code
        WHERE st.teacher_id = ?
        ORDER BY s.subject_code ASC
    """, (user_id,)).fetchall()
    
    conn.close()
    
    return render_template('teacher/feedbacks.html',
                           active_page='teacher_feedbacks',
                           feedbacks=feedbacks,
                           all_subjects=[dict(s) for s in subjects],
                           hide_navbar=True,
                           hide_footer=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN DASHBOARD (Overview)
# ══════════════════════════════════════════════════════════════════════════════

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    conn = get_db_connection()
    
    total_feedbacks = conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
    total_subjects_count = conn.execute("SELECT COUNT(*) FROM subjects").fetchone()[0]
    total_teachers_count = conn.execute("SELECT COUNT(*) FROM teachers WHERE LOWER(user_id) NOT LIKE 'adm%'").fetchone()[0]
    
    avg_rating_row = conn.execute("SELECT AVG(rating_star) FROM feedback").fetchone()[0]
    avg_rating = round(avg_rating_row, 1) if avg_rating_row else 0.0
    
    # Rating Distribution (1 to 5)
    chart_rating_counts = [0, 0, 0, 0, 0]
    ratings = conn.execute("SELECT rating_star, COUNT(*) as count FROM feedback GROUP BY rating_star").fetchall()
    for r in ratings:
        if 1 <= r['rating_star'] <= 5:
            chart_rating_counts[r['rating_star']-1] = r['count']
    
    # Sentiment Overview
    sentiments = conn.execute("SELECT sentiment_analysis, COUNT(*) as count FROM feedback GROUP BY sentiment_analysis").fetchall()
    total_positive = 0
    total_neutral = 0
    total_negative = 0
    for s in sentiments:
        if s['sentiment_analysis'] == 'positive': total_positive = s['count']
        elif s['sentiment_analysis'] == 'neutral': total_neutral = s['count']
        elif s['sentiment_analysis'] == 'negative': total_negative = s['count']
    
    # Recent Feedback
    feedbacks_raw = conn.execute("""
        SELECT f.*, s.subject_name, t.name as teacher_name 
        FROM feedback f
        LEFT JOIN subjects s ON f.subject = s.subject_code
        LEFT JOIN teachers t ON f.teacher = t.user_id
        ORDER BY f.id DESC LIMIT 10
    """).fetchall()
    
    feedbacks = [dict(f) for f in feedbacks_raw]
    for f in feedbacks:
        if not f['subject_name']: f['subject_name'] = f['subject']
        if not f['teacher_name']: f['teacher_name'] = f['teacher']
        if f.get('date'):
            f['date'] = str(f['date']).split(' ')[0]

    # Teacher stats for charts
    teacher_stats = conn.execute("""
        SELECT t.name, AVG(f.rating_star) as avg_rating
        FROM teachers t
        JOIN feedback f ON t.user_id = f.teacher
        WHERE LOWER(t.user_id) NOT LIKE 'adm%'
        GROUP BY t.user_id
        ORDER BY avg_rating DESC
    """).fetchall()
    teacher_names = [row['name'] for row in teacher_stats]
    teacher_ratings = [round(row['avg_rating'], 1) if row['avg_rating'] else 0.0 for row in teacher_stats]

    conn.close()

    return render_template('admin/dashboard.html',
                           active_page='dashboard',
                           feedbacks=feedbacks,
                           total_feedbacks=total_feedbacks,
                           avg_rating=avg_rating,
                           total_subjects_count=total_subjects_count,
                           total_teachers_count=total_teachers_count,
                           total_positive=total_positive,
                           total_neutral=total_neutral,
                           total_negative=total_negative,
                           chart_rating_counts=chart_rating_counts,
                           teacher_names=teacher_names,
                           teacher_ratings=teacher_ratings,
                           hide_navbar=True,
                           hide_footer=True)

# ──────────────────────────────────────────────────────────────────────────────
#  ADMIN FEEDBACKS
# ──────────────────────────────────────────────────────────────────────────────

@admin_bp.route('/feedbacks')
@admin_required
def feedbacks():
    conn = get_db_connection()
    # Extract query parameters
    teacher_query = request.args.get('teacher', '').strip()
    subject_id = request.args.get('subject_id', '').strip()
    rating = request.args.get('rating', '').strip()

    # Build query dynamically
    query = """
        SELECT f.*, s.subject_name, t.name as teacher_name 
        FROM feedback f
        LEFT JOIN subjects s ON f.subject = s.subject_code
        LEFT JOIN teachers t ON f.teacher = t.user_id
        WHERE 1=1
    """
    params = []

    if teacher_query:
        query += " AND t.name LIKE ?"
        params.append(f"%{teacher_query}%")
    if subject_id:
        query += " AND f.subject = ?"
        params.append(subject_id)
    if rating:
        query += " AND f.rating_star = ?"
        params.append(int(rating))

    query += " ORDER BY f.id DESC"

    feedbacks_raw = conn.execute(query, params).fetchall()
    feedbacks = [dict(f) for f in feedbacks_raw]
    for f in feedbacks:
        if not f['subject_name']: f['subject_name'] = f['subject']
        if not f['teacher_name']: f['teacher_name'] = f['teacher']
        if f.get('date'):
            f['date'] = str(f['date']).split(' ')[0]
    
    subjects = conn.execute("SELECT subject_code as id, subject_name as name FROM subjects ORDER BY subject_code ASC").fetchall()
    conn.close()
    
    return render_template('admin/feedbacks.html',
                           active_page='feedbacks',
                           feedbacks=feedbacks,
                           all_subjects=[dict(s) for s in subjects],
                           hide_navbar=True,
                           hide_footer=True)


# ──────────────────────────────────────────────────────────────────────────────
#  TEACHERS ADMIN PAGE
# ──────────────────────────────────────────────────────────────────────────────

@admin_bp.route('/teachers')
@admin_required
def teachers():
    conn = get_db_connection()
    teachers_raw = conn.execute("""
        SELECT t.user_id, t.name, t.admin,
               (SELECT GROUP_CONCAT(s.subject_code || ' - ' || s.subject_name, ', ') 
                FROM subject_teachers st 
                JOIN subjects s ON st.subject_code = s.subject_code 
                WHERE st.teacher_id = t.user_id) as assigned_subjects,
               (SELECT COUNT(id) FROM feedback WHERE teacher = t.user_id) as total_feedback, 
               (SELECT AVG(rating_star) FROM feedback WHERE teacher = t.user_id) as avg_rating
        FROM teachers t
        WHERE LOWER(t.user_id) NOT LIKE 'adm%'
        GROUP BY t.user_id
        ORDER BY t.user_id ASC
    """).fetchall()
    all_teachers = []
    for t in teachers_raw:
        td = dict(t)
        td['avg_rating'] = round(t['avg_rating'], 1) if t['avg_rating'] else 0.0
        if td['assigned_subjects']:
            subs_list = [s.strip() for s in td['assigned_subjects'].split(',')]
            subs_list.sort()
            td['assigned_subjects'] = ', '.join(subs_list)
        all_teachers.append(td)
    conn.close()
    return render_template('admin/teachers.html', active_page='teachers', teachers=all_teachers, hide_navbar=True, hide_footer=True)

# ──────────────────────────────────────────────────────────────────────────────
#  SUBJECTS ADMIN PAGE
# ──────────────────────────────────────────────────────────────────────────────

@admin_bp.route('/subjects')
@admin_required
def subjects():
    conn = get_db_connection()
    subjects_raw = conn.execute("""
        SELECT s.subject_code, s.subject_name,
               GROUP_CONCAT(t.name, ', ') as teacher_name,
               GROUP_CONCAT(t.user_id, ',') as teacher_ids,
               (SELECT COUNT(id) FROM feedback WHERE subject = s.subject_code) as total_feedback,
               (SELECT AVG(rating_star) FROM feedback WHERE subject = s.subject_code) as avg_rating
        FROM subjects s
        LEFT JOIN subject_teachers st ON s.subject_code = st.subject_code
        LEFT JOIN teachers t ON st.teacher_id = t.user_id
        GROUP BY s.subject_code
        ORDER BY s.subject_code ASC
    """).fetchall()
    
    all_subjects = []
    for s in subjects_raw:
        s_dict = dict(s)
        s_dict['avg_rating'] = round(s['avg_rating'], 1) if s['avg_rating'] else 0.0
        if s_dict['teacher_ids'] and s_dict['teacher_name']:
            t_ids = s_dict['teacher_ids'].split(',')
            t_names = s_dict['teacher_name'].split(', ')
            paired = list(zip(t_ids, t_names))
            paired.sort(key=lambda x: x[0])
            s_dict['teacher_ids_list'] = [p[0] for p in paired]
            s_dict['teacher_name'] = ', '.join([p[1] for p in paired])
        else:
            s_dict['teacher_ids_list'] = []
        all_subjects.append(s_dict)
    
    teachers_raw = conn.execute("SELECT user_id, name FROM teachers WHERE LOWER(user_id) NOT LIKE 'adm%' ORDER BY user_id ASC").fetchall()
    all_teachers = [dict(t) for t in teachers_raw]
    
    conn.close()
    return render_template('admin/subjects.html', active_page='subjects', subjects=all_subjects, teachers=all_teachers, hide_navbar=True, hide_footer=True)


@admin_bp.route('/subjects/add', methods=['POST'])
@admin_required
def add_subject():
    code = request.form.get('subject_code', '').strip().upper().replace('-', ' ')
    code = re.sub(r'[^A-Z0-9 ]', '', code)
    code = re.sub(r'^([A-Z]{2})([0-9]{3,4})$', r'\1 \2', code)
    code = re.sub(r'\s+', ' ', code)
    name = request.form.get('subject_name', '').strip()
    
    if not code or not name:
        flash("Subject Code and Name are required.", "danger")
    elif not re.match(r'^[A-Z]{2} [0-9]{3,4}$', code):
        flash("Invalid Subject Code", "danger")
    else:
        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO subjects (subject_code, subject_name) VALUES (?, ?)", (code, name))
            conn.commit()
            conn.close()
            flash(f"Subject '{code} – {name}' added successfully.", "success")
        except Exception as e:
            flash("Subject code must be unique.", "danger")
    return redirect(url_for('admin.subjects'))

@admin_bp.route('/subjects/update_teacher/<string:subject_id>', methods=['POST'])
@admin_required
def update_subject_teacher(subject_id):
    # Expect multiple teacher IDs
    teacher_ids = request.form.getlist('teacher_ids')
        
    try:
        conn = get_db_connection()
        # Delete existing mappings
        conn.execute("DELETE FROM subject_teachers WHERE subject_code = ?", (subject_id,))
        # Insert new mappings
        for tid in teacher_ids:
            if tid.strip():
                conn.execute("INSERT INTO subject_teachers (subject_code, teacher_id) VALUES (?, ?)", (subject_id, tid.strip()))
        

        
        conn.commit()
        conn.close()
        flash(f"Teachers updated successfully for subject '{subject_id}'.", "success")
    except Exception as e:
        flash("Error updating teacher assignment.", "danger")
        
    return redirect(url_for('admin.subjects'))

@admin_bp.route('/subjects/delete/<string:subject_id>', methods=['POST'])
@admin_required
def delete_subject(subject_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM subjects WHERE subject_code = ?", (subject_id,))
    conn.execute("DELETE FROM feedback WHERE subject = ?", (subject_id,))
    conn.commit()
    conn.close()
    flash("Subject deleted successfully.", "success")
    return redirect(url_for('admin.subjects'))

@admin_bp.route('/teachers/add', methods=['POST'])
@admin_required
def add_teacher():
    teacher_id = clean_username(request.form.get('teacher_employee_id', ''))
    name = request.form.get('teacher_name', '').strip()
    if not name:
        flash("Both Teacher ID and Name are required.", "danger")
    elif not teacher_id or len(teacher_id) != 6:
        flash("Invalid Teacher ID", "danger")
    else:
        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO teachers (user_id, name, password, admin) VALUES (?, ?, ?, 'no')", (teacher_id, name, '123456'))
            conn.commit()
            conn.close()
            flash(f"Teacher '{name}' registered successfully. Default password is '123456'.", "success")
        except Exception as e:
            flash("Teacher ID must be unique.", "danger")
    return redirect(url_for('admin.teachers'))

@admin_bp.route('/teachers/delete/<string:teacher_id>', methods=['POST'])
@admin_required
def delete_teacher(teacher_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM teachers WHERE user_id = ?", (teacher_id,))
    conn.execute("DELETE FROM feedback WHERE teacher = ?", (teacher_id,))
    conn.execute("DELETE FROM subject_teachers WHERE teacher_id = ?", (teacher_id,))
    conn.commit()
    conn.close()
    flash("Teacher deleted successfully.", "success")
    return redirect(url_for('admin.teachers'))

@admin_bp.route('/teachers/toggle-admin/<string:teacher_id>', methods=['POST'])
@admin_required
def toggle_admin(teacher_id):
    if session.get('user_id') != 'ADM001':
        flash("Unauthorized. Only the main Administrator can modify admin privileges.", "danger")
        return redirect(url_for('admin.teachers'))

    # Don't allow toggling the logged-in admin's own status (optional but good security)
    if session.get('user_id') == teacher_id:
        flash("You cannot remove your own admin privileges.", "danger")
        return redirect(url_for('admin.teachers'))

    conn = get_db_connection()
    row = conn.execute("SELECT admin, name FROM teachers WHERE user_id = ?", (teacher_id,)).fetchone()
    if row:
        new_status = 'yes' if row['admin'] == 'no' else 'no'
        conn.execute("UPDATE teachers SET admin = ? WHERE user_id = ?", (new_status, teacher_id))
        conn.commit()
        if new_status == 'yes':
            flash(f"'{row['name']}' has been promoted to Admin successfully.", "success")
        else:
            flash(f"Admin privileges removed from '{row['name']}'.", "success")
    conn.close()
    return redirect(url_for('admin.teachers'))

# ──────────────────────────────────────────────────────────────────────────────
#  ADMIN MANAGEMENT
# ──────────────────────────────────────────────────────────────────────────────

@admin_bp.route('/admins')
@admin_required
def admins():
    if session.get('user_id') != 'ADM001':
        flash("Unauthorized. Only the main Administrator can manage admin accounts.", "danger")
        return redirect(url_for('admin.dashboard'))

    conn = get_db_connection()
    admins = conn.execute("SELECT * FROM teachers WHERE admin = 'yes' ORDER BY user_id ASC").fetchall()
    teachers = conn.execute("SELECT * FROM teachers WHERE admin = 'no' ORDER BY user_id ASC").fetchall()
    conn.close()
    return render_template('admin/admins.html',
                           active_page='admins',
                           admins=[dict(a) for a in admins],
                           teachers=[dict(t) for t in teachers],
                           hide_navbar=True,
                           hide_footer=True)

@admin_bp.route('/admins/add', methods=['POST'])
@admin_required
def add_admin():
    if session.get('user_id') != 'ADM001':
        flash("Unauthorized. Only the main Administrator can create admin accounts.", "danger")
        return redirect(url_for('admin.dashboard'))

    username = clean_username(request.form.get('username', ''))
    name = request.form.get('name', '').strip()
    if not name:
        name = username

    if username and len(username) == 6:
        conn = get_db_connection()
        teacher = conn.execute("SELECT * FROM teachers WHERE user_id = ?", (username,)).fetchone()
        if teacher:
            conn.close()
            flash("User ID already exists. Admin ID must be unique.", "danger")
            return redirect(url_for('admin.admins'))
        else:
            conn.execute("INSERT INTO teachers (user_id, name, password, admin) VALUES (?, ?, ?, 'yes')", (username, name, '123456'))
            conn.commit()
            conn.close()
            flash(f"Admin '{name}' created successfully. Default password is '123456'.", "success")
    else:
        flash("Invalid Admin ID. Must be 3 letters + 3 numbers (e.g. ADM002).", "danger")
    return redirect(url_for('admin.admins'))

@admin_bp.route('/admins/promote', methods=['POST'])
@admin_required
def promote_teacher():
    if session.get('user_id') != 'ADM001':
        flash("Unauthorized. Only the main Administrator can manage admin accounts.", "danger")
        return redirect(url_for('admin.dashboard'))

    teacher_id = request.form.get('teacher_id')
    if teacher_id:
        conn = get_db_connection()
        teacher = conn.execute("SELECT name FROM teachers WHERE user_id = ?", (teacher_id,)).fetchone()
        if teacher:
            conn.execute("UPDATE teachers SET admin = 'yes' WHERE user_id = ?", (teacher_id,))
            conn.commit()
            flash(f"Teacher '{teacher['name']}' promoted to Admin successfully.", "success")
        else:
            flash("Teacher not found.", "danger")
        conn.close()
    else:
        flash("Please select a teacher to promote.", "danger")
    return redirect(url_for('admin.admins'))

@admin_bp.route('/admins/delete/<string:admin_id>', methods=['POST'])
@admin_required
def delete_admin(admin_id):
    if session.get('user_id') != 'ADM001':
        flash("Unauthorized. Only the main Administrator can delete admin accounts.", "danger")
        return redirect(url_for('admin.dashboard'))

    if admin_id == 'ADM001':
        flash("Cannot delete default admin.", "danger")
        return redirect(url_for('admin.admins'))
        
    conn = get_db_connection()
    if admin_id.upper().startswith('ADM'):
        # Delete custom admin completely from the database
        conn.execute("DELETE FROM teachers WHERE user_id = ?", (admin_id,))
        conn.execute("DELETE FROM feedback WHERE teacher = ?", (admin_id,))
        conn.execute("DELETE FROM subject_teachers WHERE teacher_id = ?", (admin_id,))
        conn.commit()
        flash("Admin account deleted successfully from the database.", "success")
    else:
        # Demote promoted teacher back to regular teacher
        conn.execute("UPDATE teachers SET admin = 'no' WHERE user_id = ?", (admin_id,))
        conn.commit()
        flash("Admin privileges removed successfully.", "success")
    conn.close()
    return redirect(url_for('admin.admins'))


# ──────────────────────────────────────────────────────────────────────────────
#  REPORTS & CHARTS PAGE
# ──────────────────────────────────────────────────────────────────────────────

@admin_bp.route('/reports')
@admin_required
def reports():
    """Reports page - currently redirects to dashboard (charts are integrated there)."""
    return redirect(url_for('admin.dashboard'))

# ──────────────────────────────────────────────────────────────────────────────
#  DELETE FEEDBACK
# ──────────────────────────────────────────────────────────────────────────────

@admin_bp.route('/delete/<int:feedback_id>', methods=['POST'])
@admin_required
def delete_feedback(feedback_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM feedback WHERE id = ?", (feedback_id,))
    conn.commit()
    conn.close()
    flash('Feedback deleted successfully.', 'success')
    return redirect(url_for('admin.feedbacks'))
