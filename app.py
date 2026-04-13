import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="SomaAço | Industrial", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Visual Industrial (Foco em Dark Mode e Usabilidade)
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #0f172a; color: #f8fafc; }
    
    /* Estilização das Abas */
    .stTabs [data-baseweb="tab-list"] { background-color: #1e293b; border-radius: 8px; padding: 5px; }
    .stTabs [data-baseweb="tab"] { height: 45px; color: #94a3b8 !important; }
    .stTabs [aria-selected="true"] { color: #3b82f6 !important; border-bottom: 2px solid #3b82f6 !important; }

    /* Containers e Inputs */
    .section-card {
        background-color: #1e293b;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    input, textarea { background-color: #020617 !important; border: 1px solid #334155 !important; color: #f1f5f9 !important; }
    
    /* Botão Industrial */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 15px;
        font-weight: 700;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# Ícones Minimalistas (SVG para máxima nitidez)
icon_gear = '⚙️' 
icon_timer = '⏱️'
icon_calc = '<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="1.5"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="16" y1="14" x2="16" y2="14.01"/><line x1="12" y1="14" x2="12" y2="14.01"/><line x1="8" y1="14" x2="8" y2="14.01"/><line x1="8" y1="10" x2="16" y2="10"/></svg>'

# --- HEADER ---
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 15px; margin-bottom: 25px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background-color
