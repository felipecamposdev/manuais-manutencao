import streamlit as st
from google import genai
import time

st.set_page_config(page_title="Manual Interativo", page_icon="⚙️", layout="centered")
st.title("🤖 Assistente de Manutenção")

# Conecta a IA usando o novo formato oficial de cliente
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def load_pdf_to_gemini():
    # Envia o arquivo manual.pdf que está no GitHub
    file_path = "manual.pdf"
    uploaded_pdf = client.files.upload(file=file_path)
    
    # Aguarda o processamento
    while uploaded_pdf.state.name == "PROCESSING":
        time.sleep(2)
        uploaded_pdf = client.files.get(name=uploaded_pdf.name)
    return uploaded_pdf

try:
    with st.spinner("Iniciando sistemas e lendo o manual..."):
        pdf_file_uri = load_pdf_to_gemini()
    st.success("Sistema pronto! Digite o código de falha ou procedimento abaixo.")
except Exception as e:
    st.error(f"Erro do sistema: {e}")
    st.stop()

# Exibe o histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de pergunta
if prompt := st.chat_input("Ex: Como resolver a falha E-04?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando no manual..."):
            # Faz a pergunta usando o novo formato do SDK
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[pdf_file_uri, prompt],
                config={
                    "system_instruction": "Você é um assistente técnico especialista. Responda APENAS com base no PDF. Se não estiver no manual, diga que não sabe. Destaque alertas de segurança.",
                }
            )
            st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})
