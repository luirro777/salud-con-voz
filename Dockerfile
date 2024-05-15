FROM python:3.10

ENV PYTHONUNBUFFERED 1

# Instalación de netcat
RUN apt-get update && \
    apt-get install -y netcat-openbsd

# Copiar el script de espera de MySQL al contenedor
ADD wait-for-mysql.sh /wait-for-mysql.sh

# Dar permisos de ejecución al script
RUN chmod +x /wait-for-mysql.sh

# Instalación de las dependencias del proyecto Python
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copiar la aplicación al contenedor
ADD ./app /app

WORKDIR /app
EXPOSE 8000

# Ejecutar el script de espera de MySQL antes de iniciar el servidor
CMD /wait-for-mysql.sh && gunicorn config.wsgi --bind 0.0.0.0:8000 --chdir=/app --timeout 1800
