import streamlit as st
import pandas as pd
from itertools import combinations

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Gestão Industrial", layout="wide", initial_sidebar_state="collapsed")

# 2. Session State e Controle de Reset de Campos
if 'lista_lotes' not in st.session_state: st.session_state.lista_lotes = []
if 'historico_operacoes' not in st.session_state: st.session_state.historico_operacoes = []
if 'resultados_atuais' not in st.session_state: st.session_state.resultados_atuais = None
if 'form_count' not in st.session_state: st.session_state.form_count = 0

# 3. Definição de Ícones SVG
icon_trash = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>'
icon_paper_tab = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
icon_clock_tab = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
icon_logo_rolls = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 15px;"><circle cx="7" cy="14" r="5"/><circle cx="17" cy="14" r="5"/><circle cx="12" cy="7" r="5"/></svg>'

# 4. CSS Estilizado (Chaves dobradas {{ }} para evitar SyntaxError)
st.markdown(f"""
    <style>
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stApp {{ background-color: #0f172a; color: #f8fafc; }}
    .section-card {{ background-color: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 15px; }}
    .lote-item {{ background-color: #0f172a; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-left: 4px solid #3b82f6; }}
    .hist-item {{ background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 10px; }}
    input, textarea {{ background-color: #020617 !important; border: 1px solid #334155 !important; color: #f1f5f9 !important; }}
    .stButton>button {{ width: 100%; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; padding: 12px; font-weight: 700; border-radius: 8px; }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: #1e293b; border-radius: 8px; padding: 5px; }}
    
    .brand-title {{ font-size: 2.2rem; font-weight: 800; letter-spacing: -1px; margin: 0; color: white; line-height: 1; }}
    .brand-subtitle {{ font-size: 0.85rem; color: #94a3b8; letter-spacing: 1px; margin: 0; }}
    
    .resultado-balao {{
        background-color: #3b82f6;
        padding: 15px;
        border-radius: 12px;
        color: white;
        margin-bottom: 15px;
        border: 1px solid #60a5fa;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }}
    .resultado-balao-falha {{
        background-color: #991b1b;
        padding: 15px;
        border-radius: 12px;
        color: #fecaca;
        margin-bottom: 15px;
        border: 1px solid #f87171;
    }}
    </style>
    """, unsafe_allow_html=True)

# 5. Lógica do Algoritmo
def encontrar_combinacao(pesos, alvo, qtd_alvo=None, tolerancia=0.5):
    r_range = [qtd_alvo] if qtd_alvo and qtd_alvo > 0 else range(1, len(pesos) + 1)
    for r in r_range:
        if r > len(pesos): continue
        for combo in combinations(pesos, r):
            if abs(sum(combo) - alvo) <= tolerancia:
                return list(combo)
    return None

# --- HEADER ---
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid #334155; padding-bottom: 20px; margin-bottom: 30px;">
        <div style="display: flex; align-items: center;">
            {icon_logo_rolls}
            <div>
                <h1 class="brand-title">SOMA AÇO</h1>
                <p class="brand-subtitle">SISTEMA DE GESTÃO E CONFERÊNCIA DE CARGAS</p>
            </div>
        </div>
        <div style="text-align: right; color:#475569; font-size:0.75rem; font-weight: 600;">INDUSTRIAL v1.1</div>
    </div>
    """, unsafe_allow_html=True)

tab_config, tab_hist = st.tabs(["Painel", "Histórico"])

# Script para ícones (também com chaves duplicadas)
st.markdown(f"""<script>
    var tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
    if(tabs.length >= 2) {{
        tabs[0].innerHTML = '{icon_paper_tab} Painel';
        tabs[1].innerHTML = '{icon_clock_tab} Histórico';
    }}
