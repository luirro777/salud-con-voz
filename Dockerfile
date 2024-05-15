FROM python:3.10

ENV PYTHONUNBUFFERED 1

# Instalación de netcat
RUN apt-get update && \
    apt-get install -y netcat-openbsd

# Instalación de las dependencias del proyecto Python
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copiar la aplicación al contenedor
ADD ./app /app
RUN chmod +x /app

WORKDIR /app
EXPOSE 8000
CMD [ "gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000", "--chdir=/app", "--timeout", "1800" ]
