import streamlit as st
import pandas as pd
import os
import plotly.express as px
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="AgroSmart RB House", layout="wide", initial_sidebar_state="expanded")

# --- CONFIGURATION EMAIL ---
EMAIL_EXPEDITEUR = "ton_adresse_gmail@gmail.com"
EMAIL_RECEPTEUR = "ton_adresse_gmail@gmail.com"
MOT_DE_PASSE_APP = "kwmt hcfr yukn mitv"

def envoyer_alerte_email(donnees):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_EXPEDITEUR
        msg['To'] = EMAIL_RECEPTEUR
        msg['Subject'] = f"🌿 Nouveau Relevé : {donnees['Produit']} ({donnees['Prix']} FCFA)"
        corps = f"""
        Bonjour,
        Un nouvel enregistrement vient d'être effectué sur AgroSmart :
        - Produit : {donnees['Produit']} ({donnees['Catégorie']})
        - Prix : {donnees['Prix']} FCFA
        - Unité : {donnees['Unité']}
        - Marché : {donnees['Marché']}
        - Ville : {donnees['Ville']}
        - Date : {donnees['Date']}
        """
        msg.attach(MIMEText(corps, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_EXPEDITEUR, MOT_DE_PASSE_APP)
        server.send_message(msg)
        server.quit()
        return True
    except Exception:
        return False

# --- INITIALISATION ---
if 'catalogue' not in st.session_state:
    st.session_state.catalogue = {
        "Vivres frais": ["Tomate", "Oignon", "Carotte", "Piment", "Chou", "Poivron", "Ail"],
        "Épicerie": ["Sel", "Sucre", "Huile de palme", "Huile raffinée", "Farine", "Cube Maggi"],
        "Conserves": ["Sardine", "Tomate concentrée", "Petit pois", "Maïs doux"],
        "Boissons": ["Eau minérale", "Jus de fruits", "Soda", "Bière", "Vin", "Lait"],
        "Viandes": ["Bœuf", "Poulet", "Porc", "Chèvre", "Mouton"],
        "Poissons": ["Bar", "Maquereau", "Capitaine", "Kanga", "Poisson fumé"],
        "Céréales": ["Riz local", "Riz importé", "Maïs blanc", "Sorgho", "Mil"],
        "Tubercules": ["Manioc", "Plantain", "Macabo", "Igname", "Pomme de terre"]
    }

if 'villes' not in st.session_state:
    st.session_state.villes = ["Douala", "Yaoundé", "Bafoussam", "Garoua", "Bamenda", "Kribi"]

# Utilisation de clés simples pour la navigation interne afin d'éviter les bugs d'emojis
if 'menu_option' not in st.session_state:
    st.session_state.menu_option = "dashboard"

# --- DESIGN CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f7f4; color: #1b4332; }
    [data-testid="stSidebar"] { background-color: #2d6a4f; border-right: 2px solid #1b4332; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p { color: #ffffff !important; }
    label p { color: #1b4332 !important; font-weight: bold !important; font-size: 1.1em !important; }
    .stSelectbox div[data-baseweb="select"], .stTextInput input, .stNumberInput input, .stDateInput input {
        background-color: #ffffff !important;
        border: 2px solid #2d6a4f !important;
        border-radius: 8px !important;
        color: #1b4332 !important;
    }
    .metric-card {
        background-color: #ffffff; border-left: 5px solid #52b788; border-radius: 10px;
        padding: 15px; text-align: center; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #1b4332;
    }
    .metric-card h2 { color: #2d6a4f; margin: 5px 0; font-size: 2em; }
    .logo-text { font-family: 'Helvetica', sans-serif; color: #95d5b2; font-weight: bold; font-size: 1.6em; }
    .stButton>button { background-color: #40916c; color: white !important; font-weight: bold; border-radius: 8px; width: 100%; }
    .stButton>button:hover { background-color: #1b4332; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
DB_FILE = "agro_dynamic_data.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Date", "Catégorie", "Produit", "Ville", "Marché", "Prix", "Unité"]).to_csv(DB_FILE, index=False)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('''<div style="display: flex; align-items: center; gap: 10px;"><span style="font-size: 2em;">🌱</span><p class="logo-text" style="margin: 0;">AgroSmart</p></div>''', unsafe_allow_html=True)
    st.markdown('<p style="color:#d8f3dc; font-size:0.8em; margin-top:-5px; padding-left:45px;">Powered by RB house</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("📈 Tableau de bord"):
        st.session_state.menu_option = "dashboard"
        st.rerun()
    if st.button("📥 Collecte"):
        st.session_state.menu_option = "collecte"
        st.rerun()
    if st.button("📑 Rapports"):
        st.session_state.menu_option = "rapports"
        st.rerun()

# Chargement immédiat des données
df = pd.read_csv(DB_FILE)

# --- LOGIQUE DES PAGES ---

if st.session_state.menu_option == "dashboard":
    st.title("📈 Tableau de bord")
    
    # Métriques
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card">Relevés<br><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
    with m2: 
        moyenne = int(df["Prix"].mean()) if not df.empty else 0
        st.markdown(f'<div class="metric-card">Prix Moyen<br><h2>{moyenne}</h2></div>', unsafe_allow_html=True)
    with m3: 
        villes_count = df["Ville"].nunique() if not df.empty else 0
        st.markdown(f'<div class="metric-card">Villes<br><h2>{villes_count}</h2></div>', unsafe_allow_html=True)
    with m4: 
        cat_count = df["Catégorie"].nunique() if not df.empty else 0
        st.markdown(f'<div class="metric-card">Catégories<br><h2>{cat_count}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    if not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.pie(df, names='Catégorie', hole=0.5, title="Volume par catégorie", color_discrete_sequence=px.colors.sequential.Greens_r)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.bar(df, x='Produit', y='Prix', color='Ville', title="Prix par produit et ville", color_discrete_sequence=px.colors.sequential.Emrld)
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("👋 Bienvenue ! Le tableau de bord est vide. Enregistrez votre premier relevé dans l'onglet 'Collecte'.")

elif st.session_state.menu_option == "collecte":
    st.title("📥 Collecte de données")
    col_cat, col_prod = st.columns(2)
    with col_cat: choix_cat = st.selectbox(" Catégorie", list(st.session_state.catalogue.keys()))
    with col_prod: choix_prod = st.selectbox(" Produit", st.session_state.catalogue[choix_cat])

    with st.form("form_collecte"):
        f1, f2, f3 = st.columns(3)
        with f1: choix_ville = st.selectbox(" Ville", st.session_state.villes)
        with f2: marche = st.text_input(" Marché", placeholder="Ex: Mokolo")
        with f3: prix = st.number_input(" Prix (FCFA)", min_value=0, step=100)
        
        u, d = st.columns(2)
        with u: unite = st.selectbox(" Unité", ["Kg", "Litre", "Sac", "Tas", "Unité", "Casier"])
        with d: date_s = st.date_input(" Date", datetime.now())

        if st.form_submit_button("VALIDER L'ENREGISTREMENT"):
            if marche and prix > 0:
                new_row = pd.DataFrame([[date_s, choix_cat, choix_prod, choix_ville, marche, prix, unite]], columns=df.columns)
                new_row.to_csv(DB_FILE, mode='a', header=False, index=False)
                
                # Envoi mail
                envoyer_alerte_email({"Date": date_s, "Catégorie": choix_cat, "Produit": choix_prod, "Ville": choix_ville, "Marché": marche, "Prix": prix, "Unité": unite})
                
                st.success("Données enregistrées !")
                st.balloons()
            else:
                st.error("Veuillez remplir tous les champs.")

elif st.session_state.menu_option == "rapports":
    st.title("📑 Rapports et Historique")
    if not df.empty:
        st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Télécharger le CSV", data=csv, file_name="export_agro.csv", mime="text/csv")
    else:
        st.info("Aucune donnée enregistrée.")