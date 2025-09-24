from flask import Flask, send_from_directory, jsonify, request
import os
from experiment_analysis import run_complete_experiment_analysis, convert_numpy_types

app = Flask(__name__, static_folder="frontend", static_url_path="")

@app.route("/")
def serve_index():
    return send_from_directory("frontend", "index.html")

@app.route("/api/run-analysis", methods=["GET"])
def run_analysis():
    report = run_complete_experiment_analysis()
    report_clean = convert_numpy_types(report)
    return jsonify(report_clean)

@app.route("/api/get-question", methods=["GET"])
def get_question():
    grado = request.args.get("grado", "1")
    report = run_complete_experiment_analysis()
    aciertos = report.get("aciertos", 5)
    total = report.get("total", 10)
    rendimiento = aciertos / total

    if rendimiento < 0.4:
        nivel = "facil"
    elif rendimiento < 0.7:
        nivel = "medio"
    else:
        nivel = "dificil"

    banco = {
        "1": {"facil": "¿Qué es una variable?", "medio": "Explica la diferencia entre variable dependiente e independiente.", "dificil": "Da un ejemplo práctico de un experimento con control de variables."},
        "2": {"facil": "¿Qué es la media aritmética?", "medio": "Explica la diferencia entre media y mediana.", "dificil": "Resuelve: Si las notas son 12, 14 y 18, ¿cuál es la varianza?"},
        "3": {"facil": "¿Qué es una fracción?", "medio": "Convierte 3/4 en número decimal.", "dificil": "Resuelve: ¿Cuál es el mínimo común múltiplo de 12 y 18?"}
    }

    pregunta = banco.get(grado, {}).get(nivel, "Pregunta no disponible")

    return jsonify({
        "grado": grado,
        "nivel_asignado": nivel,
        "rendimiento": round(rendimiento, 2),
        "pregunta": pregunta
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
