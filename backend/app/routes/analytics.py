from flask import Blueprint, jsonify
from app.services.adaptive_engine import AdaptiveEngine
from app.models import Performance

bp = Blueprint('analytics', __name__)

@bp.route('/analytics/learning_patterns/<int:student_id>', methods=['GET'])
def get_learning_patterns(student_id):
    """Análisis avanzado de patrones de aprendizaje"""
    engine = AdaptiveEngine()
    patterns = engine.analyze_learning_patterns(student_id)
    
    # Datos adicionales para visualización
    performances = Performance.query.filter_by(student_id=student_id).order_by(
        Performance.timestamp
    ).all()
    
    timeline_data = []
    for perf in performances:
        timeline_data.append({
            'timestamp': perf.timestamp.isoformat(),
            'difficulty': perf.difficulty_at_time,
            'success': perf.is_correct,
            'response_time': perf.response_time
        })
    
    return jsonify({
        'patterns': patterns,
        'timeline': timeline_data,
        'insights': engine.generate_recommendation(student_id)
    })