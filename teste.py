import streamlit as st
import urllib.parse

st.set_page_config(page_title="Ordem de Serviço - WhatsApp", page_icon="📱", layout="centered")

st.title("🛠️ Abertura de Ordem de Serviço")
st.write("Preencha os dados e anexe a foto da falha.")

with st.form("form_whats_foto"):
    maquina = st.selectbox("Selecione a Máquina", ["Torno CNC 01", "Injetora 04", "Esteira de Embalagem"])
    tipo_problema = st.selectbox("Tipo de Ocorrência", ["Falha Elétrica", "Problema Mecânico", "Parada de Emergência"])
    descricao = st.text_area("Descreva o que aconteceu:")
    
    # O operador já pode tirar a foto direto pelo celular aqui
    foto_falha = st.file_uploader("Tirar ou anexar foto da falha", type=["jpg", "png", "jpeg"])
    
    enviar = st.form_submit_button("Gerar Chamado para o WhatsApp")

if enviar:
    if not descricao:
        st.warning("Por favor, preencha a descrição do problema.")
    else:
        numero_whatsapp = "5511999999999"  # Altere para o número da manutenção
        
        texto_mensagem = f"""*🚨 NOVA ORDEM DE SERVIÇO (QR CODE)*
* *Máquina:* {maquina}
* *Tipo:* {tipo_problema}
* *Descrição:* {descricao}"""
        
        texto_codificado = urllib.parse.quote(texto_mensagem)
        link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={texto_codificado}"
        
        st.success("✅ Chamado gerado com sucesso!")
        
        # Se ele enviou uma foto no Streamlit, podemos avisá-lo para mandá-la junto no chat
        if foto_falha is not None:
            st.info("💡 **Dica:** Como você anexou uma foto acima, salve-a ou tire um print rápido se necessário, e envie junto na conversa do WhatsApp que vai abrir!")
            # Mostra a miniatura da foto para o operador conferir
            st.image(foto_falha, caption="Foto capturada para envio", width=250)
            
        st.markdown("### Clique abaixo para abrir o WhatsApp:")
        st.link_button("📲 Enviar Mensagem para a Manutenção", link_whatsapp)
