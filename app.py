import streamlit as st
import pandas as pd
from itertools import combinations

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Gestão Industrial", layout="wide", initial_sidebar_state="collapsed")

# 2. Session State
if 'lista_lotes' not in st.session_state: st.session_state.lista_lotes = []
if 'historico_operacoes' not in st.session_state: st.session_state.historico_operacoes = []
if 'resultados_atuais' not in st.session_state: st.session_state.resultados_atuais = None
if 'form_reset_key' not in st.session_state: st.session_state.form_reset_key = 0

# 3. CSS Original Restaurado
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
    </style>
    """, unsafe_allow_html=True)

# 4. Motor de Cálculo Robusto
def resolver_carregamento(pesos, lotes):
    def backtrack(idx, pesos_disponiveis):
        if idx == len(lotes):
            return [], pesos_disponiveis
        
        lote = lotes[idx]
        alvo = lote['meta']
        qtd = lote['qtd']
        
        # Define o intervalo de busca para a quantidade de rolos
        r_range = [qtd] if qtd > 0 else range(1, len(pesos_disponiveis) + 1)
        
        for r in r_range:
            if r > len(pesos_disponiveis): continue
            for combo in combinations(pesos_disponiveis, r):
                if sum(combo) == alvo:
                    restantes = list(pesos_disponiveis)
                    for p in combo: restantes.remove(p)
                    
                    res_posterior, sobra_final = backtrack(idx + 1, restantes)
                    if res_posterior is not None:
                        return [{"id": lote['id'], "meta": alvo, "rolos": list(combo), "status": "✅"}] + res_posterior, sobra_final
        return None, None

    return backtrack(0, pesos)

# --- HEADER ---
st.markdown('<h1 class="brand-title">SOMA AÇO</h1><p class="brand-subtitle">SISTEMA DE GESTÃO E CONFERÊNCIA DE CARGAS</p>', unsafe_allow_html=True)

tab_painel, tab_hist = st.tabs(["Painel", "Histórico"])

with tab_painel:
    col_in, col_out = st.columns([1, 1], gap="large")
    
    with col_in:
        # ADICIONAR LOTE
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-top:0; font-size:0.9rem;'>ADICIONAR LOTE</h4>", unsafe_allow_html=True)
        c_id = st.text_input("ID DO LOTE", key=f"id_{st.session_state.form_reset_key}")
        c_meta = st.number_input("PESO TOTAL (KG)", min_value=0, step=1, key=f"meta_{st.session_state.form_reset_key}")
        c_qtd = st.number_input("QTD ROLOS (OPCIONAL)", min_value=0, step=1, key=f"qtd_{st.session_state.form_reset_key}")
        
        if st.button("➕ ADICIONAR À FILA"):
            if c_id and c_meta > 0:
                st.session_state.lista_lotes.append({"id": str(c_id).upper(), "meta": int(c_meta), "qtd": int(c_qtd)})
                st.session_state.form_reset_key += 1
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # PROCESSAR
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-top:0; font-size:0.9rem;'>PROCESSAR</h4>", unsafe_allow_html=True)
        pesos_input = st.text_area("PESOS DOS ROLOS RECEBIDOS", height=120, placeholder="Digite ou cole os pesos...")
        
        if st.button("▶ INICIAR CONFERÊNCIA"):
            if not st.session_state.lista_lotes:
                st.error("Adicione pelo menos um lote na fila.")
            elif not pesos_input.strip():
                st.error("Insira os pesos dos rolos.")
            else:
                try:
                    # Limpeza profunda dos dados de entrada
                    import re
                    # Encontra todos os números no texto, ignorando vírgulas, espaços e letras
                    estoque = [int(n) for n in re.findall(r'\d+', pesos_input)]
                    
                    solucao, sobras = resolver_carregamento(estoque, st.session_state.lista_lotes)
                    
                    if solucao:
                        res_final = {"lotes": solucao, "sobras": sobras}
                    else:
                        res_final = {
                            "lotes": [{"id": l['id'], "meta": l['meta'], "status": "❌", "rolos": None} for l in st.session_state.lista_lotes],
                            "sobras": estoque
                        }
                    
                    st.session_state.historico_operacoes.insert(0, {
                        "hora": pd.Timestamp.now().strftime("%H:%M:%S"),
                        "detalhes": res_final["lotes"],
                        "sobras": res_final["sobras"]
                    })
                    st.session_state.resultados_atuais = res_final
                    st.session_state.lista_lotes = []
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao processar dados. Verifique a formatação.")

        st.markdown('</div>', unsafe_allow_html=True)

        # LIMPAR TELA
        if st.button("🧹 LIMPAR TELA"):
            st.session_state.lista_lotes = []
            st.session_state.resultados_atuais = None
            st.session_state.form_reset_key += 1
            st.rerun()

    with col_out:
        st.markdown("<h4 style='color:#94a3b8; font-size:0.9rem;'>FILA / RESULTADOS:</h4>", unsafe_allow_html=True)
        
        # Exibe fila de espera
        for l in st.session_state.lista_lotes:
            st.markdown(f'<div class="lote-item"><b>{l["id"]}</b>: {l["meta"]}kg</div>', unsafe_allow_html=True)
        
        # Exibe resultados do último processamento
        if st.session_state.resultados_atuais:
            for r in st.session_state.resultados_atuais['lotes']:
                if r['status'] == "✅":
                    st.markdown(f"""
                        <div class="resultado-balao">
                            <b>✅ Lote: {r["id"]}</b><br>
                            <small>{len(r["rolos"])} rolos: {r["rolos"]}</small>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="resultado-balao-falha"><b>❌ Lote: {r["id"]}</b>: Não foi possível fechar {r["meta"]}kg.</div>', unsafe_allow_html=True)
            
            if st.session_state.resultados_atuais['sobras']:
                st.warning(f"SOBRAS NÃO ALOCADAS: {st.session_state.resultados_atuais['sobras']}")

with tab_hist:
    for op in st.session_state.historico_operacoes:
        with st.expander(f"Carga às {op['hora']}"):
            for d in op['detalhes']:
                st.write(f"{d['status']} {d['id']} ({d['meta']}kg): {d['rolos']}")
            if op['sobras']: st.write(f"Sobras: {op['sobras']}")

st.markdown("<p style='text-align: center; color: #475569; font-size: 0.7rem; margin-top: 40px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
