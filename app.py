
import json
import uuid
import sqlite3
from datetime import datetime
from functools import wraps
import io
import csv
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, request, jsonify, render_template, session, Response, redirect, url_for, flash, g
from scoring import calculate_all_scores # Updated import
import config

# Configuration
# Database configuration
DATABASE = config.DATABASE_PATH

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# --- Database Connection Handling (Robust Pattern) ---
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, check_same_thread=False)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- Database Initialization with Auto-Migration ---
def create_tables():
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        # Simplified schema: store the entire report as a single JSON object
        cursor.execute("CREATE TABLE IF NOT EXISTS assessments (id INTEGER PRIMARY KEY, session_id TEXT UNIQUE, user_id INTEGER, timestamp DATETIME, full_report TEXT, ip_address TEXT, user_agent TEXT, completed BOOLEAN, FOREIGN KEY(user_id) REFERENCES users(id));")
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, email TEXT, phone TEXT, role TEXT, approved BOOLEAN, created_at DATETIME);")
        cursor.execute("CREATE TABLE IF NOT EXISTS consultant_patient_map (id INTEGER PRIMARY KEY, consultant_id INTEGER, patient_id INTEGER, FOREIGN KEY(consultant_id) REFERENCES users(id), FOREIGN KEY(patient_id) REFERENCES users(id));")
        
        # --- Self-Healing Migration Logic ---
        try:
            cursor.execute("SELECT full_report FROM assessments LIMIT 1")
        except sqlite3.OperationalError:
            print("INFO: Old database schema detected. Recreating assessments table...")
            cursor.execute("DROP TABLE IF EXISTS assessments")
            cursor.execute("CREATE TABLE assessments (id INTEGER PRIMARY KEY, session_id TEXT UNIQUE, user_id INTEGER, timestamp DATETIME, full_report TEXT, ip_address TEXT, user_agent TEXT, completed BOOLEAN, FOREIGN KEY(user_id) REFERENCES users(id));")
            print("INFO: Table 'assessments' has been recreated with the new schema.")

        cursor.execute("SELECT * FROM users WHERE username = ?", (config.ADMIN_USERNAME,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (username, password_hash, role, approved) VALUES (?, ?, ?, ?)", (config.ADMIN_USERNAME, generate_password_hash(config.ADMIN_PASSWORD), 'admin', True))
        
        conn.commit()

# --- Authentication Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to view this page.", "warning")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def requires_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash("You must be logged in to view this page.", "warning")
                return redirect(url_for('login', next=request.url))
            if session.get('role') != required_role:
                flash(f"This page requires the '{required_role}' role.", "danger")
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return wrapper
    return decorator

# --- Main Routes ---
@app.route('/')
def index():
    patient_id = request.args.get('patient_id')
    if patient_id:
        session['patient_id_for_assessment'] = patient_id
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

# --- Dashboards ---
@app.route('/dashboard')
@requires_role('client')
def dashboard():
    conn = get_db()
    assessments = conn.execute("SELECT session_id, timestamp FROM assessments WHERE user_id = ? AND completed = TRUE ORDER BY timestamp DESC", (session['user_id'],)).fetchall()
    return render_template('dashboard.html', assessments=assessments)

@app.route('/consultant/dashboard')
@requires_role('consultant')
def consultant_dashboard():
    return render_template('consultant_dashboard.html')

# --- Authentication Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username, password, email, phone, role = request.form.get('username'), request.form.get('password'), request.form.get('email'), request.form.get('phone'), request.form.get('role')
        conn = get_db()
        if conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        
        is_approved = role == 'client'
        
        conn.execute("INSERT INTO users (username, password_hash, email, phone, role, approved) VALUES (?, ?, ?, ?, ?, ?)",
            (username, generate_password_hash(password), email, phone, role, is_approved))
        conn.commit()
        
        if role == 'client':
            flash('Registration successful! You can now log in.', 'success')
        else:
            flash('Registration successful! Your consultant account requires admin approval.', 'info')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        user = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and user['password_hash'] and check_password_hash(user['password_hash'], password):
            if not user['approved']:
                flash('Your account has not been approved by an administrator yet.', 'warning')
                return redirect(url_for('login'))
            session['user_id'], session['username'], session['role'] = user['id'], user['username'], user['role']
            flash(f'Welcome back, {user["username"]}!', 'success')
            next_page = request.args.get('next')
            if session['role'] == 'admin': return redirect(next_page or url_for('admin'))
            if session['role'] == 'consultant': return redirect(next_page or url_for('consultant_dashboard'))
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

# --- API and Result Routes ---
@app.route('/api/submit', methods=['POST'])
def submit():
    user_id = session.get('patient_id_for_assessment') or session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No user is associated with this assessment. Please use a valid link or log in.'}), 403
    session.pop('patient_id_for_assessment', None)
    data = request.get_json()
    
    # --- New Centralized Scoring ---
    full_report = calculate_all_scores(data['responses'])

    conn = get_db()
    completion_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute("INSERT INTO assessments (session_id, user_id, timestamp, full_report, ip_address, user_agent, completed) VALUES (?, ?, ?, ?, ?, ?, TRUE)",
        (session.get('session_id'), user_id, completion_timestamp, json.dumps(full_report), request.remote_addr, request.user_agent.string))
    conn.commit()
    return jsonify({'message': 'Assessment submitted successfully.', 'session_id': session.get('session_id')})

@app.route('/results/<session_id>')
@login_required
def results(session_id):
    if session['role'] == 'client':
        flash("Your assessment has been submitted successfully. Your consultant or an administrator will contact you with the results.", "success")
        return redirect(url_for('dashboard'))

    conn = get_db()
    assessment = conn.execute("SELECT * FROM assessments WHERE session_id = ?", (session_id,)).fetchone()
    if not assessment: return redirect(url_for('index'))

    user_id, user_role, assessment_user_id = session['user_id'], session['role'], assessment['user_id']
    
    if user_role == 'consultant':
        is_their_patient = conn.execute("SELECT 1 FROM consultant_patient_map WHERE consultant_id = ? AND patient_id = ?", (user_id, assessment_user_id)).fetchone()
        if not is_their_patient:
            flash("You do not have permission to view this client's report.", "danger")
            return redirect(url_for('consultant_dashboard'))

    return render_template('results.html')

@app.route('/api/results/<session_id>')
@login_required
def api_results(session_id):
    conn = get_db()
    assessment = conn.execute("SELECT * FROM assessments WHERE session_id = ?", (session_id,)).fetchone()
    if not assessment:
        return jsonify({'error': 'Assessment not found'}), 404

    user_id, user_role, assessment_user_id = session['user_id'], session['role'], assessment['user_id']
    if user_role == 'client':
        return jsonify({'error': 'Permission denied'}), 403
    if user_role == 'consultant':
        is_their_patient = conn.execute("SELECT 1 FROM consultant_patient_map WHERE consultant_id = ? AND patient_id = ?", (user_id, assessment_user_id)).fetchone()
        if not is_their_patient:
            return jsonify({'error': 'Permission denied'}), 403

    return jsonify(json.loads(assessment['full_report']))

# --- Consultant API Routes ---
@app.route('/api/consultant/patients')
@requires_role('consultant')
def get_consultant_patients():
    conn = get_db()
    patients = conn.execute("SELECT u.id, u.username, u.email, u.phone, (SELECT a.session_id FROM assessments a WHERE a.user_id = u.id AND a.completed = TRUE ORDER BY a.timestamp DESC LIMIT 1) as latest_session_id FROM users u JOIN consultant_patient_map m ON u.id = m.patient_id WHERE m.consultant_id = ?", (session['user_id'],)).fetchall()
    return jsonify([dict(row) for row in patients])

@app.route('/api/consultant/add_patient', methods=['POST'])
@requires_role('consultant')
def add_consultant_patient():
    data = request.get_json()
    username, email, phone = data.get('username'), data.get('email'), data.get('phone')
    conn = get_db()
    if conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
        return jsonify({'error': 'A user with this username already exists.'}), 400
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, phone, role, approved) VALUES (?, ?, ?, 'client', TRUE)", (username, email, phone))
    patient_id = cursor.lastrowid
    cursor.execute("INSERT INTO consultant_patient_map (consultant_id, patient_id) VALUES (?, ?)", (session['user_id'], patient_id))
    conn.commit()
    return jsonify({'message': 'Client created successfully.', 'patient_id': patient_id})

# --- Admin Routes ---
@app.route('/admin')
@requires_role('admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/user/<int:user_id>')
@requires_role('admin')
def view_user_assessments(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    assessments = conn.execute("SELECT * FROM assessments WHERE user_id = ? AND completed = TRUE ORDER BY timestamp DESC", (user_id,)).fetchall()
    if not user: return redirect(url_for('admin'))
    return render_template('user_assessments.html', user=user, assessments=assessments)

@app.route('/api/admin/all_users')
@requires_role('admin')
def get_all_users():
    users = get_db().execute("""
        SELECT u.id, u.username, u.role, u.approved, u.email, u.phone, 
               a.session_id as latest_session_id,
               a.timestamp as latest_assessment_date
        FROM users u 
        LEFT JOIN assessments a ON a.user_id = u.id AND a.completed = TRUE 
        WHERE u.role != 'admin' 
        GROUP BY u.id 
        HAVING a.timestamp = (SELECT MAX(timestamp) FROM assessments WHERE user_id = u.id AND completed = TRUE) OR a.timestamp IS NULL
        ORDER BY u.username
    """).fetchall()
    
    # Format the data for better display
    formatted_users = []
    for row in users:
        user_dict = dict(row)
        if user_dict['latest_assessment_date']:
            # Format the date to be more readable
            user_dict['latest_assessment_date'] = user_dict['latest_assessment_date'].split(' ')[0]  # Just the date part
        else:
            user_dict['latest_assessment_date'] = 'N/A'
        formatted_users.append(user_dict)
    
    return jsonify(formatted_users)

@app.route('/api/admin/users')
@requires_role('admin')
def get_unapproved_users():
    users = get_db().execute("SELECT id, username, role, created_at FROM users WHERE approved = FALSE AND role = 'consultant'").fetchall()
    return jsonify([dict(row) for row in users])

@app.route('/api/admin/approve/<int:user_id>', methods=['POST'])
@requires_role('admin')
def approve_user(user_id):
    conn = get_db()
    conn.execute("UPDATE users SET approved = TRUE WHERE id = ?", (user_id,))
    conn.commit()
    return jsonify({'message': f'User {user_id} approved.'})

@app.route('/api/print-pdf/<session_id>')
@login_required
def print_pdf(session_id):
    """Generate PDF with the results chart"""
    try:
        # Get assessment data
        conn = get_db()
        assessment = conn.execute(
            "SELECT * FROM assessments WHERE session_id = ?", (session_id,)
        ).fetchone()
        
        if not assessment:
            return jsonify({'error': 'Assessment not found'}), 404
        
        # Calculate scores
        scores = calculate_all_scores(json.loads(assessment['responses']))
        
        # Create matplotlib chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Prepare data for chart
        categories = []
        values = []
        
        for category, data in scores['detailed_breakdown'].items():
            if category != 'has_dc_adjustment':
                categories.append(category.replace('_', ' ').title())
                values.append(data['score'])
        
        # Create bar chart
        bars = ax.bar(categories, values, color=['#3498db', '#e74c3c', '#f39c12', '#2ecc71', '#9b59b6'])
        ax.set_title('Assessment Results Breakdown', fontsize=16, fontweight='bold')
        ax.set_ylabel('Scores', fontsize=12)
        ax.set_xlabel('Categories', fontsize=12)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{value}', ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save chart to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Create PDF
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        width, height = letter
        
        # Add title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, "Assessment Results Report")
        
        # Add assessment info
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Session ID: {session_id}")
        c.drawString(50, height - 100, f"Date: {assessment['created_at']}")
        c.drawString(50, height - 120, f"Total Score: {scores['total_score']}")
        c.drawString(50, height - 140, f"Final BR Score: {scores['final_br_score']}")
        
        # Add chart image
        img_reader = ImageReader(img_buffer)
        c.drawImage(img_reader, 50, height - 500, width=500, height=300)
        
        c.save()
        pdf_buffer.seek(0)
        
        return Response(
            pdf_buffer.getvalue(),
            mimetype='application/pdf',
            headers={'Content-Disposition': f'attachment; filename=assessment_results_{session_id}.pdf'}
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/print-word/<session_id>')
@login_required
def print_word(session_id):
    """Generate Word document with verbal interpretation of results"""
    try:
        # Get assessment data
        conn = get_db()
        assessment = conn.execute(
            "SELECT * FROM assessments WHERE session_id = ?", (session_id,)
        ).fetchone()
        
        if not assessment:
            return jsonify({'error': 'Assessment not found'}), 404
        
        # Calculate scores
        scores = calculate_all_scores(json.loads(assessment['responses']))
        
        # Create Word document
        doc = Document()
        
        # Add title
        title = doc.add_heading('Assessment Results Report', 0)
        title.alignment = 1  # Center alignment
        
        # Add assessment information
        doc.add_heading('Assessment Information', level=1)
        info_para = doc.add_paragraph()
        info_para.add_run('Session ID: ').bold = True
        info_para.add_run(f'{session_id}\n')
        info_para.add_run('Date: ').bold = True
        info_para.add_run(f'{assessment["created_at"]}\n')
        info_para.add_run('Total Score: ').bold = True
        info_para.add_run(f'{scores["total_score"]}\n')
        info_para.add_run('Final BR Score: ').bold = True
        info_para.add_run(f'{scores["final_br_score"]}')
        
        # Add detailed breakdown
        doc.add_heading('Detailed Score Breakdown', level=1)
        
        for category, data in scores['detailed_breakdown'].items():
            if category != 'has_dc_adjustment':
                category_name = category.replace('_', ' ').title()
                doc.add_heading(f'{category_name}', level=2)
                
                para = doc.add_paragraph()
                para.add_run('Score: ').bold = True
                para.add_run(f'{data["score"]}\n')
                para.add_run('Raw Score: ').bold = True
                para.add_run(f'{data["raw_score"]}\n')
                para.add_run('Adjustment: ').bold = True
                para.add_run(f'{data["adjustment"]}')
        
        # Add interpretation section
        doc.add_heading('Clinical Interpretation', level=1)
        
        # Interpret final BR score
        final_br = scores['final_br_score']
        interpretation_para = doc.add_paragraph()
        interpretation_para.add_run('Overall Assessment: ').bold = True
        
        if final_br >= 85:
            interpretation_para.add_run('The final BR score of ')
            interpretation_para.add_run(str(final_br)).bold = True
            interpretation_para.add_run(' indicates a very high likelihood of significant clinical concerns. ')
            interpretation_para.add_run('This score suggests the presence of notable psychological distress or behavioral patterns that warrant immediate clinical attention and comprehensive evaluation.')
        elif final_br >= 75:
            interpretation_para.add_run('The final BR score of ')
            interpretation_para.add_run(str(final_br)).bold = True
            interpretation_para.add_run(' indicates a high likelihood of clinical significance. ')
            interpretation_para.add_run('This score suggests moderate to significant psychological concerns that should be addressed through appropriate clinical intervention and monitoring.')
        elif final_br >= 65:
            interpretation_para.add_run('The final BR score of ')
            interpretation_para.add_run(str(final_br)).bold = True
            interpretation_para.add_run(' indicates a moderate level of clinical concern. ')
            interpretation_para.add_run('This score suggests some psychological distress or behavioral patterns that may benefit from clinical attention and further assessment.')
        elif final_br >= 35:
            interpretation_para.add_run('The final BR score of ')
            interpretation_para.add_run(str(final_br)).bold = True
            interpretation_para.add_run(' falls within the normal range. ')
            interpretation_para.add_run('This score suggests typical psychological functioning with no significant clinical concerns indicated at this time.')
        else:
            interpretation_para.add_run('The final BR score of ')
            interpretation_para.add_run(str(final_br)).bold = True
            interpretation_para.add_run(' is below the typical range. ')
            interpretation_para.add_run('This unusually low score may indicate either very positive psychological functioning or potential response patterns that warrant further review.')
        
        # Add category-specific interpretations
        doc.add_heading('Category Analysis', level=2)
        
        for category, data in scores['detailed_breakdown'].items():
            if category != 'has_dc_adjustment':
                category_name = category.replace('_', ' ').title()
                score = data['score']
                
                cat_para = doc.add_paragraph()
                cat_para.add_run(f'{category_name}: ').bold = True
                
                if score >= 85:
                    cat_para.add_run(f'Score of {score} indicates very high elevation in this domain, suggesting significant clinical attention is needed.')
                elif score >= 75:
                    cat_para.add_run(f'Score of {score} indicates high elevation in this domain, suggesting clinical significance.')
                elif score >= 65:
                    cat_para.add_run(f'Score of {score} indicates moderate elevation in this domain, warranting clinical consideration.')
                elif score >= 35:
                    cat_para.add_run(f'Score of {score} falls within the normal range for this domain.')
                else:
                    cat_para.add_run(f'Score of {score} is below typical range for this domain.')
        
        # Add denial/complaint adjustment info if applicable
        if scores['detailed_breakdown'].get('has_dc_adjustment'):
            doc.add_heading('Denial/Complaint Adjustment', level=2)
            dc_para = doc.add_paragraph()
            dc_para.add_run('A Denial/Complaint adjustment has been applied to these results. ')
            dc_para.add_run('This adjustment accounts for response patterns that may indicate either ')
            dc_para.add_run('defensive responding (denial) or excessive complaint patterns, ')
            dc_para.add_run('which can affect the interpretation of clinical scales.')
        
        # Add recommendations
        doc.add_heading('Recommendations', level=1)
        rec_para = doc.add_paragraph()
        
        if final_br >= 75:
            rec_para.add_run('• Immediate clinical evaluation recommended\n')
            rec_para.add_run('• Consider comprehensive psychological assessment\n')
            rec_para.add_run('• Monitor for safety concerns\n')
            rec_para.add_run('• Develop appropriate treatment plan\n')
        elif final_br >= 65:
            rec_para.add_run('• Clinical consultation recommended\n')
            rec_para.add_run('• Consider further assessment if indicated\n')
            rec_para.add_run('• Monitor progress over time\n')
        else:
            rec_para.add_run('• Continue routine monitoring\n')
            rec_para.add_run('• Reassess if concerns arise\n')
            rec_para.add_run('• Maintain supportive environment\n')
        
        # Save document to bytes
        doc_buffer = io.BytesIO()
        doc.save(doc_buffer)
        doc_buffer.seek(0)
        
        return Response(
            doc_buffer.getvalue(),
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            headers={'Content-Disposition': f'attachment; filename=assessment_report_{session_id}.docx'}
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    # Only run in debug mode for local development
    app.run(debug=False, host='0.0.0.0', port=5000)
