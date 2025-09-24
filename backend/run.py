from app import create_app, db
from app.utils.data_initializer import initialize_sample_data

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        
        # Verificar si hay datos, si no, inicializar
        from app.models import Topic
        if Topic.query.count() == 0:
            print("📊 Inicializando base de datos con datos de ejemplo...")
            initialize_sample_data()
            print("✅ Base de datos inicializada con datos de ejemplo")
        else:
            print("✅ Base de datos ya contiene datos")
    
    print("🚀 Iniciando servidor del sistema de aprendizaje adaptativo...")
    print("📚 Endpoints disponibles en http://localhost:5000")
    print("🧪 Sistema de experimentación activado")
    print("💾 Base de datos: instance/adaptive_learning.db")
    
    app.run(debug=True, host='0.0.0.0', port=5000)