
FROM python:3.14-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY src/ ./src/

# Permitir importar el paquete datasentry
ENV PYTHONPATH=/app/src

EXPOSE 8000

# Arrancar la API
CMD ["uvicorn", "datasentry.api:app", "--host", "0.0.0.0", "--port", "8000"]
