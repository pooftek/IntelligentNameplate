from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///classroom_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
socketio = SocketIO(app, cors_allowed_origins="*")

# Database Models
class Professor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    rfid_card_id = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    class_code = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    professor = db.relationship('Professor', backref=db.backref('classes', lazy=True))

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    class_obj = db.relationship('Class', backref=db.backref('enrollments', lazy=True))
    student = db.relationship('Student', backref=db.backref('enrollments', lazy=True))

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    present = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    class_obj = db.relationship('Class', backref=db.backref('attendances', lazy=True))
    student = db.relationship('Student', backref=db.backref('attendances', lazy=True))

class Participation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    peer_grade = db.Column(db.Float, default=0.0)
    instructor_grade = db.Column(db.Float, default=0.0)
    hand_raises = db.Column(db.Integer, default=0)
    thumbs_up = db.Column(db.Integer, default=0)
    thumbs_down = db.Column(db.Integer, default=0)
    class_obj = db.relationship('Class', backref=db.backref('participations', lazy=True))
    student = db.relationship('Student', backref=db.backref('participations', lazy=True))

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    options = db.Column(db.Text, nullable=False)  # JSON string
    correct_answer = db.Column(db.Integer, nullable=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    class_obj = db.relationship('Class', backref=db.backref('polls', lazy=True))

class PollResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    answer = db.Column(db.Integer, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    poll = db.relationship('Poll', backref=db.backref('responses', lazy=True))
    student = db.relationship('Student', backref=db.backref('poll_responses', lazy=True))

class ClassSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False, unique=True)
    show_first_name_only = db.Column(db.Boolean, default=False)
    quiet_mode = db.Column(db.Boolean, default=False)
    class_obj = db.relationship('Class', backref=db.backref('settings', uselist=False))

@login_manager.user_loader
def load_user(user_id):
    return Professor.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type', 'professor')
        
        if user_type == 'professor':
            professor = Professor.query.filter_by(username=username).first()
            if professor and check_password_hash(professor.password_hash, password):
                login_user(professor)
                return jsonify({'success': True, 'redirect': url_for('dashboard')})
            return jsonify({'success': False, 'error': 'Invalid credentials'})
        else:
            # Student login will be handled differently
            return jsonify({'success': False, 'error': 'Use student interface'})
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form.to_dict()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'success': False, 'error': 'All fields are required'})
        
        # Check if username already exists
        if Professor.query.filter_by(username=username).first():
            return jsonify({'success': False, 'error': 'Username already exists'})
        
        # Check if email already exists
        if Professor.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'Email already exists'})
        
        # Create new professor
        professor = Professor(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(professor)
        db.session.commit()
        
        # Auto-login the new professor
        login_user(professor)
        
        return jsonify({'success': True, 'redirect': url_for('dashboard')})
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    classes = Class.query.filter_by(professor_id=current_user.id).all()
    return render_template('dashboard.html', classes=classes)

@app.route('/preferences')
@login_required
def preferences():
    return render_template('preferences.html')

@app.route('/classroom/<int:class_id>')
@login_required
def classroom(class_id):
    class_obj = Class.query.get_or_404(class_id)
    if class_obj.professor_id != current_user.id:
        return redirect(url_for('dashboard'))
    
    students = db.session.query(Student).join(Enrollment).filter(
        Enrollment.class_id == class_id
    ).all()
    
    settings = ClassSettings.query.filter_by(class_id=class_id).first()
    if not settings:
        settings = ClassSettings(class_id=class_id)
        db.session.add(settings)
        db.session.commit()
    
    return render_template('classroom.html', class_obj=class_obj, students=students, settings=settings)

@app.route('/api/start_class/<int:class_id>', methods=['POST'])
@login_required
def start_class(class_id):
    class_obj = Class.query.get_or_404(class_id)
    if class_obj.professor_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    class_obj.is_active = True
    db.session.commit()
    
    socketio.emit('class_started', {'class_id': class_id, 'class_code': class_obj.class_code}, room=f'class_{class_id}')
    
    return jsonify({'success': True, 'redirect': url_for('faculty_dashboard', class_id=class_id)})

@app.route('/api/stop_class/<int:class_id>', methods=['POST'])
@login_required
def stop_class(class_id):
    class_obj = Class.query.get_or_404(class_id)
    if class_obj.professor_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    class_obj.is_active = False
    db.session.commit()
    
    # Update gradebook with participation data
    update_gradebook(class_id)
    
    socketio.emit('class_stopped', {'class_id': class_id}, room=f'class_{class_id}')
    
    return jsonify({'success': True})

def update_gradebook(class_id):
    today = datetime.utcnow().date()
    students = db.session.query(Student).join(Enrollment).filter(
        Enrollment.class_id == class_id
    ).all()
    
    for student in students:
        participation = Participation.query.filter_by(
            class_id=class_id,
            student_id=student.id,
            date=today
        ).first()
        
        if not participation:
            participation = Participation(
                class_id=class_id,
                student_id=student.id,
                date=today
            )
            db.session.add(participation)
        
        # Calculate poll grade
        poll_responses = PollResponse.query.join(Poll).filter(
            Poll.class_id == class_id,
            PollResponse.student_id == student.id,
            Poll.created_at >= datetime.combine(today, datetime.min.time())
        ).all()
        
        poll_grade = 0.0
        if poll_responses:
            correct_count = sum(1 for pr in poll_responses if pr.is_correct)
            poll_grade = (correct_count / len(poll_responses)) * 100
        
        db.session.commit()

@app.route('/faculty_dashboard/<int:class_id>')
@login_required
def faculty_dashboard(class_id):
    class_obj = Class.query.get_or_404(class_id)
    if class_obj.professor_id != current_user.id:
        return redirect(url_for('dashboard'))
    
    students = db.session.query(Student).join(Enrollment).filter(
        Enrollment.class_id == class_id
    ).all()
    
    active_poll = Poll.query.filter_by(class_id=class_id, is_active=True).first()
    
    return render_template('faculty_dashboard.html', class_obj=class_obj, students=students, active_poll=active_poll)

@app.route('/api/gradebook/<int:class_id>')
@login_required
def get_gradebook(class_id):
    class_obj = Class.query.get_or_404(class_id)
    if class_obj.professor_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    students = db.session.query(Student).join(Enrollment).filter(
        Enrollment.class_id == class_id
    ).all()
    
    gradebook_data = []
    for student in students:
        attendances = Attendance.query.filter_by(
            class_id=class_id,
            student_id=student.id
        ).all()
        
        participations = Participation.query.filter_by(
            class_id=class_id,
            student_id=student.id
        ).all()
        
        poll_responses = PollResponse.query.join(Poll).filter(
            Poll.class_id == class_id,
            PollResponse.student_id == student.id
        ).all()
        
        attendance_count = sum(1 for a in attendances if a.present)
        total_classes = len(attendances)
        attendance_grade = (attendance_count / total_classes * 100) if total_classes > 0 else 0
        
        avg_peer_grade = sum(p.peer_grade for p in participations) / len(participations) if participations else 0
        avg_instructor_grade = sum(p.instructor_grade for p in participations) / len(participations) if participations else 0
        
        poll_grade = 0
        if poll_responses:
            correct_count = sum(1 for pr in poll_responses if pr.is_correct)
            poll_grade = (correct_count / len(poll_responses)) * 100
        
        gradebook_data.append({
            'student_id': student.id,
            'student_number': student.student_number,
            'name': f"{student.first_name} {student.last_name}",
            'attendance_grade': round(attendance_grade, 2),
            'peer_participation': round(avg_peer_grade, 2),
            'instructor_participation': round(avg_instructor_grade, 2),
            'poll_grade': round(poll_grade, 2)
        })
    
    return jsonify(gradebook_data)

@app.route('/api/update_settings/<int:class_id>', methods=['POST'])
@login_required
def update_settings(class_id):
    class_obj = Class.query.get_or_404(class_id)
    if class_obj.professor_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    settings = ClassSettings.query.filter_by(class_id=class_id).first()
    if not settings:
        settings = ClassSettings(class_id=class_id)
        db.session.add(settings)
    
    data = request.get_json()
    settings.show_first_name_only = data.get('show_first_name_only', False)
    settings.quiet_mode = data.get('quiet_mode', False)
    
    db.session.commit()
    
    socketio.emit('settings_updated', {
        'show_first_name_only': settings.show_first_name_only,
        'quiet_mode': settings.quiet_mode
    }, room=f'class_{class_id}')
    
    return jsonify({'success': True})

@app.route('/api/create_poll/<int:class_id>', methods=['POST'])
@login_required
def create_poll(class_id):
    class_obj = Class.query.get_or_404(class_id)
    if class_obj.professor_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    data = request.get_json()
    question = data.get('question')
    options = data.get('options', [])
    correct_answer = data.get('correct_answer')
    is_anonymous = data.get('is_anonymous', False)
    
    # Deactivate any existing active polls
    Poll.query.filter_by(class_id=class_id, is_active=True).update({'is_active': False})
    
    poll = Poll(
        class_id=class_id,
        question=question,
        options=json.dumps(options),
        correct_answer=correct_answer,
        is_anonymous=is_anonymous,
        is_active=True
    )
    db.session.add(poll)
    db.session.commit()
    
    socketio.emit('poll_started', {
        'poll_id': poll.id,
        'question': question,
        'options': options,
        'is_anonymous': is_anonymous
    }, room=f'class_{class_id}')
    
    return jsonify({'success': True, 'poll_id': poll.id})

@app.route('/api/stop_poll/<int:poll_id>', methods=['POST'])
@login_required
def stop_poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    class_obj = Class.query.get_or_404(poll.class_id)
    if class_obj.professor_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    poll.is_active = False
    db.session.commit()
    
    socketio.emit('poll_stopped', {'poll_id': poll_id}, room=f'class_{poll.class_id}')
    
    return jsonify({'success': True})

@app.route('/api/create_class', methods=['POST'])
@login_required
def create_class():
    data = request.get_json()
    name = data.get('name')
    class_code = data.get('class_code')
    
    if not name or not class_code:
        return jsonify({'success': False, 'error': 'Name and class code required'})
    
    if Class.query.filter_by(class_code=class_code).first():
        return jsonify({'success': False, 'error': 'Class code already exists'})
    
    class_obj = Class(
        professor_id=current_user.id,
        name=name,
        class_code=class_code
    )
    db.session.add(class_obj)
    db.session.commit()
    
    return jsonify({'success': True, 'class_id': class_obj.id})

@app.route('/api/delete_class/<int:class_id>', methods=['DELETE'])
@login_required
def delete_class(class_id):
    class_obj = Class.query.get_or_404(class_id)
    if class_obj.professor_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    try:
        # Delete all related records
        # First, delete poll responses for polls in this class
        polls = Poll.query.filter_by(class_id=class_id).all()
        for poll in polls:
            PollResponse.query.filter_by(poll_id=poll.id).delete()
        
        # Delete polls
        Poll.query.filter_by(class_id=class_id).delete()
        
        # Delete participations
        Participation.query.filter_by(class_id=class_id).delete()
        
        # Delete attendances
        Attendance.query.filter_by(class_id=class_id).delete()
        
        # Delete enrollments
        Enrollment.query.filter_by(class_id=class_id).delete()
        
        # Delete class settings
        ClassSettings.query.filter_by(class_id=class_id).delete()
        
        # Finally, delete the class
        db.session.delete(class_obj)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/add_student_to_class', methods=['POST'])
@login_required
def add_student_to_class():
    data = request.get_json()
    class_id = data.get('class_id')
    student_id = data.get('student_id')
    
    class_obj = Class.query.get_or_404(class_id)
    if class_obj.professor_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'})
    
    enrollment = Enrollment.query.filter_by(
        class_id=class_id,
        student_id=student_id
    ).first()
    
    if enrollment:
        return jsonify({'success': False, 'error': 'Student already enrolled'})
    
    enrollment = Enrollment(class_id=class_id, student_id=student_id)
    db.session.add(enrollment)
    db.session.commit()
    
    return jsonify({'success': True})

# Student routes
@app.route('/student')
def student_interface():
    return render_template('student_interface.html')

@app.route('/api/student/login', methods=['POST'])
def student_login():
    data = request.get_json()
    rfid_card_id = data.get('rfid_card_id')
    student_number = data.get('student_number')
    
    if rfid_card_id:
        student = Student.query.filter_by(rfid_card_id=rfid_card_id).first()
    elif student_number:
        student = Student.query.filter_by(student_number=student_number).first()
    else:
        return jsonify({'success': False, 'error': 'No identification provided'})
    
    if student:
        session['student_id'] = student.id
        return jsonify({
            'success': True,
            'student': {
                'id': student.id,
                'student_number': student.student_number,
                'first_name': student.first_name,
                'last_name': student.last_name
            }
        })
    
    return jsonify({'success': False, 'error': 'Student not found'})

@app.route('/api/student/register', methods=['POST'])
def student_register():
    data = request.get_json()
    student_number = data.get('student_number')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    rfid_card_id = data.get('rfid_card_id')
    
    if Student.query.filter_by(student_number=student_number).first():
        return jsonify({'success': False, 'error': 'Student number already exists'})
    
    student = Student(
        student_number=student_number,
        first_name=first_name,
        last_name=last_name,
        rfid_card_id=rfid_card_id
    )
    db.session.add(student)
    db.session.commit()
    
    session['student_id'] = student.id
    
    return jsonify({
        'success': True,
        'student': {
            'id': student.id,
            'student_number': student.student_number,
            'first_name': student.first_name,
            'last_name': student.last_name
        }
    })

@app.route('/api/student/classes')
def get_active_classes():
    active_classes = Class.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'class_code': c.class_code
    } for c in active_classes])

