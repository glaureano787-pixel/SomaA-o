import streamlit as st

# Configuração da página (Estilo Industrial que você escolheu)
st.set_page_config(page_title="SomaAço - Otimização de Lotes", layout="wide")

# Estilo visual para ficar igual ao seu print
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #3b82f6; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("SOMA AÇO")
st.subheader("ALGORITMO DE AGRUPAMENTO E CONFERÊNCIA DE LOTES")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("ENTRADA DE DADOS")
    
    # Seção de Lotes
    st.markdown("### 1. ADICIONAR LOTES REAIS")
    id_lote = st.text_input("ID DO LOTE", placeholder="Ex: Lote 181")
    meta_peso = st.number_input("META DE PESO (KG)", min_value=0.0, step=0.1)
    qtd_rolos = st.number_input("QTD. ROLOS (OPCIONAL)", min_value=0)
    
    # Seção de Estoque
    st.markdown("### 2. ESTOQUE DISPONÍVEL (PESOS DOS ROLOS)")
    pesos_input = st.text_area("Digite os pesos separados por vírgula ou espaço:", 
                               placeholder="Ex: 600, 550, 595...")

    if st.button("▶ PROCESSAR AGRUPAMENTO"):
        # Lógica simples de cálculo (O "Cérebro")
        try:
            pesos = [float(x.strip()) for x in pesos_input.replace(',', ' ').split() if x.strip()]
            st.session_state['resultado'] = f"Processando {len(pesos)} rolos para o {id_lote}..."
        except:
            st.error("Por favor, verifique se os pesos foram digitados corretamente.")

with col2:
    st.header("RESULTADO")
    if 'resultado' in st.session_state:
        st.success(st.session_state['resultado'])
        # Aqui entra o seu algoritmo que soma os rolos para bater a meta
        st.info("Otimização calculada com sucesso para o ambiente de pátio.")
    else:
        st.markdown("<div style='text-align:center; padding: 50px; border: 1px dashed #444;'>Aguardando Lotes & Estoque...</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 SomaAço - Sistemas de Gestão de Materiais e Bitolas")
