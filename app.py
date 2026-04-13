import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Industrial", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Avançado para Identidade Visual
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    .stApp { background-color: #0f172a; color: #f8fafc; }
    
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #1e293b; 
        border-radius: 8px; 
        padding: 5px;
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        color: #94a3b8 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #334155 !important;
        color: #3b82f6 !important;
        border-bottom: 2px solid #3b82f6 !important;
    }

    .section-card {
        background-color: #1e293b;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }

    input, textarea {
        background-color: #020617 !important;
        border: 1px solid #334155 !important;
        color: #f1f5f9 !important;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 15px;
        font-weight: 700;
        border-radius: 8px;
    }
    
    .icon-svg {
        vertical-align: middle;
        margin-right: 8px;
        fill: none;
        stroke: currentColor;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
    }
    </style>
    """, unsafe_allow_html=True)

# Definição dos ícones minimalistas (SVG)
icon_gear = '<svg class="icon-svg" width="20" height="20" viewBox="0 0 24 24"><path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1Z"/></svg>'
icon_timer = '<svg class="icon-svg" width="20" height="20" viewBox="0 0 24 24"><line x1="10" y1="2" x2="14" y2="2"/><line x1="12" y1="14" x2="15" y2="11"/><circle cx="12" cy="14" r="8"/></svg>'
icon_calc = '<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="16" y1="14" x2="16" y2="14.01"/><line x1="12" y1="14" x2="12" y2="14.01"/><line x1="8" y1="14" x2="8" y2="14.01"/><line x1="16" y1="18" x2="16" y2="18.01"/><line x1="12" y1="18" x2="12" y2="18.01"/><line x1="8" y1="18" x2="8" y2="18.01"/><line x1="16" y1="10" x2="16" y2="10.01"/><line x1="12" y1="10" x2="12" y2="10.01"/><line x1="8" y1="10" x2="8" y2="10.01"/></svg>'

# 3. Cabeçalho Superior
st.markdown(f"""
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

if 'historico' not in st.session_state: 
    st.session_state.historico = []

# 4. Tabs
tab_config, tab_hist = st.tabs(["Configuração", "Histórico"])

# Injeção manual dos ícones
st.markdown(f"""
    <script>
    var tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
    if(tabs.length >= 2) {{
        tabs[0].innerHTML = '{icon_gear} Configuração';
        tabs[1].innerHTML = '{icon_timer} Histórico';
    }}
    </script>
    """, unsafe_allow_html=True)

with tab_config:
    col_input, col_view = st.columns([1, 1.3], gap="large")
    with col_input:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-bottom:15px; font-size:0.9rem;'>ENTRADA DE DADOS</h4>", unsafe_allow_html=True)
        
        # Início do Formulário
        with st.form("lote_form", clear_on_submit=False):
            lote_id = st.text_input("ID DO LOTE", placeholder="Ex: Lote 181")
            c1, c2 = st.columns(2)
            with c1: meta = st.number_input("META DE PESO (KG)", min_value=0.0, step=0.1)
            with c2: qtd = st.number_input("QTD. ROLOS", min_value=0)
            pesos_raw = st.text_area("ESTOQUE (PESOS DOS ROLOS)", height=120, placeholder="600, 550, 595...")
            
            submit = st.form_submit_button("▶ PROCESSAR AGRUPAMENTO")
            
            if submit:
                if lote_id and meta > 0:
                    # Lógica simples para limpar o histórico e manter apenas os últimos 6
                    if len(st.session_state.historico) >= 6: 
                        st.session_state.historico.pop(0)
                    
                    st.session_state.historico.append({
                        "id": lote_id, 
                        "meta": meta, 
                        "hora": pd.Timestamp.now().strftime("%H:%M")
                    })
                    st.rerun()
                else:
                    st.error("Por favor, preencha o ID e a Meta.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_view:
        st.markdown('<div class="section-card" style="min-height:460px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; border: 2px dashed #334155;">', unsafe_allow_html=True)
        if not st.session_state.historico:
            st.markdown(f'<div style="margin-bottom:20px;">{icon_calc}</div>', unsafe_allow_html=True)
            st.markdown("""
                <h3 style="color:#94a3b8; margin:0; font-size:1.2rem;">Aguardando Lotes & Estoque</h3>
                <p style="color:#475569; font-size:0.8rem; max-width:280px;">Cadastre as metas de peso para o algoritmo processar as combinações.</p>
            """, unsafe_allow_html=True)
        else:
            ultimo = st.session_state.historico[-1]
            st.markdown(f"<h2 style='color:#3b82f6;'>Lote: {ultimo['id']}</h2>", unsafe_allow_html=True)
            st.info(f"Otimizando para {ultimo['meta']} KG...")
            # Aqui entrará a lógica de cálculo no futuro
        st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown("<p style='text-align: center; color: #475569; font-size: 0.7rem; margin-top: 40px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
