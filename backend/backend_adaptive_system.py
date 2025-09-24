from flask import Flask, jsonify
from experiment_analysis import run_complete_experiment_analysis, convert_numpy_types

app = Flask(__name__)

@app.route("/api/run-analysis", methods=["GET"])
def run_analysis():
    report = run_complete_experiment_analysis()
    report_clean = convert_numpy_types(report)
    return jsonify(report_clean)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
