from flask import Flask, jsonify, request
from experiment_analysis import run_complete_experiment_analysis, convert_numpy_types

app = Flask(__name__)

# Banco de preguntas por grado y dificultad
banco = {
    "1": {
        "facil": "¿Qué es una variable?",
        "medio": "Explica la diferencia entre variable dependiente e independiente.",
        "dificil": "Da un ejemplo práctico de un experimento con control de variables."
    },
    "2": {
        "facil": "¿Qué es la media aritmética?",
        "medio": "Explica la diferencia entre media y mediana.",
        "dificil": "Resuelve: Si las notas son 12, 14 y 18, ¿cuál es la varianza?"
    },
    "3": {
        "facil": "¿Qué es una fracción?",
        "medio": "Convierte 3/4 en número decimal.",
        "dificil": "Resuelve: ¿Cuál es el mínimo común múltiplo de 12 y 18?"
    }
}

@app.route("/api/run-analysis", methods=["GET"])
def run_analysis():
    report = run_complete_experiment_analysis()
    report_clean = convert_numpy_types(report)
    return jsonify(report_clean)

@app.route("/api/get-question", methods=["GET"])
def get_question():
    grado = request.args.get("grado", "1")

    # Ejecutamos análisis
    report = run_complete_experiment_analysis()
    aciertos = report.get("aciertos", 5)
    total = report.get("total", 10)
    rendimiento = aciertos / total

    # Nivel adaptativo
    if rendimiento < 0.4:
        nivel = "facil"
    elif rendimiento < 0.7:
        nivel = "medio"
    else:
        nivel = "dificil"

    pregunta = banco.get(grado, {}).get(nivel, "Pregunta no disponible")

    return jsonify({
        "grado": grado,
        "nivel_asignado": nivel,
        "rendimiento": round(rendimiento, 2),
        "pregunta": pregunta
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
