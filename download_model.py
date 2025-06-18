# download_model.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

MODEL_ID = "google/mt5-base"
MODEL_PATH = "model"

if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

print(f"Descargando y guardando el modelo '{MODEL_ID}' en la carpeta '{MODEL_PATH}'...")

# Descargar y guardar el tokenizador
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.save_pretrained(MODEL_PATH)

# Descargar y guardar el modelo
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
model.save_pretrained(MODEL_PATH)

print("Modelo y tokenizador guardados exitosamente.")