@app.route('/api/student/join_class', methods=['POST'])
def student_join_class():
    student_id = session.get('student_id')
    if not student_id:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    data = request.get_json()
    class_id = data.get('class_id')
    
    class_obj = Class.query.get_or_404(class_id)
    if not class_obj.is_active:
        return jsonify({'success': False, 'error': 'Class is not active'})
    
    # Check if already enrolled
    enrollment = Enrollment.query.filter_by(
        class_id=class_id,
        student_id=student_id
    ).first()
    
    if not enrollment:
        enrollment = Enrollment(class_id=class_id, student_id=student_id)
        db.session.add(enrollment)
    
    # Mark attendance
    today = datetime.utcnow().date()
    attendance = Attendance.query.filter_by(
        class_id=class_id,
        student_id=student_id,
        date=today
    ).first()
    
    if not attendance:
        attendance = Attendance(
            class_id=class_id,
            student_id=student_id,
            date=today,
            present=True
        )
        db.session.add(attendance)
    
    db.session.commit()
    
    socketio.emit('student_joined', {
        'student_id': student_id,
        'class_id': class_id
    }, room=f'class_{class_id}')
    
    return jsonify({'success': True, 'class_id': class_id})

@app.route('/api/student/interaction', methods=['POST'])
def student_interaction():
    try:
        student_id = session.get('student_id')
        if not student_id:
            return jsonify({'success': False, 'error': 'Not logged in'})
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        class_id = data.get('class_id')
        interaction_type = data.get('type')  # 'hand_raise', 'thumbs_up', 'thumbs_down'
        
        if not class_id:
            return jsonify({'success': False, 'error': 'Class ID required'})
        
        if not interaction_type:
            return jsonify({'success': False, 'error': 'Interaction type required'})
        
        today = datetime.utcnow().date()
        participation = Participation.query.filter_by(
            class_id=class_id,
            student_id=student_id,
            date=today
        ).first()
        
        if not participation:
            participation = Participation(
                class_id=class_id,
                student_id=student_id,
                date=today
            )
            db.session.add(participation)
        
        # Ensure fields are initialized to 0 if None
        if participation.hand_raises is None:
            participation.hand_raises = 0
        if participation.thumbs_up is None:
            participation.thumbs_up = 0
        if participation.thumbs_down is None:
            participation.thumbs_down = 0
        
        if interaction_type == 'hand_raise':
            participation.hand_raises += 1
        elif interaction_type == 'thumbs_up':
            participation.thumbs_up += 1
        elif interaction_type == 'thumbs_down':
            participation.thumbs_down += 1
        else:
            return jsonify({'success': False, 'error': 'Invalid interaction type'})
        
        db.session.commit()
        
        socketio.emit('student_interaction', {
            'student_id': student_id,
            'class_id': class_id,
            'type': interaction_type
        }, room=f'class_{class_id}')
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/student/poll_response', methods=['POST'])
def student_poll_response():
    student_id = session.get('student_id')
    if not student_id:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    data = request.get_json()
    poll_id = data.get('poll_id')
    answer = data.get('answer')
    
    poll = Poll.query.get_or_404(poll_id)
    if not poll.is_active:
        return jsonify({'success': False, 'error': 'Poll is not active'})
    
    # Check if already responded
    existing = PollResponse.query.filter_by(
        poll_id=poll_id,
        student_id=student_id
    ).first()
    
    if existing:
        return jsonify({'success': False, 'error': 'Already responded'})
    
    is_correct = (poll.correct_answer is not None and answer == poll.correct_answer)
    
    response = PollResponse(
        poll_id=poll_id,
        student_id=student_id,
        answer=answer,
        is_correct=is_correct
    )
    db.session.add(response)
    db.session.commit()
    
    socketio.emit('poll_response', {
        'poll_id': poll_id,
        'student_id': student_id,
        'answer': answer,
        'is_correct': is_correct,
        'is_anonymous': poll.is_anonymous
    }, room=f'class_{poll.class_id}')
    
    return jsonify({'success': True, 'is_correct': is_correct})

