import streamlit as st
import os
import tempfile
from modules.database import init_db, save_denuncia, search_denuncias, get_all_denuncias
from modules.ingestor import extract_text_from_file
from modules.analyzer import analyze_text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Fiscalía AI",
    page_icon="⚖️",
    layout="wide"
)

# Initialize DB
init_db()

# Title
st.title("⚖️ Fiscalía AI")
st.markdown("Sistema Inteligente de Gestión de Evidencia Judicial.")

# Check API Key
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ No se encontró la API Key de OpenAI. Por favor configura el archivo .env")
    st.stop()

# Tabs
tab1, tab2 = st.tabs(["📂 Ingesta de Evidencia", "🔍 Búsqueda Inteligente"])

with tab1:
    st.header("Subir Evidencia")
    st.markdown("Soporta: Audio (mp3, wav), Documentos (pdf, docx) e Imágenes (jpg, png).")
    
    uploaded_files = st.file_uploader(
        "Arrastra tus archivos aquí", 
        type=['mp3', 'wav', 'm4a', 'ogg', 'pdf', 'docx', 'jpg', 'jpeg', 'png'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Procesar Archivos", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Procesando {uploaded_file.name}...")
                try:
                    # Determine file type
                    file_ext = uploaded_file.name.split('.')[-1].lower()
                    if file_ext in ['mp3', 'wav', 'm4a', 'ogg']:
                        file_type = 'audio'
                    elif file_ext == 'pdf':
                        file_type = 'pdf'
                    elif file_ext == 'docx':
                        file_type = 'docx'
                    elif file_ext in ['jpg', 'jpeg', 'png']:
                        file_type = 'image'
                    else:
                        file_type = 'unknown'

                    # Save temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # 1. Extract Text
                    text_content = extract_text_from_file(tmp_path, file_ext if file_type != 'audio' else file_ext)
                    
                    if text_content and "Error" not in text_content[:20]:
                        # 2. Analyze
                        analysis = analyze_text(text_content)
                        keywords = analysis.get("keywords", [])
                        summary = analysis.get("summary", "")
                        category = analysis.get("category", "Otros")
                        
                        # 3. Save
                        save_denuncia(
                            filename=uploaded_file.name,
                            transcript=text_content,
                            keywords=keywords,
                            summary=summary,
                            category=category,
                            file_type=file_type
                        )
                        st.success(f"✅ {uploaded_file.name} procesado correctamente ({category}).")
                    else:
                        st.error(f"❌ Falló el procesamiento de {uploaded_file.name}: {text_content}")
                        
                    # Cleanup
                    os.unlink(tmp_path)
                    
                except Exception as e:
                    st.error(f"Error en {uploaded_file.name}: {e}")
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("¡Procesamiento completado!")

with tab2:
    st.header("Buscador de Casos")
    
    search_query = st.text_input("Buscar por palabra clave, persona o hecho...", placeholder="Ej: robo armado, Juan Perez, contrato")
    
    if search_query:
        results = search_denuncias(search_query)
        if results:
            st.success(f"Se encontraron {len(results)} resultados.")
            for item in results:
                with st.container():
                    icon = "📄"
                    if item.file_type == 'audio': icon = "🎙️"
                    elif item.file_type == 'image': icon = "🖼️"
                    
                    st.markdown(f"### {icon} {item.category} - {item.filename}")
                    st.caption(f"ID: {item.id} | Fecha: {item.timestamp}")
                    st.markdown(f"**Resumen:** {item.summary}")
                    st.markdown(f"**Keywords:** `{item.keywords}`")
                    with st.expander("Ver Contenido Completo"):
                        st.write(item.transcript)
                    st.divider()
        else:
            st.warning("No se encontraron resultados.")
    else:
        # Show recent
        st.subheader("Ingresos Recientes")
        recent = get_all_denuncias()
        if recent:
            for item in recent[:5]:
                icon = "📄"
                if item.file_type == 'audio': icon = "🎙️"
                elif item.file_type == 'image': icon = "🖼️"
                
                with st.expander(f"{icon} {item.timestamp.strftime('%Y-%m-%d %H:%M')} - {item.filename} ({item.category})"):
                    st.markdown(f"**Resumen:**")
                    st.write(item.summary)
                    st.markdown(f"**Keywords:**")
                    st.info(f"{item.keywords}")
                    st.markdown("**Transcripción:**")
                    st.text_area("Contenido", item.transcript, height=150, key=f"trans_{item.id}")
        else:
            st.info("Aún no hay evidencia cargada.")
