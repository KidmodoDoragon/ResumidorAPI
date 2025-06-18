# app/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from . import summarizer # Importamos nuestro módulo de resumen

# Modelo de datos para el cuerpo de la petición POST con Pydantic
class TextInput(BaseModel):
    text: str
    
class SummaryResponse(BaseModel):
    summary: str

# Crear la instancia de la aplicación FastAPI
app = FastAPI(
    title="API de Resumen de Texto",
    description="Una API para generar resúmenes de texto usando el modelo T5.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    """
    Esta función se ejecuta cuando la aplicación se inicia.
    Carga el modelo de ML en memoria.
    """
    print("--- Iniciando aplicación y cargando modelo ---")
    summarizer.load_model()
    print("--- Modelo cargado. La API está lista. ---")


@app.post("/summarize/", response_model=SummaryResponse)
def create_summary(item: TextInput):
    """
    Endpoint para generar un resumen.
    Recibe un JSON con una clave "text" y devuelve un JSON con la clave "summary".
    """
    if not item.text or not item.text.strip():
        raise HTTPException(status_code=400, detail="El campo 'text' no puede estar vacío.")
    
    try:
        summary_text = summarizer.summarize(item.text)
        return {"summary": summary_text}
    except Exception as e:
        # En un entorno de producción, registrarías este error
        print(f"Error al generar el resumen: {e}")
        raise HTTPException(status_code=500, detail="Ocurrió un error interno en el servidor.")