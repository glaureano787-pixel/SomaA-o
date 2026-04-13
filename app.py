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
                    st.session_state.lista_lotes.append({"id": c_id, "meta": c_meta, "qtd": c_qtd})
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-top:0;'>2. PROCESSAR CARGA</h4>", unsafe_allow_html=True)
        estoque_txt = st.text_area("PESOS DOS ROLOS DISPONÍVEIS", height=120, placeholder="600, 550, 480.5...")
        if st.button("▶ INICIAR AGRUPAMENTO"):
            if st.session_state.lista_lotes and estoque_txt:
                try:
                    estoque = [float(x.strip()) for x in estoque_txt.replace('\n', ',').split(',') if x.strip()]
                    temp_estoque = estoque.copy()
                    resultados = []
                    for lote in st.session_state.lista_lotes:
                        enc = encontrar_combinacao(temp_estoque, lote['meta'], lote['qtd'])
                        if enc:
                            for p in enc: temp_estoque.remove(p)
                            resultados.append({"id": lote['id'], "meta": lote['meta'], "rolos": enc, "status": "✅ Sucesso"})
                        else:
                            resultados.append({"id": lote['id'], "meta": lote['meta'], "rolos": [], "status": "❌ Falha"})
                    
                    # Salvar no histórico (limite de 5)
                    nova_op = {
                        "id": pd.Timestamp.now().strftime("%d/%m %H:%M"),
                        "detalhes": resultados,
                        "sobra": temp_estoque
                    }
                    st.session_state.historico_operacoes.insert(0, nova_op)
                    if len(st.session_state.historico_operacoes) > 5:
                        st.session_state.historico_operacoes.pop()
                    
                    st.session_state.resultados_atuais = resultados
                    st.session_state.lista_lotes = [] # Limpa a fila após processar
                except: st.error("Erro nos dados de estoque.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_lista:
        st.markdown("<h4 style='color:#94a3b8;'>FILA ATUAL:</h4>", unsafe_allow_html=True)
        for i, l in enumerate(st.session_state.lista_lotes):
            st.markdown(f'<div class="lote-item">{l["id"]} - {l["meta"]}kg</div>', unsafe_allow_html=True)
        
        if st.session_state.resultados_atuais:
            st.markdown("---")
            st.markdown("<h4 style='color:#3b82f6;'>RESULTADO ÚLTIMA OPERAÇÃO:</h4>", unsafe_allow_html=True)
            for r in st.session_state.resultados_atuais:
                st.write(f"{r['status']} **{r['id']}**: {r['rolos']}")

with tab_hist:
    if not st.session_state.historico_operacoes:
        st.info("Nenhum histórico registrado.")
    else:
        for idx, op in enumerate(st.session_state.historico_operacoes):
            with st.container():
                st.markdown(f'<div class="hist-item">', unsafe_allow_html=True)
                c_data, c_del = st.columns([4, 1])
                c_data.markdown(f"**Operação de {op['id']}**")
                
                # Botão de exclusão individual
                if c_del.button(f"🗑️", key=f"del_{idx}"):
                    st.session_state.historico_operacoes.pop(idx)
                    st.rerun()
                
                for d in op['detalhes']:
                    cor = "green" if "✅" in d['status'] else "red"
                    st.markdown(f"<span style='color:{cor}'>{d['status']}</span> **{d['id']}**: {d['rolos']}", unsafe_allow_html=True)
                
                st.markdown(f"<small style='color:#475569'>Sobra: {op['sobra']}</small>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #475569; font-size: 0.7rem; margin-top: 40px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
