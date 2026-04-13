import streamlit as st
import pandas as pd
from itertools import combinations

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Otimizador Industrial", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Visual Industrial
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1e293b; border-radius: 8px; padding: 5px; gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 45px; color: #94a3b8 !important; }
    .stTabs [aria-selected="true"] { background-color: #334155 !important; color: #3b82f6 !important; border-bottom: 2px solid #3b82f6 !important; }
    .section-card { background-color: #1e293b; padding: 24px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 20px; }
    input, textarea { background-color: #020617 !important; border: 1px solid #334155 !important; color: #f1f5f9 !important; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; padding: 15px; font-weight: 700; border-radius: 8px; }
    .result-box { background-color: #020617; padding: 15px; border-radius: 8px; border-left: 5px solid #3b82f6; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Ícones Minimalistas
icon_gear = '⚙️' 
icon_timer = '⏱️'
icon_calc = '<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="1.5"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="16" y1="14" x2="16" y2="14.01"/><line x1="12" y1="14" x2="12" y2="14.01"/><line x1="8" y1="14" x2="8" y2="14.01"/><line x1="8" y1="10" x2="16" y2="10"/></svg>'

# --- FUNÇÃO DO ALGORITMO ---
def encontrar_combinacao(pesos, alvo, tolerancia=0.5):
    """Encontra a primeira combinação de pesos que soma o valor alvo."""
    for r in range(1, len(pesos) + 1):
        for combo in combinations(pesos, r):
            if abs(sum(combo) - alvo) <= tolerancia:
                return list(combo)
    return None

# --- CABEÇALHO ---
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 15px; margin-bottom: 25px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background-color:#3b82f6; width:45px; height:45px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:1.5rem;">S</div>
            <div><h1 style="margin:0; font-size:1.1rem; color:white;">SOMA AÇO</h1><p style="margin:0; font-size:0.7rem; color:#94a3b8;">SISTEMA DE IDENTIFICAÇÃO DE LOTES</p></div>
        </div>
        <div style="text-align: right; color:#475569; font-size:0.7rem;">Industrial v1.0</div>
    </div>
    """, unsafe_allow_html=True)

if 'historico' not in st.session_state: st.session_state.historico = []

tab_config, tab_hist = st.tabs([f"{icon_gear} Configuração", f"{icon_timer} Histórico"])

with tab_config:
    col_input, col_view = st.columns([1, 1.3], gap="large")
    
    with col_input:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-bottom:15px; font-size:0.9rem;'>ENTRADA DA NOTA</h4>", unsafe_allow_html=True)
        
        with st.form("lote_form"):
            lote_id = st.text_input("ID DO LOTE", placeholder="Ex: Lote A")
            meta = st.number_input("PESO TOTAL DA NOTA (KG)", min_value=0.0, step=0.1)
            estoque_txt = st.text_area("PESOS DE TODOS OS ROLOS (SEPARADOS POR VÍRGULA)", height=100, placeholder="Ex: 500, 450.5, 610...")
            
            submit = st.form_submit_button("▶ IDENTIFICAR ROLOS DO LOTE")
            
            if submit:
                try:
                    # Converter texto em lista de números
                    estoque = [float(x.strip()) for x in estoque_txt.replace('\n', ',').split(',') if x.strip()]
                    
                    resultado = encontrar_combinacao(estoque, meta)
                    
                    if resultado:
                        # Calcular o que sobrou
                        sobra = estoque.copy()
                        for r in resultado: sobra.remove(r)
                        
                        registro = {
                            "id": lote_id, "meta": meta, "encontrados": resultado, 
                            "sobra": sobra, "hora": pd.Timestamp.now().strftime("%H:%M")
                        }
                        st.session_state.historico.append(registro)
                        st.success(f"Combinação encontrada para o {lote_id}!")
                    else:
                        st.error("Nenhuma combinação exata encontrada no estoque informado.")
                except ValueError:
                    st.error("Erro nos dados: Use apenas números e vírgulas.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_view:
        st.markdown('<div class="section-card" style="min-height:460px;">', unsafe_allow_html=True)
        if not st.session_state.historico:
            st.markdown(f'<div style="text-align:center; padding-top:100px;">{icon_calc}<h3 style="color:#94a3b8;">Aguardando Processamento</h3></div>', unsafe_allow_html=True)
        else:
            res = st.session_state.historico[-1]
            st.markdown(f"<h3 style='color:#3b82f6; margin-top:0;'>Resultado: {res['id']}</h3>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="result-box">
                    <p style="color:#94a3b8; font-size:0.8rem; margin:0;">ROLOS IDENTIFICADOS (SOMA EXATA):</p>
                    <h2 style="color:#f8fafc; margin:5px 0;">{', '.join(map(str, res['encontrados']))}</h2>
                    <p style="color:#3b82f6; font-size:0.9rem; margin:0;">Total: {sum(res['encontrados'])} KG</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<p style='margin-top:20px; color:#94a3b8;'>ROLOS QUE SOBRARAM NO ESTOQUE:</p>", unsafe_allow_html=True)
            st.write(res['sobra'])
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #475569; font-size: 0.7rem; margin-top: 40px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
