import streamlit as st
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="Ordem de Serviço - Manutenção", page_icon="🛠️", layout="centered")

st.title("🛠️ Abertura de Ordem de Serviço")
st.write("Preencha os dados abaixo para relatar o problema na máquina.")

# Criando o formulário profissional
with st.form("form_os"):
    maquina = st.selectbox("Selecione a Máquina", ["Torno CNC 01", "Injetora 04", "Esteira de Embalagem"])
    tipo_problema = st.selectbox("Tipo de Ocorrência", ["Falha Elétrica", "Problema Mecânico", "Parada de Emergência", "Outros"])
    descricao = st.text_area("Descrição detalhada do problema")
    
    # Campo para anexar foto (o celular do técnico vai dar a opção de tirar a foto na hora ou escolher da galeria)
    foto_anexada = st.file_uploader("Anexar foto da falha (Opcional)", type=["jpg", "png", "jpeg"])
    
    # Botão de envio
    enviar = st.form_submit_button("Enviar Ordem de Serviço")

if enviar:
    if not descricao:
        st.warning("Por favor, preencha a descrição do problema antes de enviar.")
    else:
        with st.spinner("Enviando chamado para a manutenção..."):
            try:
                # Configuração do E-mail (Exemplo usando Gmail)
                # Dica: No Gmail, utilize uma "Senha de App" (App Password) nas configurações de segurança da sua conta
                email_remetente = "atendimento@automacel.com"
                senha_app = "Cofat1234@"
                email_destino = "felipe.campos@cofat.com"
                
                msg = EmailMessage()
                msg['Subject'] = f"🚨 Nova OS: {maquina} - {tipo_problema}"
                msg['From'] = email_remetente
                msg['To'] = email_destino
                
                corpo_email = f"""
                Foi aberta uma nova Ordem de Serviço via QR Code:
                
                - Máquina: {maquina}
                - Tipo de Ocorrência: {tipo_problema}
                - Descrição: {descricao}
                """
                msg.set_content(corpo_email)
                
                # Se o usuário anexou uma foto, adicionamos ela no e-mail
                if foto_anexada is not None:
                    dados_foto = foto_anexada.getvalue()
                    nome_arquivo = foto_anexada.name
                    msg.add_attachment(dados_foto, maintype='image', subtype='jpeg', filename=nome_arquivo)
                
                # Conecta no servidor SMTP do e-mail e envia
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(email_remetente, senha_app)
                    smtp.send_message(msg)
                
                st.success("✅ Ordem de Serviço enviada com sucesso para a equipe de manutenção!")
                
            except Exception as e:
                st.error(f"Erro ao enviar o e-mail: {e}")
