import streamlit as st
import pandas as pd
from itertools import combinations

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Otimizador Multi-Lotes", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Visual Industrial
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .section-card { background-color: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 15px; }
    .lote-item { background-color: #0f172a; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-left: 4px solid #3b82f6; }
    .result-box { background-color: #020617; padding: 15px; border-radius: 8px; border: 1px solid #3b82f6; margin-top: 10px; }
    input, textarea { background-color: #020617 !important; border: 1px solid #334155 !important; color: #f1f5f9 !important; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; padding: 12px; font-weight: 700; border-radius: 8px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1e293b; border-radius: 8px; padding: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Ícones Minimalistas
icon_gear = '⚙️' 
icon_timer = '⏱️'

# --- LÓGICA DO ALGORITMO ---
def encontrar_combinacao(pesos, alvo, qtd_alvo=None, tolerancia=0.5):
    # Se houver quantidade definida, foca apenas em combinações daquele tamanho
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
            <div><h1 style="margin:0; font-size:1.1rem; color:white;">SOMA AÇO</h1><p style="margin:0; font-size:0.7rem; color:#94a3b8;">IDENTIFICAÇÃO DE MÚLTIPLOS LOTES</p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Session State para gerenciar múltiplos lotes antes do cálculo
if 'lista_lotes' not in st.session_state: st.session_state.lista_lotes = []
if 'resultados_processados' not in st.session_state: st.session_state.resultados_processados = None

tab_config, tab_hist = st.tabs([f"{icon_gear} Painel de Montagem", f"{icon_timer} Histórico"])

with tab_config:
    col_input, col_lista = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-top:0;'>1. CADASTRAR LOTES DA NOTA</h4>", unsafe_allow_html=True)
        
        with st.container():
            c_id = st.text_input("NOME/ID DO LOTE", placeholder="Ex: Lote 01")
            c_meta = st.number_input("PESO TOTAL DO LOTE (KG)", min_value=0.0, step=0.1)
            c_qtd = st.number_input("QTD ROLOS (OPCIONAL - 0 PARA IGNORAR)", min_value=0, step=1)
            
            if st.button("➕ ADICIONAR LOTE À LISTA"):
                if c_id and c_meta > 0:
                    st.session_state.lista_lotes.append({"id": c_id, "meta": c_meta, "qtd": c_qtd})
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-top:0;'>2. ESTOQUE DE ROLOS</h4>", unsafe_allow_html=True)
        estoque_txt = st.text_area("COLE TODOS OS PESOS DOS ROLOS RECEBIDOS", height=150, placeholder="500, 480, 600.5...")
        
        if st.button("▶ PROCESSAR TODOS OS LOTES"):
            if not st.session_state.lista_lotes:
                st.error("Adicione pelo menos um lote na lista ao lado.")
            else:
                try:
                    estoque = [float(x.strip()) for x in estoque_txt.replace('\n', ',').split(',') if x.strip()]
                    temp_estoque = estoque.copy()
                    resultados = []
                    
                    for lote in st.session_state.lista_lotes:
                        encontrado = encontrar_combinacao(temp_estoque, lote['meta'], lote['qtd'])
                        if encontrado:
                            for p in encontrado: temp_estoque.remove(p)
                            resultados.append({"id": lote['id'], "meta": lote['meta'], "rolos": encontrado, "status": "Sucesso"})
                        else:
                            resultados.append({"id": lote['id'], "meta": lote['meta'], "rolos": [], "status": "Não encontrado"})
                    
                    st.session_state.resultados_processados = {"lotes": resultados, "sobra": temp_estoque}
                except Exception as e:
                    st.error("Verifique se os pesos dos rolos estão corretos (apenas números e vírgulas).")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_lista:
        st.markdown("<h4 style='color:#94a3b8;'>LOTES AGUARDANDO:</h4>", unsafe_allow_html=True)
        if not st.session_state.lista_lotes:
            st.info("Lista vazia. Adicione os lotes da nota fiscal à esquerda.")
        else:
            for i, lote in enumerate(st.session_state.lista_lotes):
                st.markdown(f"""
                <div class="lote-item">
                    <b>{lote['id']}</b> | Meta: {lote['meta']}kg | Rolos: {'Misto' if lote['qtd']==0 else lote['qtd']}
                </div>
                """, unsafe_allow_html=True)
            if st.button("❌ LIMPAR LISTA DE LOTES"):
                st.session_state.lista_lotes = []
                st.session_state.resultados_processados = None
                st.rerun()

        if st.session_state.resultados_processados:
            st.markdown("---")
            st.markdown("<h4 style='color:#3b82f6;'>RESULTADO DO AGRUPAMENTO:</h4>", unsafe_allow_html=True)
            for res in st.session_state.resultados_processados['lotes']:
                if res['status'] == "Sucesso":
                    st.success(f"**{res['id']}**: {res['rolos']} (Total: {sum(res['rolos'])}kg)")
                else:
                    st.error(f"**{res['id']}**: Nenhuma combinação encontrada.")
            
            st.warning(f"**SOBRA NO ESTOQUE:** {st.session_state.resultados_processados['sobra']}")

st.markdown("<p style='text-align: center; color: #475569; font-size: 0.7rem; margin-top: 40px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
