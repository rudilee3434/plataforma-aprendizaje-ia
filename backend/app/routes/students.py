from flask import Blueprint, request, jsonify
from app import db
from app.models import Student, Performance, Question, Topic, StudySession
from app.services.adaptive_engine import AdaptiveEngine
from app.services.experiment_tracker import ExperimentTracker
import json
from datetime import datetime

bp = Blueprint('students', __name__)

@bp.route('/students', methods=['POST'])
def create_student():
    """Crear nuevo estudiante"""
    data = request.json
    
    student = Student(
        name=data['name'],
        email=data['email'],
        level=data['level'],
        learning_style=data.get('learning_style', 'visual')
    )
    
    db.session.add(student)
    db.session.commit()
    
    # Asignar grupo experimental
    tracker = ExperimentTracker()
    group = tracker.assign_experiment_group(student.id)
    
    return jsonify({
        'id': student.id,
        'name': student.name,
        'experiment_group': group
    })

@bp.route('/students/<int:student_id>/next_question', methods=['GET'])
def get_next_question(student_id):
    """Obtener siguiente pregunta adaptativa"""
    engine = AdaptiveEngine()
    question = engine.select_next_question(student_id)
    
    if not question:
        return jsonify({'error': 'No questions available'}), 404
    
    topic = Topic.query.get(question.topic_id)
    
    return jsonify({
        'id': question.id,
        'content': question.content,
        'options': json.loads(question.options),
        'topic': topic.name,
        'difficulty': question.difficulty,
        'type': question.question_type
    })

@bp.route('/students/<int:student_id>/answer', methods=['POST'])
def submit_answer(student_id):
    """Enviar respuesta del estudiante"""
    data = request.json
    
    performance = Performance(
        student_id=student_id,
        question_id=data['question_id'],
        is_correct=data['is_correct'],
        response_time=data.get('response_time'),
        difficulty_at_time=data.get('difficulty'),
        hint_used=data.get('hint_used', False)
    )
    
    db.session.add(performance)
    db.session.commit()
    
    # Generar feedback adaptativo
    engine = AdaptiveEngine()
    recommendations = engine.generate_recommendation(student_id)
    
    return jsonify({
        'recorded': True,
        'recommendations': recommendations
    })

@bp.route('/students/<int:student_id>/dashboard', methods=['GET'])
def get_dashboard_data(student_id):
    """Obtener datos del dashboard del estudiante"""
    student = Student.query.get_or_404(student_id)
    
    # Calcular estadísticas generales
    all_performances = Performance.query.filter_by(student_id=student_id).all()
    total_questions = len(all_performances)
    correct_answers = sum(1 for p in all_performances if p.is_correct)
    accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Progreso por tema
    topic_progress = {}
    for perf in all_performances:
        question = Question.query.get(perf.question_id)
        topic = Topic.query.get(question.topic_id)
        
        if topic.name not in topic_progress:
            topic_progress[topic.name] = {'correct': 0, 'total': 0}
        
        topic_progress[topic.name]['total'] += 1
        if perf.is_correct:
            topic_progress[topic.name]['correct'] += 1
    
    # Calcular racha de días consecutivos
    sessions = StudySession.query.filter_by(student_id=student_id).order_by(
        StudySession.start_time.desc()
    ).all()
    
    consecutive_days = 0
    if sessions:
        current_date = datetime.now().date()
        for session in sessions:
            session_date = session.start_time.date()
            if (current_date - session_date).days == consecutive_days:
                consecutive_days += 1
                current_date = session_date
            else:
                break
    
    # Generar recomendaciones
    engine = AdaptiveEngine()
    recommendations = engine.generate_recommendation(student_id)
    
    return jsonify({
        'student': {
            'name': student.name,
            'level': student.level,
            'learning_style': student.learning_style
        },
        'stats': {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'accuracy_rate': f"{accuracy:.0f}%",
            'study_streak': consecutive_days
        },
        'topic_progress': topic_progress,
        'recommendations': recommendations,
        'overall_progress': min(100, accuracy)
    })