</script>""", unsafe_allow_html=True)

with tab_config:
    col_input, col_lista = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-top:0; font-size:0.9rem;'>ADICIONAR LOTE</h4>", unsafe_allow_html=True)
        
        k = st.session_state.form_count
        c_id = st.text_input("ID DO LOTE", key=f"id_{k}", placeholder="Ex: Lote 01")
        c_meta = st.number_input("PESO TOTAL (KG)", key=f"meta_{k}", min_value=0.0, step=0.1)
        c_qtd = st.number_input("QTD ROLOS (OPCIONAL)", key=f"qtd_{k}", min_value=0, step=1)
        
        if st.button("➕ ADICIONAR À FILA"):
            if c_id and c_meta > 0:
                st.session_state.lista_lotes.append({"id": c_id, "meta": c_meta, "qtd": c_qtd})
                st.session_state.form_count += 1
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-top:0; font-size:0.9rem;'>PROCESSAR</h4>", unsafe_allow_html=True)
        estoque_txt = st.text_area("PESOS DOS ROLOS (VÍRGULA OU ESPAÇO)", height=100)
        if st.button("▶ INICIAR"):
            if st.session_state.lista_lotes and estoque_txt:
                try:
                    estoque = [float(x.strip()) for x in estoque_txt.replace('\n', ',').replace(' ', ',').split(',') if x.strip()]
                    temp_estoque = estoque.copy()
                    resultados = []
                    for lote in st.session_state.lista_lotes:
                        enc = encontrar_combinacao(temp_estoque, lote['meta'], lote['qtd'])
                        if enc:
                            for p in enc: temp_estoque.remove(p)
                            resultados.append({"id": lote['id'], "meta": lote['meta'], "rolos": enc, "status": "✅"})
                        else:
                            resultados.append({"id": lote['id'], "meta": lote['meta'], "rolos": [], "status": "❌"})
                    
                    nova_op = {"id": pd.Timestamp.now().strftime("%H:%M:%S"), "detalhes": resultados, "sobra": temp_estoque}
                    st.session_state.historico_operacoes.insert(0, nova_op)
                    if len(st.session_state.historico_operacoes) > 5: st.session_state.historico_operacoes.pop()
                    st.session_state.resultados_atuais = resultados
                    st.session_state.lista_lotes = []
                    st.rerun()
                except: st.error("Erro nos pesos.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_lista:
        st.markdown("<h4 style='color:#94a3b8; font-size:0.9rem;'>FILA DE PROCESSAMENTO:</h4>", unsafe_allow_html=True)
        for l in st.session_state.lista_lotes:
            st.markdown(f'<div class="lote-item"><b>{l["id"]}</b> - {l["meta"]}kg</div>', unsafe_allow_html=True)
        
        if st.session_state.resultados_atuais:
            st.markdown("<h4 style='color:#3b82f6; font-size:0.9rem; margin-top:20px;'>ÚLTIMO RESULTADO:</h4>", unsafe_allow_html=True)
            for r in st.session_state.resultados_atuais:
                if "✅" in r['status']:
                    st.markdown(f'<div class="resultado-balao"><b>✅ Lote: {r["id"]}</b><br>{r["rolos"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="resultado-balao-falha"><b>❌ Lote: {r["id"]}</b><br>Não encontrado.</div>', unsafe_allow_html=True)

with tab_hist:
    for idx, op in enumerate(st.session_state.historico_operacoes):
        st.markdown('<div class="hist-item">', unsafe_allow_html=True)
        c_txt, c_del = st.columns([10, 1])
        c_txt.markdown(f"**Carga às {op['id']}**")
        if c_del.button("🗑️", key=f"del_{idx}"):
            st.session_state.historico_operacoes.pop(idx)
            st.rerun()
        for d in op['detalhes']:
            cor = "#3b82f6" if "✅" in d['status'] else "#991b1b"
            st.markdown(f"<div style='border-left: 3px solid {cor}; padding-left: 10px; margin-bottom: 5px;'>{d['status']} <b>{d['id']}</b>: {d['rolos']}</div>", unsafe_allow_html=True)
        st.markdown(f"<small style='color:#475569'>Sobra: {op['sobra']}</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #475569; font-size: 0.7rem; margin-top: 40px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
