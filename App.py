import streamlit as st
import whisper
import os
import tempfile

st.title("🎙️ Transcritor de Vídeo com Whisper")
st.write("Faça upload de um vídeo e obtenha a transcrição automaticamente.")

# Upload do arquivo via navegador
uploaded_file = st.file_uploader("Escolha um arquivo de vídeo", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    # Salvar o arquivo temporariamente para processar
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.video(uploaded_file)
    
    if st.button("🚀 Iniciar Transcrição"):
        with st.spinner('Carregando modelo Whisper (pode demorar um pouco)...'):
            # Carrega o modelo (cacheado para não baixar toda vez)
            @st.cache_resource
            def load_model():
                return whisper.load_model("base") # Use 'base' ou 'small' para ser mais rápido na nuvem
            
            model = load_model()

        with st.spinner('Transcrevendo... Isso depende do tamanho do vídeo.'):
            result = model.transcribe(video_path)
            transcription = result["text"]
            
            st.success("Concluído!")
            st.subheader("Texto Transcrito:")
            st.write(transcription)

            # Botão para baixar o texto
            st.download_button(
                label="💾 Baixar Transcrição (.txt)",
                data=transcription,
                file_name="transcricao.txt",
                mime="text/plain"
            )
    
    # Limpeza do arquivo temporário
    tfile.close()
  
