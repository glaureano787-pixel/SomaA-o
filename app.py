import streamlit as st
import pandas as pd

# Configuração da página para o estilo "Wide" e Dark
st.set_page_config(page_title="SomaAço - Gestão Industrial", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILO CSS PERSONALIZADO (IDÊNTICO AO IDX) ---
st.markdown("""
    <style>
    /* Fundo e Cores Globais */
    .stApp { background-color: #0f172a; color: #f8fafc; }
    
    /* Header Estilo IDX */
    .custom-header {
        background-color: #1e293b;
        padding: 1rem;
        border-bottom: 1px solid #334155;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Cards de Interface */
    .section-card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Botões Customizados */
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #2563eb; border: none; color: white; }
    
    /* Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #334155 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE ESTADO (HISTÓRICO) ---
if 'historico' not in st.session_state:
    st.session_state.historico = []

def adicionar_ao_historico(id_lote, meta, pesos):
    # Lógica de exclusão automática (mantém apenas 6)
    if len(st.session_state.historico) >= 6:
        st.session_state.historico.pop(0)
    
    novo_registro = {
        "id": id_lote,
        "meta": meta,
        "pesos": pesos,
        "data": pd.Timestamp.now().strftime("%H:%M:%S")
    }
    st.session_state.historico.append(novo_registro)

# --- INTERFACE ---
# Cabeçalho Superior
st.markdown("""
    <div class="custom-header">
        <div style="display: flex; align-items: center;">
            <div style="background-color:#3b82f6; padding:8px; border-radius:50%; margin-right:15px;">🔘</div>
            <div>
                <h2 style="margin:0; font-size:1.2rem;">SOMA AÇO</h2>
                <p style="margin:0; font-size:0.7rem; color:#94a3b8;">ALGORITMO DE AGRUPAMENTO E CONFERÊNCIA DE LOTES</p>
            </div>
        </div>
        <div style="color:#64748b; font-size:0.8rem;">Industrial v1.0</div>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📋 Configuração", "🕒 Histórico"])

with tab1:
    col_input, col_result = st.columns([1, 1.2])
    
    with col_input:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📦 ENTRADA DE DADOS")
        
        # O Streamlit já pula de campo naturalmente ao apertar Enter/Tab
        lote_id = st.text_input("IDENTIFICAÇÃO DO LOTE", placeholder="Ex: Lote 181")
        meta = st.number_input("META DE PESO (KG)", min_value=0.0, step=0.1)
        qtd_rolos = st.number_input("QTD. ROLOS (OPCIONAL)", min_value=0)
        
        st.markdown("---")
        pesos_raw = st.text_area("PESOS DOS ROLOS (Separe por espaço ou vírgula)", placeholder="600, 550, 595...")
        
        if st.button("▶ PROCESSAR AGRUPAMENTO"):
            if lote_id and meta > 0:
                adicionar_ao_historico(lote_id, meta, pesos_raw)
                st.success(f"Lote {lote_id} processado!")
            else:
                st.warning("Preencha o ID do Lote e a Meta de Peso.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        st.markdown('<div class="section-card" style="min-height: 450px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">', unsafe_allow_html=True)
        if not st.session_state.historico:
            st.markdown("""
                <div style="opacity: 0.3; font-size: 3rem;">📄</div>
                <h3>Aguardando Lotes & Estoque</h3>
                <p style="color:#64748b;">Cadastre as metas e o estoque de rolos disponível.</p>
            """, unsafe_allow_html=True)
        else:
            ultimo = st.session_state.historico[-1]
            st.markdown(f"### Resultado: {ultimo['id']}")
            st.write(f"Meta: {ultimo['meta']} kg")
            st.info("Algoritmo calculando melhor combinação de rolos...")
            # Aqui você pode inserir sua lógica matemática de soma de rolos
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("HISTÓRICO DE RELATÓRIOS")
    if not st.session_state.historico:
        st.write("Nenhum processamento recente encontrado.")
    else:
        for i, registro in enumerate(reversed(st.session_state.historico)):
            col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
            with col_h1:
                st.write(f"**Lote:** {registro['id']} | **Meta:** {registro['meta']}kg")
            with col_h2:
                st.caption(f"Hora: {registro['data']}")
            with col_h3:
                if st.button(f"Excluir", key=f"del_{i}"):
                    # Lógica de exclusão individual
                    st.session_state.historico.pop(-(i+1))
                    st.rerun()
            st.markdown("---")

# Rodapé
st.markdown(f"<p style='text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 50px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
