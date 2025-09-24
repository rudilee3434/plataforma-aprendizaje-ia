import json
from app import db
from app.models import Topic, Question

def initialize_sample_data():
    """Inicializar base de datos con datos de ejemplo"""
    
    # Crear temas
    topics = [
        Topic(name="Fracciones Básicas", category="matematicas", difficulty_base=0.4),
        Topic(name="Suma y Resta", category="matematicas", difficulty_base=0.2),
        Topic(name="Multiplicación", category="matematicas", difficulty_base=0.5),
        Topic(name="División", category="matematicas", difficulty_base=0.6)
    ]
    
    for topic in topics:
        db.session.add(topic)
    db.session.commit()
    
    # Crear preguntas de ejemplo
    questions = [
        Question(
            topic_id=1,  # Fracciones Básicas
            content="¿Cuál de estas fracciones es mayor?",
            options=json.dumps(["3/4", "2/3", "Son iguales", "No se puede determinar"]),
            correct_answer=0,
            difficulty=0.6,
            explanation="3/4 = 0.75 y 2/3 ≈ 0.667, por lo tanto 3/4 es mayor.",
            question_type="multiple_choice"
        ),
        Question(
            topic_id=1,  # Fracciones Básicas
            content="¿Cuál fracción representa la mitad?",
            options=json.dumps(["1/2", "1/3", "2/4", "1/4"]),
            correct_answer=0,
            difficulty=0.3,
            explanation="1/2 representa exactamente la mitad de algo.",
            question_type="multiple_choice"
        ),
        Question(
            topic_id=2,  # Suma y Resta
            content="¿Cuánto es 25 + 37?",
            options=json.dumps(["61", "62", "63", "64"]),
            correct_answer=1,
            difficulty=0.2,
            explanation="25 + 37 = 62",
            question_type="multiple_choice"
        )
    ]
    
    for question in questions:
        db.session.add(question)
    db.session.commit()