# SocketIO Events
@socketio.on('connect')
def on_connect():
    emit('connected', {'data': 'Connected'})

@socketio.on('join_class')
def on_join_class(data):
    class_id = data.get('class_id')
    join_room(f'class_{class_id}')
    emit('joined_class', {'class_id': class_id})

@socketio.on('get_live_stats')
def on_get_live_stats(data):
    class_id = data.get('class_id')
    
    students = db.session.query(Student).join(Enrollment).filter(
        Enrollment.class_id == class_id
    ).all()
    
    today = datetime.utcnow().date()
    present_students = db.session.query(Student).join(Attendance).filter(
        Attendance.class_id == class_id,
        Attendance.date == today,
        Attendance.present == True
    ).all()
    
    participations = Participation.query.filter_by(
        class_id=class_id,
        date=today
    ).all()
    
    total_hand_raises = sum(p.hand_raises for p in participations)
    total_thumbs_up = sum(p.thumbs_up for p in participations)
    total_thumbs_down = sum(p.thumbs_down for p in participations)
    
    active_poll = Poll.query.filter_by(class_id=class_id, is_active=True).first()
    poll_stats = None
    if active_poll:
        responses = PollResponse.query.filter_by(poll_id=active_poll.id).all()
        option_counts = {}
        for i in range(len(json.loads(active_poll.options))):
            option_counts[i] = sum(1 for r in responses if r.answer == i)
        poll_stats = {
            'poll_id': active_poll.id,
            'question': active_poll.question,
            'options': json.loads(active_poll.options),
            'option_counts': option_counts,
            'total_responses': len(responses),
            'is_anonymous': active_poll.is_anonymous
        }
    
    emit('live_stats', {
        'total_students': len(students),
        'present_students': len(present_students),
        'total_hand_raises': total_hand_raises,
        'total_thumbs_up': total_thumbs_up,
        'total_thumbs_down': total_thumbs_down,
        'poll_stats': poll_stats
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create a default professor for testing
        if not Professor.query.first():
            default_prof = Professor(
                username='professor',
                email='prof@example.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(default_prof)
            db.session.commit()
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

