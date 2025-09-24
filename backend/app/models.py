from datetime import datetime
from app import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    level = db.Column(db.String(50), nullable=False)
    learning_style = db.Column(db.String(50))  # Visual, Auditivo, Kinestésico
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    experiment_group = db.Column(db.String(20), default='adaptive')  # 'adaptive' o 'traditional'
    
    # Relaciones
    performances = db.relationship('Performance', backref='student', lazy=True)
    sessions = db.relationship('StudySession', backref='student', lazy=True)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # matematicas, ciencias, etc.
    difficulty_base = db.Column(db.Float, default=0.5)  # 0-1 scale
    prerequisites = db.Column(db.Text)  # JSON de temas prerequisitos

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text, nullable=False)  # JSON
    correct_answer = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.Float, nullable=False)  # 0-1 scale
    explanation = db.Column(db.Text)
    question_type = db.Column(db.String(50))  # multiple_choice, fill_blank, etc.

class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    response_time = db.Column(db.Float)  # en segundos
    difficulty_at_time = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    hint_used = db.Column(db.Boolean, default=False)

class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    questions_attempted = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    topics_studied = db.Column(db.Text)  # JSON
    engagement_score = db.Column(db.Float)