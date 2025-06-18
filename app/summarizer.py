import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# La ruta donde el Dockerfile copiará el modelo descargado
MODEL_PATH = "./model"

# Variables globales para mantener el modelo cargado en memoria
_model = None
_tokenizer = None
_device = None

def load_model():
    """Carga el tokenizador y el modelo en memoria desde la carpeta local."""
    global _model, _tokenizer, _device

    # Cargar solo si no ha sido cargado previamente
    if _model is None:
        print(f"[+] Cargando modelo desde la ruta local: {MODEL_PATH}")
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
        _model.to(_device)
        
        print(f"[✓] Modelo cargado en el dispositivo: {_device}")

def summarize(texto: str) -> str:
    """
    Genera un resumen del texto usando el modelo cargado.
    """
    if _model is None or _tokenizer is None:
        raise RuntimeError("El modelo no ha sido cargado. Ejecuta load_model() primero.")

    # Preparar el texto para el modelo
    inputs = _tokenizer(
        texto,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=1024
    ).to(_device)
    # Generar el resumen
    resumen_ids = _model.generate(
        inputs["input_ids"],
        num_beams=4,
        no_repeat_ngram_size=3,
        length_penalty=2.0,
        early_stopping=True,
        min_length=30,  # Reducido para resúmenes más flexibles
        max_length=200
    )

    # Decodificar el resultado
    resumen = _tokenizer.decode(
        resumen_ids[0], 
        skip_special_tokens=True, 
        clean_up_tokenization_spaces=True
    )
    
    return resumen