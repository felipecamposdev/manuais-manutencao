import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Manual Interativo", page_icon="⚙️", layout="centered")
st.title("🤖 Assistente de Manutenção")

# Puxa a chave de segurança do servidor
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# O truque do Cache: O servidor lê o PDF apenas uma vez e deixa na memória para todos os técnicos
@st.cache_resource
def load_pdf_to_gemini():
    # O nome do arquivo deve ser exatamente o mesmo que você subiu no GitHub
    file_path = "manual.pdf"
    uploaded_pdf = genai.upload_file(path=file_path, display_name="Manual_Em_Cache")
    
    while uploaded_pdf.state.name == "PROCESSING":
        time.sleep(2)
        uploaded_pdf = genai.get_file(uploaded_pdf.name)
    return uploaded_pdf

try:
    with st.spinner("Iniciando sistemas e carregando manual da máquina..."):
        pdf_file_uri = load_pdf_to_gemini()
    st.success("Sistema pronto! Digite o código de falha ou procedimento abaixo.")
except Exception as e:
    st.error(f"Erro: Não encontrei o arquivo 'manual.pdf' no servidor. Verifique o GitHub.")
    st.stop()

# Exibe o histórico do chat na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de pergunta do técnico
if prompt := st.chat_input("Ex: Como resolver a falha E-04?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    system_instruction = """
    Você é um assistente técnico especialista em manutenção industrial.
    Responda as dúvidas baseando-se EXCLUSIVAMENTE no documento PDF fornecido. 
    Se a informação não estiver no manual, diga que não consta no documento. 
    Mencione sempre os avisos de segurança pertinentes.
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )

    with st.chat_message("assistant"):
        with st.spinner("Buscando no manual..."):
            response = model.generate_content([pdf_file_uri, prompt])
            st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})
