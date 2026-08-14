import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

st.set_page_config(page_title="Manual Interativo", page_icon="⚙️", layout="centered")
st.title("🤖 Assistente de Manutenção")

# Puxa a chave de segurança do servidor
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_file_uri" not in st.session_state:
    st.session_state.pdf_file_uri = None

uploaded_file = st.file_uploader("Engenharia: Carregue o Manual em PDF", type=["pdf"])

if uploaded_file is not None and st.session_state.pdf_file_uri is None:
    with st.spinner("Processando e lendo o manual..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        
        uploaded_pdf = genai.upload_file(path=tmp_file_path, display_name="Manual_Maquina")
        
        while uploaded_pdf.state.name == "PROCESSING":
            time.sleep(2)
            uploaded_pdf = genai.get_file(uploaded_pdf.name)
            
        st.session_state.pdf_file_uri = uploaded_pdf
        os.remove(tmp_file_path)
        st.success("Manual carregado! A IA já estudou o documento.")

if st.session_state.pdf_file_uri:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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
                response = model.generate_content([st.session_state.pdf_file_uri, prompt])
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
