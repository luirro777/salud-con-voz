# Utiliza una imagen base de Linux, como Ubuntu
FROM python:3.10

# Add user that will be used in the container.
RUN useradd ciecs

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Instalación de netcat
RUN apt-get update && \
    apt-get install -y netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Instalación de las dependencias del proyecto Python
ADD requirements.txt ./
RUN pip install -r /requirements.txt

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app
RUN chown ciecs:ciecs /app

# Use user "ciecs" to run the build commands below and the server itself.
USER ciecs

# Set this directory to be owned by the "ciecs" user. This ciecs project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
COPY --chown=ciecs:ciecs app .

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

# Copia el archivo wait-for-mysql.sh al contenedor
COPY --chown=ciecs:ciecs wait-for-mysql.sh /

ENTRYPOINT ["/wait-for-mysql.sh"]

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   app instance can be started with a simple "docker run" command.
CMD set -xe; python manage.py migrate --noinput; gunicorn config.wsgi:application
