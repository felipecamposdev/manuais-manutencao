import streamlit as st
from google import genai
import time

st.set_page_config(page_title="Manual Interativo", page_icon="⚙️", layout="centered")
st.title("🤖 Assistente de Manutenção")

# Conecta a IA
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def load_pdf_to_gemini():
    file_path = "manual.pdf"
    uploaded_pdf = client.files.upload(file=file_path)
    
    # Aguarda o processamento do Google
    while uploaded_pdf.state.name == "PROCESSING":
        time.sleep(2)
        uploaded_pdf = client.files.get(name=uploaded_pdf.name)
    return uploaded_pdf

try:
    with st.spinner("Iniciando sistemas e lendo o manual..."):
        arquivo_pdf = load_pdf_to_gemini()
    st.success("Sistema pronto! Digite o código de falha ou procedimento abaixo.")
except Exception as e:
    st.error(f"Erro ao carregar PDF: {e}")
    st.stop()

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de pergunta do técnico
if prompt := st.chat_input("Ex: Como resolver a falha E-04?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando no manual..."):
            
            # TRUQUE: Incorporamos a regra de comportamento direto no texto
            prompt_seguro = f"""Você é um assistente técnico especialista em manutenção industrial. 
Responda à dúvida do técnico baseando-se EXCLUSIVAMENTE no documento PDF fornecido. 
Se a informação não estiver no manual, diga exatamente: 'Essa informação não consta no manual.' 
Sempre destaque os alertas de segurança.

Dúvida do técnico: {prompt}"""

            try:
                # Chamada enxuta e direta, sem dicionários de configuração que causam bugs
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[arquivo_pdf, prompt_seguro]
                )
                st.markdown(response.text)
                
                # Salva apenas a resposta final no histórico
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as erro_ia:
                # Se a IA recusar, mostra o erro no chat de forma amigável
                st.error(f"Ocorreu um erro de comunicação com a IA: {erro_ia}")
