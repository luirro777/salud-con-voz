# Imagen base de python
FROM python:3.10-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear un usuario non-root
RUN useradd --create-home saludconvoz

# Establecer el directorio de trabajo 
WORKDIR /app

# Copiar el código fuente
COPY ./app /app/

# Copiar y instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Crear directorios
RUN mkdir -p /app/media/temp
RUN mkdir -p /app/staticfiles

# Cambiar permisos directorio de la app
RUN chown -R saludconvoz:saludconvoz /app

# Cambiar a usuario non-root
USER saludconvoz

# Exponer el puerto
EXPOSE 8000

# Comando de ejecución de la aplicación
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
