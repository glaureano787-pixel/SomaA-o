import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Industrial", layout="wide", initial_sidebar_state="collapsed")

# 2. O "Tuning" Visual (CSS Avançado)
st.markdown("""
    <style>
    /* Esconder elementos desnecessários */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}

    /* Fundo Principal Estilo IDX */
    .stApp { background-color: #0f172a; color: #f8fafc; }
    
    /* Estilização das Abas (Tabs) */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #1e293b; 
        border-radius: 8px; 
        padding: 5px;
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border: none !important;
        background-color: transparent !important;
        color: #94a3b8 !important;
        border-radius: 6px !important;
        padding: 0 20px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #334155 !important;
        color: #3b82f6 !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
    }

    /* Cards de Seção */
    .section-card {
        background-color: #1e293b;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }

    /* Inputs Estilo Dark */
    input, textarea {
        background-color: #020617 !important;
        border: 1px solid #334155 !important;
        color: #f1f5f9 !important;
        border-radius: 6px !important;
    }
    
    /* Botão Principal Processar */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho Superior (Header)
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 15px; margin-bottom: 25px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background-color:#3b82f6; width:45px; height:45px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:1.5rem;">S</div>
            <div>
                <h1 style="margin:0; font-size:1.3rem; letter-spacing:1px; color:white;">SOMA AÇO</h1>
                <p style="margin:0; font-size:0.75rem; color:#94a3b8; font-weight:300;">ALGORITMO DE AGRUPAMENTO E CONFERÊNCIA DE LOTES</p>
            </div>
        </div>
        <div style="text-align: right;">
            <span style="display:block; font-size:0.8rem; color:#3b82f6; font-weight:bold;">Painel de Operações</span>
            <span style="font-size:0.7rem; color:#475569;">Industrial v1.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. Lógica de Persistência
if 'historico' not in st.session_state:
    st.session_state.historico = []

# 5. Organização por Tabs
tab_config, tab_hist = st.tabs(["⚙ Configuração", "📜 Histórico"])

with tab_config:
    col_input, col_view = st.columns([1, 1.3], gap="large")
    
    with col_input:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-bottom:15px; font-size:1rem;'>ENTRADA DE DADOS</h4>", unsafe_allow_html=True)
        
        lote_id = st.text_input("ID DO LOTE", placeholder="Ex: Lote 181")
        
        c1, c2 = st.columns(2)
        with c1:
            meta = st.number_input("META DE PESO (KG)", min_value=0.0, step=0.1)
        with c2:
            qtd = st.number_input("QTD. ROLOS", min_value=0)
            
        pesos_raw = st.text_area("ESTOQUE (PESOS DOS ROLOS)", placeholder="Ex: 600, 550, 595...", height=120)
        
        if st.button("▶ PROCESSAR AGRUPAMENTO"):
            if lote_id and meta > 0:
                # Lógica de limite de 6 itens
                if len(st.session_state.historico) >= 6:
                    st.session_state.historico.pop(0)
                
                novo = {"id": lote_id, "meta": meta, "pesos": pesos_raw, "hora": pd.Timestamp.now().strftime("%H:%M")}
                st.session_state.historico.append(novo)
                st.success(f"Lote {lote_id} processado com sucesso!")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_view:
        # Card de Resultado Estilo Placeholder do IDX
        st.markdown('<div class="section-card" style="min-height:460px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; border: 2px dashed #334155;">', unsafe_allow_html=True)
        if not st.session_state.historico:
            st.markdown("""
                <div style="font-size:4.5rem; color:#334155; margin-bottom:20px;">📊</div>
                <h3 style="color:#94a3b8; margin:0;">Aguardando Lotes & Estoque</h3>
                <p style="color:#475569; max-width:300px;">Cadastre as metas de peso e os rolos disponíveis para o algoritmo processar as combinações.</p>
            """, unsafe_allow_html=True)
        else:
            ultimo = st.session_state.historico[-1]
            st.markdown(f"<h2 style='color:#3b82f6;'>Lote Ativo: {ultimo['id']}</h2>", unsafe_allow_html=True)
            st.info(f"Otimizando para meta de {ultimo['meta']} KG...")
        st.markdown('</div>', unsafe_allow_html=True)

with tab_hist:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("<h4>HISTÓRICO RECENTE</h4>", unsafe_allow_html=True)
    if not st.session_state.historico:
        st.write("Nenhum dado processado.")
    else:
        # Mostrar do mais novo para o mais antigo
        for i, item in enumerate(reversed(st.session_state.historico)):
            idx_original = len(st.session_state.historico) - 1 - i
            c_h1, c_h2, c_h3 = st.columns([3, 1, 1])
            with c_h1:
                st.write(f"**{item['id']}** | Meta: {item['meta']}kg")
            with c_h2:
                st.caption(f"🕒 {item['hora']}")
            with c_h3:
                if st.button("Remover", key=f"del_{idx_original}"):
                    st.session_state.historico.pop(idx_original)
                    st.rerun()
            st.markdown("<hr style='margin:10px 0; border-color:#334155;'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown("<p style='text-align: center; color: #475569; font-size: 0.8rem; margin-top: 40px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
