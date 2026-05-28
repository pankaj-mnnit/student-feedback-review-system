from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


# ---------- Homepage Route ----------
@main_bp.route('/')
def index():
    """Render the landing page (index.html)."""
    return render_template('index.html')
