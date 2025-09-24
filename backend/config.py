import os

class Config:
    """Configuración base del sistema"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-adaptive-learning-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/adaptive_learning.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración del sistema adaptativo
    ADAPTIVE_CONFIG = {
        'MASTERY_THRESHOLD': 0.8,
        'STRUGGLE_THRESHOLD': 0.4,
        'DIFFICULTY_ADJUSTMENT_RATE': 0.1,
        'MIN_QUESTIONS_FOR_ANALYSIS': 5,
        'PERFORMANCE_WINDOW_DAYS': 7
    }
    
    # Configuración del experimento
    EXPERIMENT_CONFIG = {
        'GROUPS': ['adaptive', 'traditional'],
        'RANDOMIZATION_SEED': 42,
        'MIN_SAMPLE_SIZE': 30,
        'STUDY_DURATION_WEEKS': 2
    }

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
