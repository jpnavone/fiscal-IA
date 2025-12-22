# Arquitectura Futura: Fiscalía AI (Fase 2 - RAG)

Este documento describe la evolución hacia un sistema **RAG (Retrieval Augmented Generation)** completo.

## Diagrama de Arquitectura (RAG)

```mermaid
graph TD
    subgraph "Ingesta & Indexación (Offline)"
        Docs[Documentos PDF/Word/Audio] -->|1. Carga| Loader[LangChain Loaders]
        Loader -->|2. Texto Crudo| Splitter[Text Splitter]
        Splitter -->|3. Chunks (Fragmentos)| Embedder[OpenAI Embeddings]
        Embedder -->|4. Vectores| VectorDB[(ChromaDB / Pinecone)]
    end

    subgraph "Consulta & Respuesta (Online)"
        User[Usuario] -->|5. Pregunta| Chain[LangChain Retrieval Chain]
        Chain -->|6. Embed Pregunta| Embedder
        Embedder -->|7. Búsqueda Semántica| VectorDB
        VectorDB -->|8. Chunks Relevantes| Chain
        Chain -->|9. Contexto + Pregunta| LLM[GPT-4o]
        LLM -->|10. Respuesta con Fuentes| User
    end
```

## ¿Por qué LangChain?

LangChain actúa como el "pegamento" u orquestador de toda la arquitectura. Sus principales ventajas sobre la implementación manual son:

1.  **Abstracción de Modelos:** Permite cambiar de OpenAI a Anthropic, Llama 3 (local) o Azure con una sola línea de código.
2.  **Manejo de Memoria:** Gestiona automáticamente el historial del chat, permitiendo que el usuario haga preguntas de seguimiento ("¿Y quién es él?" refiriéndose a la respuesta anterior).
3.  **Splitters Inteligentes:** Cortar texto no es trivial. LangChain tiene algoritmos optimizados para cortar por párrafos, markdown o código, evitando romper frases a la mitad.
4.  **Retrievers Avanzados:** Implementa técnicas de búsqueda complejas como *Self-Querying* (la IA filtra metadatos antes de buscar) o *Parent Document Retrieval* (buscar chunks pequeños pero devolver el contexto grande).

## Componentes Clave

### A. Base de Datos Vectorial (Vector Store)
- **Tecnología:** ChromaDB (Local) o Pinecone (Nube).
- **Función:** Almacena los significados semánticos. Permite encontrar "violencia" aunque la búsqueda sea "agresión física".

### B. Pipeline de Ingesta
- **OCR:** Tesseract/Azure para digitalizar expedientes viejos.
- **Chunking:** División estratégica de documentos largos (ej. 1500 páginas) en piezas procesables.

### C. Generación (LLM)
- **Modelo:** GPT-4o (o modelos locales finetuneados para leyes chilenas).
- **Prompting:** Inyección dinámica de contexto legal y reglas de respuesta.
