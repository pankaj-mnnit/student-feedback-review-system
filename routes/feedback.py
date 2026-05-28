from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from utils.sentiment import analyze_sentiment
from database import get_db_connection
from datetime import datetime
from urllib.parse import unquote

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/get-teachers/<path:subject_id>')
def get_teachers(subject_id):
    """API endpoint to fetch assigned teacher for a specific subject."""
    # URL-decode subject_id to handle spaces encoded as %20 (e.g. 'AL%20601' → 'AL 601')
    subject_id = unquote(subject_id)
    conn = get_db_connection()
    teacher = conn.execute("""
        SELECT t.user_id as id, t.name 
        FROM teachers t
        JOIN subject_teachers st ON t.user_id = st.teacher_id
        WHERE st.subject_code = ? AND LOWER(t.user_id) NOT LIKE 'adm%'
        ORDER BY t.user_id ASC
    """, (subject_id,)).fetchall()
    conn.close()
    return jsonify([dict(t) for t in teacher])

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
def submit_feedback():
    """
    GET: Render the feedback form with subjects from db.
    POST: Process form submission.
    """
    if request.method == 'POST':
        subject_id = request.form.get('subject_id', '').strip()
        teacher_id = request.form.get('teacher_id', '').strip()
        rating     = request.form.get('rating', '').strip()
        comments   = request.form.get('comments', '').strip()

        # Validation
        if not subject_id or not teacher_id or not rating or not comments:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
               'application/json' in request.accept_mimetypes:
                return jsonify({'success': False, 'message': 'All fields (subject, teacher, rating, and review comment) are required.'}), 400
            flash('All fields (subject, teacher, rating, and review comment) are required.', 'danger')
            return redirect(url_for('feedback.submit_feedback'))
        
        try:
            rating_int = int(rating)
        except ValueError:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
               'application/json' in request.accept_mimetypes:
                return jsonify({'success': False, 'message': 'Invalid rating.'}), 400
            flash('Invalid rating.', 'danger')
            return redirect(url_for('feedback.submit_feedback'))

        # Analyze sentiment using TextBlob - comment-based only, not rating-based
        sentiment_analysis, polarity_score = analyze_sentiment(comments)
        print(f"[SENTIMENT] comment='{comments[:50]}...' polarity={polarity_score} label={sentiment_analysis}")

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO feedback (subject, teacher, rating_star, feedback_comment, sentiment_analysis, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (subject_id, teacher_id, rating_int, comments, sentiment_analysis, current_date))
        conn.commit()
        conn.close()

        # Return JSON for AJAX submissions (JS handles the success UI)
        # For non-JS form submissions, flash and redirect
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
           'application/json' in request.accept_mimetypes:
            return jsonify({'success': True, 'message': 'Feedback submitted successfully. Thank you for sharing your review.'})
        
        flash('Feedback submitted successfully. Thank you for sharing your review.', 'success')
        return redirect(url_for('feedback.submit_feedback'))  # ← Stay on feedback page with success message

    # GET: Fetch only subjects for the initial dropdown
    conn = get_db_connection()
    subjects_raw = conn.execute("SELECT subject_code as id, subject_code || ' - ' || subject_name as name FROM subjects ORDER BY subject_code ASC").fetchall()
    subjects = [dict(s) for s in subjects_raw]
    conn.close()
    
    return render_template('feedback.html', subjects=subjects)

