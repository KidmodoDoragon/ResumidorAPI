# Dockerfile - Versión Súper Optimizada

# --- ETAPA 1: Builder - Instalar dependencias y descargar el modelo ---
FROM python:3.10-slim AS builder

# Establecer el directorio de trabajo
WORKDIR /builder

# 1. Copiar solo el archivo de requerimientos
COPY requirements.txt .

# 2. Instalar TODAS las dependencias de Python.
#    Confiamos en que pip descargue los wheels pre-compilados.
#    Mantenemos el timeout largo por si acaso.
RUN pip install \
    --no-cache-dir \
    --timeout=300 \
    -r requirements.txt \
    --target=./wheels

# 3. Copiar el script para descargar el modelo
COPY download_model.py .

# 4. Ejecutar el script para descargar el modelo
RUN python download_model.py

# --- ETAPA 2: Final - Construir la imagen de la aplicación ---
FROM python:3.10-slim

# Establecer el directorio de trabajo final
WORKDIR /code

# Copiar las librerías YA INSTALADAS desde la etapa 'builder'
COPY --from=builder /builder/wheels /usr/local/lib/python3.10/site-packages

# Copiar el modelo pre-descargado desde la etapa 'builder'
COPY --from=builder /builder/model ./model

# Copiar el código de nuestra aplicación
COPY ./app ./app

# Exponer el puerto
EXPOSE 8000

# Comando para iniciar la API
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]