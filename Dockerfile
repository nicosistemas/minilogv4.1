FROM python:3.12-slim

WORKDIR /app

# Asegura que los módulos del proyecto sean importables
ENV PYTHONPATH=/app

# Dependencias primero (aprovecha cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código fuente
COPY . .

# Directorio de datos persistente (montado como volumen)
RUN mkdir -p /app/data/users

EXPOSE 5000

CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]
