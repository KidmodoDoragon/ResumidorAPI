# Dockerfile

# --- ETAPA 1: Builder - Descargar y guardar el modelo ---
# Usamos una imagen base de Python para esta tarea
FROM python:3.10-slim as builder

# Establecer el directorio de trabajo
WORKDIR /builder

# Instalar las dependencias necesarias SOLO para descargar el modelo
# --no-cache-dir reduce el tamaño de la capa
RUN pip install --no-cache-dir torch transformers sentencepiece

# Copiar el script de descarga
COPY download_model.py .

# Ejecutar el script. Esto creará una carpeta 'model' con los archivos descargados.
RUN python download_model.py

# --- ETAPA 2: Final - Construir la imagen de la aplicación ---
# Empezamos desde una imagen base limpia y ligera
FROM python:3.10-slim

# Establecer el directorio de trabajo final
WORKDIR /code

# Copiar el archivo de requerimientos primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instalar las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt
# Copiar el modelo pre-descargado desde la etapa 'builder' a la imagen final
# Esto es clave: la carpeta 'model' ahora existe dentro de nuestra imagen
COPY --from=builder /builder/model ./model

# Copiar el código de nuestra aplicación (la carpeta 'app')
COPY ./app ./app

# Exponer el puerto en el que se ejecutará la API
EXPOSE 8000

# Comando para iniciar el servidor de la API cuando el contenedor se ejecute
# uvicorn app.api:app -> Ejecuta el objeto 'app' que está en el archivo 'app/api.py'
# --host 0.0.0.0 -> Permite que la API sea accesible desde fuera del contenedor
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]