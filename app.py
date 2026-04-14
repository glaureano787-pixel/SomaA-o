import streamlit as st
import pandas as pd
from itertools import permutations

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Gestão Industrial", layout="wide", initial_sidebar_state="collapsed")

# 2. Session State
if 'lista_lotes' not in st.session_state: st.session_state.lista_lotes = []
if 'historico_operacoes' not in st.session_state: st.session_state.historico_operacoes = []
if 'resultados_atuais' not in st.session_state: st.session_state.resultados_atuais = None
if 'form_reset_key' not in st.session_state: st.session_state.form_reset_key = 0

# 3. Ícone SVG
icon_logo_rolls = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 15px;"><circle cx="7" cy="14" r="5"/><circle cx="17" cy="14" r="5"/><circle cx="12" cy="7" r="5"/></svg>'

# 4. CSS Estilizado
st.markdown(f"""
    <style>
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stApp {{ background-color: #0f172a; color: #f8fafc; }}
    .section-card {{ background-color: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 15px; }}
    .lote-item {{ background-color: #0f172a; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #3b82f6; display: flex; justify-content: space-between; align-items: center; }}
    input, textarea {{ background-color: #020617 !important; border: 1px solid #334155 !important; color: #f1f5f9 !important; }}
    .stButton>button {{ width: 100%; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; border-radius: 8px; font-weight: 700; padding: 10px; }}
    .brand-title {{ font-size: 2.2rem; font-weight: 800; color: white; line-height: 1; margin: 0; }}
    .brand-subtitle {{ font-size: 0.85rem; color: #94a3b8; margin: 0; }}
    .resultado-balao {{ background-color: #3b82f6; padding: 15px; border-radius: 12px; color: white; margin-bottom: 10px; border: 1px solid #60a5fa; }}
    .resultado-balao-falha {{ background-color: #991b1b; padding: 15px; border-radius: 12px; color: #fecaca; margin-bottom: 10px; border: 1px solid #f87171; }}
    .alerta-sobra {{ background-color: #fbbf24; padding: 15px; border-radius: 12px; color: #451a03; margin-top: 10px; font-weight: bold; border: 2px solid #d97706; }}
    </style>
    """, unsafe_allow_html=True)

# 5. NOVO MOTOR DE CÁLCULO: Backtracking para exatidão total
def resolver_carregamento(pesos, lotes):
    def backtrack(index_lote, pesos_restantes):
        if index_lote == len(lotes):
            return [], pesos_restantes
        
        alvo = lotes[index_lote]['meta']
        qtd_fixa = lotes[index_lote]['qtd']
        
        # Tenta todas as combinações possíveis para o lote atual
        r_range = [qtd_fixa] if qtd_fixa > 0 else range(1, len(pesos_restantes) + 1)
        
        from itertools import combinations
        for r in r_range:
            for combo in combinations(pesos_restantes, r):
                if sum(combo) == alvo:
                    novos_pesos = list(pesos_restantes)
                    for p in combo: novos_pesos.remove(p)
                    
                    resultado_posterior, sobra_final = backtrack(index_lote + 1, novos_pesos)
                    
                    if resultado_posterior is not None:
                        return [{"id": lotes[index_lote]['id'], "rolos": list(combo), "status": "✅"}] + resultado_posterior, sobra_final
        return None, None

    return backtrack(0, pesos)

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

