const API_URL = "http://localhost:5000"; // Cambiar en producción al dominio del hosting

// Cargar datos desde la BD
async function cargarDatos() {
    const response = await fetch(`${API_URL}/get-data`);
    const data = await response.json();
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
}

// Ejecutar análisis con experiment_analysis.py
async function ejecutarAnalisis() {
    const response = await fetch(`${API_URL}/run-analysis`);
    const result = await response.json();
    document.getElementById("output").textContent = JSON.stringify(result, null, 2);
}

// Guardar respuesta en la BD
document.getElementById("respuestaForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const respuesta = document.getElementById("respuestaInput").value;

    const response = await fetch(`${API_URL}/save-response`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ respuesta })
    });

    const result = await response.json();
    document.getElementById("output").textContent = JSON.stringify(result, null, 2);
});
