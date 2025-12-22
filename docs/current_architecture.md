# Arquitectura Actual: Fiscalía AI (MVP)

Este documento describe la arquitectura técnica actual de la versión MVP de "Fiscalía AI".

## Diagrama de Arquitectura

```mermaid
graph TD
    User[Usuario (Fiscal/Asistente)] -->|Sube Archivos| UI[Interfaz Streamlit]
    User -->|Busca Casos| UI
    
    subgraph "Frontend & Control"
        UI -->|Procesa Archivo| Ingestor[Módulo de Ingesta]
        UI -->|Consulta| DB[(SQLite Database)]
    end
    
    subgraph "Procesamiento de Archivos"
        Ingestor -->|Audio| Whisper[OpenAI Whisper API]
        Ingestor -->|Imagen/PDF Escaneado| OCR[Tesseract OCR]
        Ingestor -->|PDF/Docx Texto| Extract[Extractores de Texto]
    end
    
    subgraph "Inteligencia Artificial"
        Whisper -->|Texto Transcrito| Analyzer[Módulo Analizador]
        OCR -->|Texto Extraído| Analyzer
        Extract -->|Texto Extraído| Analyzer
        
        Analyzer -->|Prompt + Texto| GPT[OpenAI GPT-4o-mini]
        GPT -->|JSON: Resumen, Keywords, Categoría| Analyzer
    end
    
    Analyzer -->|Datos Estructurados| UI
    UI -->|Guarda| DB
```

## Componentes

### 1. Interfaz de Usuario (Streamlit)
- **Función:** Punto de entrada para el usuario. Maneja la carga de archivos y la visualización de resultados.
- **Tecnología:** Streamlit (Python).

### 2. Módulo de Ingesta (`ingestor.py`)
- **Función:** Normaliza la entrada de datos. Detecta el tipo de archivo y decide qué herramienta usar para extraer el texto.
- **Soporte:**
    - **Audio:** Usa `transcriber.py` (Whisper).
    - **Imágenes:** Usa `pytesseract` (OCR local).
    - **Documentos:** Usa `pypdf` y `python-docx`.

### 3. Módulo Analizador (`analyzer.py`)
- **Función:** Cerebro del sistema. Toma el texto crudo y lo enriquece.
- **Lógica:** Envía el texto a GPT-4o-mini con un prompt específico para:
    - Resumir el caso.
    - Extraer entidades clave.
    - Clasificar el delito (Categorización).

### 4. Base de Datos (`database.py`)
- **Función:** Persistencia de datos local.
- **Tecnología:** SQLite (archivo `judicial_voice.db`).
- **Esquema:** Tabla única `denuncias` con campos para metadatos, contenido original y análisis generado.

## Flujo de Datos
1.  El usuario carga un archivo (ej. `denuncia.mp3`).
2.  El **Ingestor** detecta que es audio y llama a la API de Whisper.
3.  Whisper devuelve el texto transcrito.
4.  El **Analizador** toma el texto y lo envía a GPT-4o.
5.  GPT-4o devuelve un JSON con: `{ "resumen": "...", "keywords": [...], "category": "Robo" }`.
6.  La **UI** muestra los resultados y guarda todo en **SQLite**.
