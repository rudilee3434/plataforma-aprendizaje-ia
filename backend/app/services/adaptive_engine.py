import numpy as np
from sklearn.cluster import KMeans
from app import db
from app.models import Performance, Question, Topic
import logging

logger = logging.getLogger(__name__)

class AdaptiveEngine:
    def __init__(self, difficulty_adjustment_rate=0.1, mastery_threshold=0.8, struggle_threshold=0.4):
        self.difficulty_adjustment_rate = difficulty_adjustment_rate
        self.mastery_threshold = mastery_threshold
        self.struggle_threshold = struggle_threshold
        
    def calculate_student_ability(self, student_id, topic_id):
        """Calcula la habilidad actual del estudiante en un tema específico"""
        recent_performances = Performance.query.filter_by(
            student_id=student_id
        ).join(Question).filter(
            Question.topic_id == topic_id
        ).order_by(Performance.timestamp.desc()).limit(10).all()
        
        if not recent_performances:
            return 0.5  # Habilidad neutral por defecto
        
        # Calcular tasa de éxito con peso temporal (respuestas recientes pesan más)
        total_weight = 0
        weighted_success = 0
        
        for i, perf in enumerate(recent_performances):
            weight = 1.0 / (i + 1)  # Peso decreciente
            total_weight += weight
            if perf.is_correct:
                weighted_success += weight
        
        ability = weighted_success / total_weight if total_weight > 0 else 0.5
        
        # Ajustar por tiempo de respuesta
        avg_response_time = np.mean([p.response_time for p in recent_performances if p.response_time])
        if avg_response_time:
            # Bonificación por respuestas rápidas
            time_factor = max(0.8, min(1.2, 30 / avg_response_time))
            ability *= time_factor
        
        return min(1.0, max(0.0, ability))
    
    def get_optimal_difficulty(self, student_ability):
        """Calcula la dificultad óptima basada en la teoría de la zona de desarrollo próximo"""
        # La dificultad óptima debe estar ligeramente por encima de la habilidad actual
        optimal_difficulty = student_ability + 0.15
        return min(0.95, max(0.05, optimal_difficulty))
    
    def select_next_question(self, student_id):
        """Selecciona la siguiente pregunta usando algoritmo adaptativo"""
        # Obtener temas donde el estudiante necesita más práctica
        struggling_topics = self.identify_struggling_topics(student_id)
        
        if struggling_topics:
            topic_id = struggling_topics[0]['topic_id']
        else:
            # Seleccionar tema siguiente en el currículum
            topic_id = self.get_next_curriculum_topic(student_id)
        
        student_ability = self.calculate_student_ability(student_id, topic_id)
        optimal_difficulty = self.get_optimal_difficulty(student_ability)
        
        # Buscar pregunta con dificultad más cercana a la óptima
        question = Question.query.filter_by(topic_id=topic_id).order_by(
            db.func.abs(Question.difficulty - optimal_difficulty)
        ).first()
        
        return question
    
    def identify_struggling_topics(self, student_id):
        """Identifica temas donde el estudiante tiene dificultades"""
        topic_performance = db.session.query(
            Question.topic_id,
            db.func.avg(Performance.is_correct.cast(db.Float)).label('success_rate'),
            db.func.count(Performance.id).label('attempts')
        ).join(Performance).filter(
            Performance.student_id == student_id
        ).group_by(Question.topic_id).having(
            db.func.count(Performance.id) >= 3  # Mínimo 3 intentos
        ).all()
        
        struggling = []
        for topic_id, success_rate, attempts in topic_performance:
            if success_rate < self.struggle_threshold:
                struggling.append({
                    'topic_id': topic_id,
                    'success_rate': success_rate,
                    'priority': (self.struggle_threshold - success_rate) * attempts
                })
        
        return sorted(struggling, key=lambda x: x['priority'], reverse=True)
    
    def get_next_curriculum_topic(self, student_id):
        """Obtiene el siguiente tema según el currículum adaptativo"""
        # Lógica simplificada: rotar entre temas disponibles
        topics = Topic.query.all()
        return topics[0].id if topics else 1
    
    def analyze_learning_patterns(self, student_id):
        """Analiza patrones de aprendizaje usando ML básico"""
        performances = Performance.query.filter_by(student_id=student_id).all()
        
        if len(performances) < 10:
            return {"pattern": "insufficient_data"}
        
        # Preparar datos para análisis
        features = []
        for perf in performances:
            features.append([
                perf.difficulty_at_time,
                perf.response_time or 30,  # Default si no hay tiempo
                1 if perf.is_correct else 0,
                1 if perf.hint_used else 0
            ])
        
        X = np.array(features)
        
        # Clustering simple para identificar patrones
        try:
            kmeans = KMeans(n_clusters=3, random_state=42)
            clusters = kmeans.fit_predict(X)
            
            # Analizar clusters
            patterns = {}
            for i in range(3):
                cluster_data = X[clusters == i]
                if len(cluster_data) > 0:
                    patterns[f'cluster_{i}'] = {
                        'avg_difficulty': float(np.mean(cluster_data[:, 0])),
                        'avg_response_time': float(np.mean(cluster_data[:, 1])),
                        'success_rate': float(np.mean(cluster_data[:, 2])),
                        'hint_usage': float(np.mean(cluster_data[:, 3])),
                        'size': len(cluster_data)
                    }
            
            return patterns
        except Exception as e:
            logger.error(f"Error en análisis de patrones: {e}")
            return {"pattern": "analysis_error"}
    
    def generate_recommendation(self, student_id):
        """Genera recomendaciones personalizadas basadas en IA"""
        patterns = self.analyze_learning_patterns(student_id)
        struggling_topics = self.identify_struggling_topics(student_id)
        
        recommendations = []
        
        # Recomendaciones basadas en temas con dificultades
        if struggling_topics:
            topic = Topic.query.get(struggling_topics[0]['topic_id'])
            recommendations.append(
                f"Necesitas reforzar {topic.name}. Tu tasa de éxito es {struggling_topics[0]['success_rate']:.0%}."
            )
        
        # Recomendaciones basadas en patrones de aprendizaje
        if 'cluster_0' in patterns:
            dominant_cluster = max(patterns.values(), key=lambda x: x['size'])
            if dominant_cluster['avg_response_time'] > 45:
                recommendations.append("Tómate más tiempo para leer las preguntas cuidadosamente.")
            if dominant_cluster['hint_usage'] > 0.3:
                recommendations.append("Trata de resolver más problemas sin usar pistas.")
        
        return recommendations if recommendations else ["¡Excelente progreso! Continúa practicando."]