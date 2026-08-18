import streamlit as st
import urllib.parse

st.set_page_config(page_title="Ordem de Serviço - WhatsApp", page_icon="📱", layout="centered")

st.title("🛠️ Abertura de Ordem de Serviço")
st.write("Preencha os dados abaixo e envie o chamado direto para a equipe técnica.")

with st.form("form_whatsapp"):
    # Campos do formulário
    maquina = st.selectbox("Selecione a Máquina / Equipamento", ["Torno CNC 01", "Injetora 04", "Esteira de Embalagem", "Robô de Solda"])
    tipo_problema = st.selectbox("Tipo de Ocorrência", ["Falha Elétrica", "Problema Mecânico", "Parada de Emergência", "Outros"])
    descricao = st.text_area("Descreva o que aconteceu:")
    
    # Botão de envio
    enviar = st.form_submit_button("Gerar Chamado para o WhatsApp")

if enviar:
    if not descricao:
        st.warning("Por favor, preencha a descrição do problema.")
    else:
        # Número de WhatsApp que vai receber o chamado (coloque o DDD e o número, apenas números)
        # Exemplo para Brasil: 55 + DDD + Número (ex: 5511999999999)
        numero_whatsapp = "5511970816834" 
        
        # Formata o texto que irá na mensagem
        texto_mensagem = f"""*🚨 NOVA ORDEM DE SERVIÇO (QR CODE)*
* *Máquina:* {maquina}
* *Tipo:* {tipo_problema}
* *Descrição:* {descricao}"""
        
        # Codifica o texto para o formato de link da Web/Celular
        texto_codificado = urllib.parse.quote(texto_mensagem)
        link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={texto_codificado}"
        
        st.success("✅ Chamado processado com sucesso!")
        st.markdown("### Clique no botão abaixo para enviar para a manutenção:")
        
        # Botão link estilizado que abre o WhatsApp do usuário
        st.link_button("📲 Enviar Mensagem no WhatsApp", link_whatsapp)
