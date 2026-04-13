import streamlit as st
import pandas as pd
from itertools import combinations

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Gestão Industrial", layout="wide", initial_sidebar_state="collapsed")

# 2. Session State
if 'lista_lotes' not in st.session_state: st.session_state.lista_lotes = []
if 'historico_operacoes' not in st.session_state: st.session_state.historico_operacoes = []
if 'resultados_atuais' not in st.session_state: st.session_state.resultados_atuais = None
if 'form_count' not in st.session_state: st.session_state.form_count = 0
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# 3. Definição de Ícones SVG
icon_trash = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>'
icon_edit = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>'
icon_paper_tab = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
icon_clock_tab = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 8px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
icon_logo_rolls = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 15px;"><circle cx="7" cy="14" r="5"/><circle cx="17" cy="14" r="5"/><circle cx="12" cy="7" r="5"/></svg>'

# 4. CSS Estilizado
st.markdown(f"""
    <style>
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stApp {{ background-color: #0f172a; color: #f8fafc; }}
    .section-card {{ background-color: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 15px; }}
    .lote-item {{ background-color: #0f172a; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #3b82f6; display: flex; justify-content: space-between; align-items: center; }}
    input, textarea {{ background-color: #020617 !important; border: 1px solid #334155 !important; color: #f1f5f9 !important; }}
    .stButton>button {{ width: 100%; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; border-radius: 8px; font-weight: 700; }}
    .brand-title {{ font-size: 2.2rem; font-weight: 800; color: white; line-height: 1; margin: 0; }}
    .brand-subtitle {{ font-size: 0.85rem; color: #94a3b8; margin: 0; }}
    .resultado-balao {{ background-color: #3b82f6; padding: 15px; border-radius: 12px; color: white; margin-bottom: 10px; border: 1px solid #60a5fa; }}
    </style>
    """, unsafe_allow_html=True)

# 5. Algoritmo
def encontrar_combinacao(pesos, alvo, qtd_alvo=None, tolerancia=0.5):
    r_range = [qtd_alvo] if qtd_alvo and qtd_alvo > 0 else range(1, len(pesos) + 1)
    for r in r_range:
        if r > len(pesos): continue
        for combo in combinations(pesos, r):
            if abs(sum(combo) - alvo) <= tolerancia: return list(combo)
    return None

# --- HEADER ---
st.markdown(f"""
    <div style="display: flex; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 20px; margin-bottom: 30px;">
        {icon_logo_rolls}
        <div>
            <h1 class="brand-title">SOMA AÇO</h1>
            <p class="brand-subtitle">SISTEMA DE GESTÃO E CONFERÊNCIA DE CARGAS</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

tab_config, tab_hist = st.tabs(["Painel", "Histórico"])

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
        label_botao = "💾 SALVAR ALTERAÇÃO" if st.session_state.edit_index is not None else "➕ ADICIONAR À FILA"
        st.markdown(f"<h4 style='color:#3b82f6; margin-top:0; font-size:0.9rem;'>{label_botao.split()[-1]} LOTE</h4>", unsafe_allow_html=True)
        
        # Lógica de Edição: se houver um index selecionado, preenche os campos com os valores atuais
        default_id = ""
        default_meta = 0.0
        default_qtd = 0
        
        if st.session_state.edit_index is not None:
            lote_edit = st.session_state.lista_lotes[st.session_state.edit_index]
            default_id = lote_edit['id']
            default_meta = lote_edit['meta']
            default_qtd = lote_edit['qtd']

        k = st.session_state.form_count
        c_id = st.text_input("ID DO LOTE", value=default_id, key=f"id_{k}")
        c_meta = st.number_input("PESO TOTAL (KG)", value=default_meta, key=f"meta_{k}", step=0.1)
        c_qtd = st.number_input("QTD ROLOS (OPCIONAL)", value=default_qtd, key=f"qtd_{k}", step=1)
        
        if st.button(label_botao):
            if c_id and c_meta > 0:
                novo_lote = {"id": c_id, "meta": c_meta, "qtd": c_qtd}
                if st.session_state.edit_index is not None:
                    st.session_state.lista_lotes[st.session_state.edit_index] = novo_lote
                    st.session_state.edit_index = None
                else:
                    st.session_state.lista_lotes.append(novo_lote)
                st.session_state.form_count += 1
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-top:0; font-size:0.9rem;'>PROCESSAR</h4>", unsafe_allow_html=True)
        estoque_txt = st.text_area("PESOS DOS ROLOS (VÍRGULA OU ESPAÇO)", height=100)
        if st.button("▶ INICIAR"):
            if st.session_state.lista_lotes and estoque_txt:
                try:
                    limpo = estoque_txt.replace('\n', ',').replace(' ', ',')
                    estoque = [float(x.strip()) for x in limpo.split(',') if x.strip()]
                    temp_estoque, resultados = estoque.copy(), []
                    for lote in st.session_state.lista_lotes:
                        enc = encontrar_combinacao(temp_estoque, lote['meta'], lote['qtd'])
                        if enc:
                            for p in enc: temp_estoque.remove(p)
                            resultados.append({"id": lote['id'], "meta": lote['meta'], "rolos": enc, "status": "✅"})
                        else:
                            resultados.append({"id": lote['id'], "meta": lote['meta'], "rolos": [], "status": "❌"})
                    st.session_state.historico_operacoes.insert(0, {"id": pd.Timestamp.now().strftime("%H:%M:%S"), "detalhes": resultados, "sobra": temp_estoque})
                    st.session_state.resultados_atuais = resultados
                    st.session_state.lista_lotes = []
                    st.rerun()
                except: st.error("Erro nos pesos.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_lista:
        st.markdown("<h4 style='color:#94a3b8; font-size:0.9rem;'>FILA DE PROCESSAMENTO:</h4>", unsafe_allow_html=True)
        for i, l in enumerate(st.session_state.lista_lotes):
            # Layout de cada item na fila com botões de ação
            col_lote_info, col_edit, col_del = st.columns([3, 0.5, 0.5])
            col_lote_info.markdown(f'<div class="lote-item"><b>{l["id"]}</b> | {l["meta"]}kg</div>', unsafe_allow_html=True)
            
            if col_edit.button("✏️", key=f"edt_btn_{i}"):
                st.session_state.edit_index = i
                st.rerun()
                
            if col_del.button("🗑️", key=f"del_btn_{i}"):
                st.session_state.lista_lotes.pop(i)
                st.rerun()
        
        if st.session_state.resultados_atuais:
            st.markdown("<h4 style='color:#3b82f6; font-size:0.9rem; margin-top:20px;'>ÚLTIMO RESULTADO:</h4>", unsafe_allow_html=True)
            for r in st.session_state.resultados_atuais:
                estilo = "resultado-balao" if "✅" in r['status'] else "resultado-balao-falha"
                st.markdown(f'<div class="{estilo}"><b>{r["status"]} {r["id"]}</b><br>{r["rolos"] if r["rolos"] else "Sem combinação"}</div>', unsafe_allow_html=True)

with tab_hist:
    for idx, op in enumerate(st.session_state.historico_operacoes):
        st.markdown('<div class="hist-item">', unsafe_allow_html=True)
        st.write(f"**Carga às {op['id']}**")
        for d in op['detalhes']:
            st.write(f"{d['status']} {d['id']}: {d['rolos']}")
        st.markdown(f"<small>Sobra: {op['sobra']}</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #475569; font-size: 0.7rem; margin-top: 40px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
