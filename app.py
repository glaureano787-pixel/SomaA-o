import streamlit as st
import pandas as pd
from itertools import combinations

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Gestão Industrial", layout="wide", initial_sidebar_state="collapsed")

# 2. Session State
if 'lista_lotes' not in st.session_state: st.session_state.lista_lotes = []
if 'historico_operacoes' not in st.session_state: st.session_state.historico_operacoes = []
if 'resultados_atuais' not in st.session_state: st.session_state.resultados_atuais = None
if 'edit_index' not in st.session_state: st.session_state.edit_index = None
if 'input_pesos' not in st.session_state: st.session_state.input_pesos = ""

# Estados para os campos de texto (permitem o reset automático)
if 'temp_id' not in st.session_state: st.session_state.temp_id = ""
if 'temp_meta' not in st.session_state: st.session_state.temp_meta = 0
if 'temp_qtd' not in st.session_state: st.session_state.temp_qtd = 0

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
    .hist-item {{ background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# 5. Algoritmo para Números Inteiros
def encontrar_combinacao(pesos, alvo, qtd_alvo=None, tolerancia=0):
    r_range = [qtd_alvo] if qtd_alvo and qtd_alvo > 0 else range(1, len(pesos) + 1)
    for r in r_range:
        if r > len(pesos): continue
        for combo in combinations(pesos, r):
            if abs(sum(combo) - alvo) <= tolerancia:
                return list(combo)
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

with tab_config:
    col_input, col_lista = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        label_botao = "💾 SALVAR ALTERAÇÃO" if st.session_state.edit_index is not None else "➕ ADICIONAR À FILA"
        st.markdown(f"<h4 style='color:#3b82f6; margin-top:0; font-size:0.9rem;'>{label_botao.split()[-1]} LOTE</h4>", unsafe_allow_html=True)
        
        # Interface de input usando os estados temporários
        c_id = st.text_input("ID DO LOTE", value=st.session_state.temp_id, key="input_id")
        c_meta = st.number_input("PESO TOTAL (KG)", value=st.session_state.temp_meta, key="input_meta", step=1)
        c_qtd = st.number_input("QTD ROLOS (OPCIONAL)", value=st.session_state.temp_qtd, key="input_qtd", step=1)
        
        if st.button(label_botao):
            if c_id and c_meta > 0:
                novo = {"id": c_id, "meta": int(c_meta), "qtd": int(c_qtd)}
                if st.session_state.edit_index is not None:
                    st.session_state.lista_lotes[st.session_state.edit_index] = novo
                    st.session_state.edit_index = None
                else:
                    st.session_state.lista_lotes.append(novo)
                
                # RESET DOS CAMPOS
                st.session_state.temp_id = ""
                st.session_state.temp_meta = 0
                st.session_state.temp_qtd = 0
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:#3b82f6; margin-top:0; font-size:0.9rem;'>PROCESSAR</h4>", unsafe_allow_html=True)
        estoque_txt = st.text_area("PESOS DOS ROLOS", value=st.session_state.input_pesos, height=120)
        
        if st.button("▶ INICIAR"):
            if st.session_state.lista_lotes and estoque_txt:
                try:
                    # Tratamento para INTEIROS (substitui vírgula por espaço para aceitar múltiplos formatos)
                    limpo = estoque_txt.replace('\n', ' ').replace(',', ' ')
                    estoque = [int(x.strip()) for x in limpo.split() if x.strip()]
                    temp_estoque, resultados = estoque.copy(), []
                    
                    for lote in st.session_state.lista_lotes:
                        enc = encontrar_combinacao(temp_estoque, lote['meta'], lote['qtd'])
                        if enc:
                            for p in enc: temp_estoque.remove(p)
                            resultados.append({"id": lote['id'], "meta": lote['meta'], "rolos": enc, "qtd_encontrada": len(enc), "status": "✅"})
                        else:
                            resultados.append({"id": lote['id'], "meta": lote['meta'], "rolos": None, "status": "❌"})
                    
                    st.session_state.historico_operacoes.insert(0, {
                        "hora": pd.Timestamp.now().strftime("%H:%M:%S"),
                        "entrada_original": estoque_txt,
                        "detalhes": resultados,
                        "sobra": temp_estoque
                    })
                    st.session_state.resultados_atuais = resultados
                    st.session_state.lista_lotes = []
                    st.session_state.input_pesos = ""
                    st.rerun()
                except ValueError:
                    st.error("Erro nos pesos: Verifique se há letras ou símbolos inválidos.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_lista:
        st.markdown("<h4 style='color:#94a3b8; font-size:0.9rem;'>FILA:</h4>", unsafe_allow_html=True)
        for i, l in enumerate(st.session_state.lista_lotes):
            c_info, c_ed, c_de = st.columns([3, 0.5, 0.5])
            c_info.markdown(f'<div class="lote-item"><b>{l["id"]}</b> | {l["meta"]}kg</div>', unsafe_allow_html=True)
            if c_ed.button("✏️", key=f"e_{i}"):
                st.session_state.edit_index = i
                st.session_state.temp_id = l['id']
                st.session_state.temp_meta = l['meta']
                st.session_state.temp_qtd = l['qtd']
                st.rerun()
            if c_de.button("🗑️", key=f"d_{i}"):
                st.session_state.lista_lotes.pop(i)
                st.rerun()
        
        if st.session_state.resultados_atuais:
            st.markdown("<h4 style='color:#3b82f6; font-size:0.9rem; margin-top:20px;'>RESULTADO:</h4>", unsafe_allow_html=True)
            for r in st.session_state.resultados_atuais:
                if r['status'] == "✅":
                    rolos_kg = [f"{p}kg" for p in r['rolos']]
                    st.markdown(f"""
                        <div class="resultado-balao">
                            <b>✅ Lote: {r["id"]}</b> ({r['qtd_encontrada']} rolos)<br>
                            <small>{rolos_kg}</small>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="resultado-balao-falha">
                            <b>❌ Lote: {r["id"]}</b><br>
                            <small>Não encontrado. Falta atender {r["meta"]}kg</small>
                        </div>""", unsafe_allow_html=True)

with tab_hist:
    for idx, op in enumerate(st.session_state.historico_operacoes):
        st.markdown('<div class="hist-item">', unsafe_allow_html=True)
        c_h, c_act = st.columns([8, 2])
        c_h.write(f"**Carga {op['hora']}**")
        if c_act.button("🔄 REPLICAR", key=f"rep_{idx}"):
            st.session_state.lista_lotes = []
            for d in op['detalhes']:
                st.session_state.lista_lotes.append({"id": d['id'], "meta": d['meta'], "qtd": 0})
            st.session_state.input_pesos = op['entrada_original']
            st.rerun()
        for d in op['detalhes']:
            if d['rolos']:
                rolos_kg = [f"{p}kg" for p in d['rolos']]
                st.write(f"{d['status']} {d['id']} ({d['qtd_encontrada']} rolos): {rolos_kg}")
            else:
                st.write(f"{d['status']} {d['id']}: Falhou")
        st.markdown(f"<small style='color:#64748b'>Sobra: {op['sobra']}</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #475569; font-size: 0.7rem; margin-top: 40px;'>© 2026 SomaAço. Desenvolvido por Laureano Romagnole 38.</p>", unsafe_allow_html=True)
