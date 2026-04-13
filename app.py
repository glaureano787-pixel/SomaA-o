import streamlit as st
import pandas as pd
from itertools import combinations

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Gestão de Histórico", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Visual Industrial
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .section-card { background-color: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 15px; }
    .lote-item { background-color: #0f172a; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-left: 4px solid #3b82f6; }
    .hist-item { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 10px; }
    input, textarea { background-color: #020617 !important; border: 1px solid #334155 !important; color: #f1f5f9 !important; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; padding: 12px; font-weight: 700; border-radius: 8px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1e293b; border-radius: 8px; padding: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DO ALGORITMO ---
def encontrar_combinacao(pesos, alvo, qtd_alvo=None, tolerancia=0.5):
    r_range = [qtd_alvo] if qtd_alvo and qtd_alvo > 0 else range(1, len(pesos) + 1)
    for r in r_range:
        if r > len(pesos): continue
        for combo in combinations(pesos, r):
            if abs(sum(combo) - alvo) <= tolerancia:
                return list(combo)
    return None

# --- HEADER ---
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 15px; margin-bottom: 25px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background-color:#3b82f6; width:45px; height:45px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:1.5rem;">S</div>
            <div><h1 style="margin:0; font-size:1.1rem; color:white;">SOMA AÇO</h1><p style="margin:0; font-size:0.7rem; color:#94a3b8;">HISTÓRICO E GESTÃO DE CARGAS</p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Session State
if 'lista_lotes' not in st.session_state: st.session_state.lista_lotes = []
if 'historico_operacoes' not in st.session_state: st.session_state.historico_operacoes = []
if 'resultados_atuais' not in st.session_state: st.session_state.resultados_atuais = None

tab_config, tab_hist = st.tabs(["⚙️ Painel de Montagem", "⏱️ Histórico"])

with tab_config:
    col_input, col_lista = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-top:0;'>1. CADASTRAR LOTES</h4>", unsafe_allow_html=True)
        with st.container():
            c_id = st.text_input("ID DO LOTE", placeholder="Ex: Lote 101")
            c_meta = st.number_input("PESO TOTAL (KG)", min_value=0.0, step=0.1)
            c_qtd = st.number_input("QTD ROLOS (OPCIONAL)", min_value=0, step=1)
            if st.button("➕ ADICIONAR À FILA"):
                if c_id and c_meta > 0:
                    st.session_state.lista_lotes.append({"id": c_id, "meta": c_meta, "qtd": c