with tab_config:
    col_input, col_lista = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"<h4 style='color:#3b82f6; margin-top:0; font-size:0.9rem;'>ADICIONAR LOTE</h4>", unsafe_allow_html=True)
        
        c_id = st.text_input("ID DO LOTE", key=f"id_f_{st.session_state.form_reset_key}")
        c_meta = st.number_input("PESO TOTAL (KG)", min_value=0, step=1, key=f"meta_f_{st.session_state.form_reset_key}")
        c_qtd = st.number_input("QTD ROLOS (OPCIONAL)", min_value=0, step=1, key=f"qtd_f_{st.session_state.form_reset_key}")
        
        if st.button("➕ ADICIONAR À FILA"):
            if c_id and c_meta > 0:
                st.session_state.lista_lotes.append({"id": c_id, "meta": int(c_meta), "qtd": int(c_qtd)})
                st.session_state.form_reset_key += 1
                st.rerun()

        st.markdown('</div><div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-top:0; font-size:0.9rem;'>PROCESSAR</h4>", unsafe_allow_html=True)
        estoque_txt = st.text_area("PESOS DOS ROLOS RECEBIDOS", height=120, help="Separe por espaço, vírgula ou uma por linha")
        
        if st.button("▶ INICIAR CONFERÊNCIA"):
            if st.session_state.lista_lotes and estoque_txt:
                try:
                    dados_limpos = estoque_txt.replace('\n', ' ').replace(',', ' ')
                    estoque = [int(x.strip()) for x in dados_limpos.split() if x.strip()]
                    
                    solucao, sobras = resolver_carregamento(estoque, st.session_state.lista_lotes)
                    
                    if solucao:
                        res_final = {"lotes": solucao, "sobras": sobras}
                    else:
                        # Se o motor global falhar, ele mostra quais lotes não bateram individualmente
                        res_final = {"lotes": [{"id": l['id'], "status": "❌", "rolos": None} for l in st.session_state.lista_lotes], "sobras": estoque}

                    st.session_state.historico_operacoes.insert(0, {
                        "hora": pd.Timestamp.now().strftime("%H:%M:%S"),
                        "entrada": estoque_txt,
                        "detalhes": res_final["lotes"],
                        "sobras": res_final["sobras"]
                    })
                    st.session_state.resultados_atuais = res_final
                    st.session_state.lista_lotes = []
                    st.rerun()
                except: st.error("Verifique se os pesos são apenas números inteiros.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_lista:
        st.markdown("<h4 style='color:#94a3b8; font-size:0.9rem;'>FILA DE PROCESSAMENTO:</h4>", unsafe_allow_html=True)
        for i, l in enumerate(st.session_state.lista_lotes):
            st.markdown(f'<div class="lote-item"><b>{l["id"]}</b> | {l["meta"]}kg</div>', unsafe_allow_html=True)
        
        if st.session_state.resultados_atuais:
            st.markdown("<h4 style='color:#3b82f6; font-size:0.9rem; margin-top:20px;'>RESULTADO DA CONFERÊNCIA:</h4>", unsafe_allow_html=True)
            for r in st.session_state.resultados_atuais['lotes']:
                if r['status'] == "✅":
                    rolos = [f"{p}kg" for p in r['rolos']]
                    st.markdown(f'<div class="resultado-balao"><b>✅ {r["id"]}</b><br><small>{len(r["rolos"])} rolos: {rolos}</small></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="resultado-balao-falha"><b>❌ {r["id"]}</b><br><small>Erro: Não foi encontrada combinação para este peso.</small></div>', unsafe_allow_html=True)
            
            sobras = st.session_state.resultados_atuais['sobras']
            if sobras:
                st.markdown(f'<div class="alerta-sobra">⚠️ SOBRAS NÃO ALOCADAS: {sobras}</div>', unsafe_allow_html=True)
            else:
                st.success("Conferência perfeita! Todos os rolos batem com os lotes.")

with tab_hist:
    for idx, op in enumerate(st.session_state.historico_operacoes):
        st.markdown('<div class="hist-item">', unsafe_allow_html=True)
        st.write(f"**Carga {op['hora']}**")
        for d in op['detalhes']:
            st.write(f"{d['status']} {d['id']}: {d['rolos'] if d['rolos'] else 'FALHA'}")
        if op['sobras']: st.write(f"Sobra: {op['sobras']}")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #475569; font-size: 0.7rem; margin-top: 40px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
