# Dockerfile Optimizado

# --- ETAPA 1: Builder - Instalar dependencias y descargar el modelo ---
FROM python:3.10-slim AS builder

# Establecer el directorio de trabajo
WORKDIR /builder

# 1. Instalar las dependencias del sistema operativo que algunas librerías podrían necesitar
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++

# 2. Copiar solo el archivo de requerimientos
COPY requirements.txt .

# 3. Instalar TODAS las dependencias en una carpeta local llamada 'wheels'
#    Esto aumenta el tiempo de espera de pip a 300 segundos (5 minutos)
RUN pip install \
    --no-cache-dir \
    --timeout=300 \
    -r requirements.txt \
    --target=./wheels

# 4. Copiar el script para descargar el modelo
COPY download_model.py .

# 5. Ejecutar el script para descargar el modelo
RUN python download_model.py

# --- ETAPA 2: Final - Construir la imagen de la aplicación ---
FROM python:3.10-slim

# Establecer el directorio de trabajo final
WORKDIR /code

# Copiar las librerías YA INSTALADAS desde la etapa 'builder'
COPY --from=builder /builder/wheels /usr/local/lib/python3.10/site-packages

# Copiar el modelo pre-descargado desde la etapa 'builder'
COPY --from=builder /builder/model ./model

# Copiar el código de nuestra aplicación (la carpeta 'app')
COPY ./app ./app

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la API
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]