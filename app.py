import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Industrial", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS para Visual Industrial (Estilo IDX)
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #0f172a; color: #f8fafc; }
    
    /* Abas Minimalistas */
    .stTabs [data-baseweb="tab-list"] { background-color: #1e293b; border-radius: 8px; padding: 5px; }
    .stTabs [data-baseweb="tab"] { height: 45px; color: #94a3b8 !important; }
    .stTabs [aria-selected="true"] { color: #3b82f6 !important; border-bottom: 2px solid #3b82f6 !important; }

    /* Cards e Inputs */
    .section-card {
        background-color: #1e293b;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    input, textarea { background-color: #020617 !important; border: 1px solid #334155 !important; color: #f1f5f9 !important; }
    
    /* Botão Azul Profissional */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 15px;
        font-weight: 700;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Ícones Minimalistas (Traços)
icon_gear = '⚙️' # Engrenagem minimalista
icon_timer = '⏱️' # Cronômetro minimalista
icon_calc = '<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="1.5"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="16" y1="14" x2="16" y2="14.01"/><line x1="12" y1="14" x2="12" y2="14.01"/><line x1="8" y1="14" x2="8" y2="14.01"/><line x1="8" y1="10" x2="16" y2="10"/></svg>'

# --- INTERFACE ---
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 15px; margin-bottom: 25px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background-color:#3b82f6; width:45px; height:45px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:1.5rem;">S</div>
            <div>
                <h1 style="margin:0; font-size:1.1rem; letter-spacing:1px; color:white;">SOMA AÇO</h1>
                <p style="margin:0; font-size:0.7rem; color:#94a3b8;">ALGORITMO DE AGRUPAMENTO E CONFERÊNCIA DE LOTES</p>
            </div>
        </div>
        <div style="text-align: right; color:#475569; font-size:0.7rem;">Industrial v1.0</div>
    </div>
    """, unsafe_allow_html=True)

if 'historico' not in st.session_state: st.session_state.historico = []

tab_config, tab_hist = st.tabs([f"{icon_gear} Configuração", f"{icon_timer} Histórico"])

with tab_config:
    col_in, col_out = st.columns([1, 1.3], gap="large")
    with col_in:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-bottom:15px; font-size:0.9rem;'>ENTRADA DE DADOS</h4>", unsafe_allow_html=True)
        lote_id = st.text_input("ID DO LOTE", placeholder="Ex: Lote 181")
        meta = st.number_input("META DE PESO (KG)", min_value=0.0)
        pesos_raw = st.text_area("ESTOQUE (PESOS DOS ROLOS)", height=120)
        if st.button("▶ PROCESSAR AGRUPAMENTO"):
            if lote_id and meta > 0:
                if len(st.session_state.historico) >= 6: st.session_state.historico.pop(0)
                st.session_state.historico.append({"id": lote_id, "meta": meta})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_out:
        st.markdown('<div class="section-card" style="min-height:460px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; border: 2px dashed #334155;">', unsafe_allow_html=True)
        if not st.session_state.historico:
            st.markdown(f'<div>{icon_calc}</div>', unsafe_allow_html=True)
            st.markdown("<h3 style='color:#94a3b8;'>Aguardando Lotes</h3>", unsafe_allow_html=True)
        else:
            st.success(f"Lote {st.session_state.historico[-1]['id']} Ativo")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#475569; font-size:0.7rem; margin-top:40px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
