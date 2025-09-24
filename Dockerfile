# Usamos una imagen oficial de Python
FROM python:3.12-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos requirements y los instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el proyecto
COPY . .

# Exponemos el puerto que Flask usará
EXPOSE 5000

# Comando para iniciar la app
CMD ["python", "backend/backend_adaptive_system.py"]