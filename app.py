# ============================
# Cronos IA Image - App Web
# ============================

# --------- IMPORTAÇÕES ---------
import streamlit as st
import speech_recognition as sr
import base64
import requests
import io
from PIL import Image

# --------- INSTRUÇÕES DE INSTALAÇÃO ---------
# pip install streamlit speechrecognition pillow requests

# --------- CONFIGURAÇÃO DA PÁGINA ---------
st.set_page_config(page_title="Cronos IA Image", layout="centered")
st.title("Cronos IA Image")
st.subheader("Gere imagens com o poder da IA a partir de texto ou voz")

# --------- INSIRA SUA API KEY AQUI ---------
API_KEY = ""  # Substitua pela sua chave da API Google Gemini (Vertex ou Generative AI Studio)
MODEL_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagegenerator:generateImage?key=" + API_KEY

# --------- FUNÇÕES AUXILIARES ---------
def reconhecer_fala():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Fale agora...")
        try:
            audio = recognizer.listen(source, timeout=5)
            texto = recognizer.recognize_google(audio, language="pt-BR")
            st.success("Texto reconhecido: " + texto)
            return texto
        except sr.UnknownValueError:
            st.warning("Não foi possível entender o áudio.")
        except sr.RequestError:
            st.error("Erro ao conectar com o serviço de reconhecimento de voz.")
        except sr.WaitTimeoutError:
            st.warning("Tempo de gravação esgotado.")
    return None

def gerar_imagem(prompt):
    if not API_KEY:
        st.error("API Key ausente. Por favor, configure sua chave da API Google Gemini.")
        return None

    headers = {"Content-Type": "application/json"}
    data = {"prompt": {"text": prompt}}

    response = requests.post(MODEL_URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            image_base64 = response.json()['candidates'][0]['content']['parts'][0]['inlineData']['data']
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_bytes))
            return image
        except Exception as e:
            st.error(f"Erro ao processar a imagem: {e}")
    else:
        st.error(f"Erro na API ({response.status_code}): {response.text}")
    return None

# --------- CONSTRUÇÃO DA INTERFACE ---------
st.markdown("---")
texto_input = st.text_area("Digite uma descrição para a imagem:")

col1, col2 = st.columns([1, 1])
with col1:
    gravar = st.button("🎤 Gravar Voz")
with col2:
    gerar = st.button(":art: Gerar Imagem")

# Reconhecimento de voz
if gravar:
    texto_reconhecido = reconhecer_fala()
    if texto_reconhecido:
        texto_input = texto_reconhecido
        st.session_state['texto'] = texto_input

# Atualiza campo de texto com reconhecimento de voz
if 'texto' in st.session_state:
    st.text_area("Texto reconhecido:", st.session_state['texto'], disabled=True)

# Gera imagem a partir do prompt
if gerar:
    prompt_final = texto_input.strip() or st.session_state.get('texto', '').strip()
    if not prompt_final:
        st.warning("Por favor, insira um texto manualmente ou por voz.")
    else:
        with st.spinner("Gerando imagem..."):
            imagem = gerar_imagem(prompt_final)
            if imagem:
                st.image(imagem, caption="Imagem gerada com IA", use_column_width=True)

# --------- NOTA FINAL ---------
st.markdown("---")
st.caption("Desenvolvido por Cronos AI - Sugerido também: Cronos Vision ou Cronos Imaginador")
