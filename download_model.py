# download_model.py
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Lee el token desde los secrets de GitHub Actions
HUGGING_FACE_TOKEN = os.getenv("HF_TOKEN")

MODEL_NAME = "google/mt5-base"
SAVE_DIRECTORY = "./model"

print(f"--- Descargando modelo: {MODEL_NAME} ---")

# Descargar y guardar el tokenizador
# Usamos el token para autenticarnos
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME, 
    token=HUGGING_FACE_TOKEN
)
tokenizer.save_pretrained(SAVE_DIRECTORY)

# Descargar y guardar el modelo
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME, 
    token=HUGGING_FACE_TOKEN
)
model.save_pretrained(SAVE_DIRECTORY)

print(f"--- Modelo y tokenizador guardados en {SAVE_DIRECTORY} ---")