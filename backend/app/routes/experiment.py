from flask import Blueprint, jsonify
from app.services.experiment_tracker import ExperimentTracker

bp = Blueprint('experiment', __name__)

@bp.route('/experiment/report', methods=['GET'])
def get_experiment_report():
    """Obtener reporte del experimento científico"""
    tracker = ExperimentTracker()
    report = tracker.generate_experiment_report()
    return jsonify(report)