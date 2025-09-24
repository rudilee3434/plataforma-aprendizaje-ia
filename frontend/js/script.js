async function cargarPregunta() {
    let grado = document.getElementById("grado").value;

    try {
        let response = await fetch(`http://127.0.0.1:5000/api/get-question?grado=${grado}`);
        let data = await response.json();

        document.getElementById("resultado").innerText =
            `Grado: ${data.grado} | Rendimiento: ${(data.rendimiento * 100).toFixed(0)}% | Nivel: ${data.nivel_asignado}`;

        document.getElementById("pregunta").innerText = data.pregunta;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("pregunta").innerText = "Error al obtener pregunta.";
    }
}

