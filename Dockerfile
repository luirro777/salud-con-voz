# Utiliza una imagen base de Linux, como Ubuntu
FROM python:3.10

# Instalación de netcat
RUN apt-get update && \
    apt-get install -y netcat-openbsd

# Copia el archivo wait-for-mysql.sh al contenedor
COPY wait-for-mysql.sh /

# Otorga permisos de ejecución al archivo wait-for-mysql.sh
RUN chmod +x /wait-for-mysql.sh

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalación de las dependencias del proyecto Python
ADD requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./app .

# Ejecuta el script ejemplo.sh cuando el contenedor se inicie
EXPOSE 8000
ENTRYPOINT ["/wait-for-mysql.sh"]
CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000", "--chdir=/app", "--timeout", "1800"]
