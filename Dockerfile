# Usa una imagen base de Python
FROM python:3.12-slim

# Instala las dependencias necesarias
RUN apt-get update && apt-get install -y python3 python3-pip

# Copia el código fuente al contenedor
WORKDIR /app
COPY requirements.txt ./

# Instala las dependencias de tu aplicación
RUN pip install --no-cache-dir -r requirements.txt

COPY ./dist/upyfact /app/
RUN chmod +x /app/upyfact
EXPOSE 5000
# Define el comando por defecto para ejecutar el contenedor
CMD ["./upyfact"]
