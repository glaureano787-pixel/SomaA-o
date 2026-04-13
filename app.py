import streamlit as st
import pandas as pd

# Configuração Master
st.set_page_config(page_title="SomaAço", layout="wide", initial_sidebar_state="collapsed")

# --- CSS DE ALTA PRECISÃO (PARA FICAR IGUAL AO IDX) ---
st.markdown("""
    <style>
    /* Esconder elementos padrão do Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { background-color: #1e293b; border-radius: 8px 8px 0 0; gap: 10px; padding: 5px; }
    .stTabs [data-baseweb="tab"] { height: 40px; background-color: transparent; border: none; color: #94a3b8; }
    .stTabs [aria-selected="true"] { background-color: #334155 !important; color: white !important; border-radius: 4px; border-bottom: 2px solid #3b82f6 !important; }
    
    /* Fundo Total Escuro */
    .stApp { background-color: #0f172a; }
    
    /* Estilo dos Cards (O segredo do visual) */
    .css-1r6slb0, .stVerticalBlock { gap: 0.5rem; }
    div[data-testid="stVerticalBlock"] > div:has(div.section-card) { background: transparent; }
    
    .section-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }

    /* Inputs Dark */
    input, textarea { 
        background-color: #0f172a !important; 
        color: #e2e8f0 !important; 
        border: 1px solid #334155 !important; 
    }
    
    /* Botão Processar */
    .stButton>button {
        background: linear-gradient(to bottom, #3b82f6, #1d4ed8);
        border: none;
        padding: 12px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #334155; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="background:#3b82f6; width:40px; height:40px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:bold;">S</div>
            <div>
                <h2 style="margin:0; color:white; font-size:1.1rem; letter-spacing:2px;">SOMA AÇO</h2>
                <span style="color:#64748b; font-size:0.7rem;">ALGORITMO DE AGRUPAMENTO E CONFERÊNCIA DE LOTES</span>
            </div>
        </div>
        <div style="color:#475569; font-size:0.8rem;">Industrial v1.0</div>
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE HISTÓRICO ---
if 'historico' not in st.session_state: st.session_state.historico = []

# --- CORPO DO APP ---
tab1, tab2 = st.tabs(["Configuração", "Histórico"])

with tab1:
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-bottom:20px;'>📦 ENTRADA DE DADOS</h4>", unsafe_allow_html=True)
        
        lote = st.text_input("IDENTIFICAÇÃO DO LOTE", placeholder="Ex: Lote 181")
        meta = st.number_input("META DE PESO (KG)", min_value=0.0, format="%.2f")
        qtd = st.number_input("QTD. ROLOS (OPCIONAL)", min_value=0)
        
        pesos_input = st.text_area("PESOS DOS ROLOS", placeholder="600, 550, 595...", height=100)
        
        if st.button("▶ PROCESSAR AGRUPAMENTO"):
            if lote and meta > 0:
                if len(st.session_state.historico) >= 6: st.session_state.historico.pop(0)
                st.session_state.historico.append({"id": lote, "meta": meta, "data": pd.Timestamp.now().strftime("%H:%M")})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card" style="min-height:430px; display:flex; flex-direction:column; justify-content:center; align-items:center; border: 2px dashed #334155;">', unsafe_allow_html=True)
        if not st.session_state.historico:
            st.markdown("""
                <div style="font-size:4rem; opacity:0.1;">📋</div>
                <h3 style="color:#94a3b8;">Aguardando Lotes & Estoque</h3>
                <p style="color:#475569; font-size:0.9rem;">Cadastre as metas para iniciar o processamento.</p>
            """, unsafe_allow_html=True)
        else:
            ultimo = st.session_state.historico[-1]
            st.success(f"Lote {ultimo['id']} ativo")
            st.info("Algoritmo em execução...")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<div style='text-align:center; margin-top:40px; color:#475569; font-size:0.8rem;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</div>", unsafe_allow_html=True)
