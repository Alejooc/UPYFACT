# Upyfact

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0%2B-green)
![Docker](https://img.shields.io/badge/Docker-20.10.0%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Descripción

**Upyfact** es una integración en Python para el sistema de facturación CG1 8.5. Este proyecto utiliza FastAPI para exponer un servidor web que permite interactuar con el sistema de facturación mediante un endpoint para la facturación electrónica.

## Características

- **Servidor FastAPI**: Implementación de un servidor web rápido y eficiente.
- **Integración con CG1 8.5**: Conexión directa con el sistema de facturación CG1 8.1.
- **Endpoint para Facturación Electrónica**: Recepción y procesamiento de datos de facturación en formato JSON.
- **Compatibilidad con Docker**: Fácil despliegue utilizando contenedores Docker.

## Requisitos

- Python 3.8+
- FastAPI 0.68.0+
- Docker 20.10.0+
- paramiko
- CG1 8.5

## Instalación

### Uso sin Docker

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/upyfact.git
    cd upyfact
    ```

2. Crear y activar un entorno virtual:
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Iniciar el servidor FastAPI:
    ```bash
    uvicorn main:app --reload
    ```

5. Acceder a la documentación interactiva de la API en tu navegador:
    ```plaintext
    http://127.0.0.1:8000/docs
    ```

### Uso con Docker

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/upyfact.git
    cd upyfact
    ```

2. Crear la imagen de Docker:
    ```bash
    docker build -t upyfact:latest .
    ```

3. Ejecutar el contenedor:
    ```bash
    docker run -d -p 8000:8000 upyfact:latest
    ```

4. Acceder a la documentación interactiva de la API en tu navegador:
    ```plaintext
    http://127.0.0.1:8000/docs
    ```

## Endpoints

### `POST /electronica`

Este endpoint recibe un JSON con los datos de la factura electrónica y los procesa a través del sistema CG1 8.1.


## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

Contacto
Autor: Alejandro osorio


**¡Gracias por usar Upyfact! 🚀**