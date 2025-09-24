import random
import numpy as np
from app.models import Student, Performance
from scipy import stats

class ExperimentTracker:
    """Sistema para rastrear datos del experimento científico"""
    
    def __init__(self, experiment_groups=None):
        self.experiment_groups = experiment_groups or ['adaptive', 'traditional']
    
    def assign_experiment_group(self, student_id):
        """Asigna estudiante a grupo experimental de forma aleatoria"""
        group = random.choice(self.experiment_groups)
        
        student = Student.query.get(student_id)
        if student:
            student.experiment_group = group
            from app import db
            db.session.commit()
        
        return group
    
    @staticmethod
    def collect_pre_test_data(student_id, scores):
        """Recolecta datos de pre-test para comparación"""
        # Almacenar en tabla separada o como metadatos del estudiante
        pass
    
    def generate_experiment_report(self):
        """Genera reporte del experimento comparando grupos"""
        adaptive_students = Student.query.filter_by(experiment_group='adaptive').all()
        traditional_students = Student.query.filter_by(experiment_group='traditional').all()
        
        adaptive_performance = []
        traditional_performance = []
        
        for student in adaptive_students:
            performances = Performance.query.filter_by(student_id=student.id).all()
            if performances:
                success_rate = sum(1 for p in performances if p.is_correct) / len(performances)
                adaptive_performance.append(success_rate)
        
        for student in traditional_students:
            performances = Performance.query.filter_by(student_id=student.id).all()
            if performances:
                success_rate = sum(1 for p in performances if p.is_correct) / len(performances)
                traditional_performance.append(success_rate)
        
        report = {
            'adaptive_group': {
                'count': len(adaptive_performance),
                'avg_performance': np.mean(adaptive_performance) if adaptive_performance else 0,
                'std_performance': np.std(adaptive_performance) if adaptive_performance else 0
            },
            'traditional_group': {
                'count': len(traditional_performance),
                'avg_performance': np.mean(traditional_performance) if traditional_performance else 0,
                'std_performance': np.std(traditional_performance) if traditional_performance else 0
            }
        }
        
        # Realizar t-test si hay suficientes datos
        if len(adaptive_performance) >= 10 and len(traditional_performance) >= 10:
            t_stat, p_value = stats.ttest_ind(adaptive_performance, traditional_performance)
            report['statistical_test'] = {
                't_statistic': float(t_stat),
                'p_value': float(p_value),
                'significant': p_value < 0.05
            }
        
        return report