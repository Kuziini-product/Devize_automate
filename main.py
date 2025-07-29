import streamlit as st
import pandas as pd
import base64
from pathlib import Path
from PIL import Image
from ai_generator import genereaza_deviz_AI
from image_utils import extrage_dimensiuni_din_imagine
from deviz_exporter import export_excel_pdf, lista_oferte_istoric
import os

# Setări generale
st.set_page_config(page_title="Kuziini | Configurator Devize", layout="centered")

# Logo Kuziini sau fallback text
logo_path = Path("assets/Kuziini_logo_negru.png")
if logo_path.exists():
    st.image(str(logo_path), width=300)
else:
    st.markdown("### 🪑 Kuziini | Configurator Devize")

# Titlu aplicație
st.markdown("## Configurator Devize pentru Corpuri de Mobilier")

# 1. Încărcare imagine (schiță)
st.markdown("### 1. Încarcă o poză cu corpul de mobilier (opțional)")
poza = st.file_uploader("Poză cu schiță (jpg/png)", type=["jpg", "png"])
dimensiuni_auto = ""
if poza:
    dimensiuni_auto = extrage_dimensiuni_din_imagine(poza)
    st.success(f"Dimensiuni extrase: {dimensiuni_auto}")

# 2. Dimensiuni + descriere
st.markdown("### 2. Introdu dimensiuni și descriere")
dimensiuni = st.text_input("Dimensiuni (ex: 800x400x2000)", value=dimensiuni_auto or "")
descriere = st.text_area("Descriere corp mobilier", height=150)

# 3. Baza de date automată din fișier
st.markdown("### 3. Baza de date Kuziini (preluată automat din Accesorii.csv)")
try:
    df = pd.read_csv("Accesorii.csv", encoding="latin1")  # poți încerca și utf-8
    st.success("Baza de date a fost încărcată cu succes.")
except Exception as e:
    st.error(f"Eroare la citirea fișierului Accesorii.csv: {e}")
    st.stop()

# Buton generare deviz
if st.button("🔧 Generează deviz"):
    if not descriere or not dimensiuni:
        st.warning("Te rugăm să introduci descrierea și dimensiunile.")
    else:
        raspuns, deviz_df = genereaza_deviz_AI(descriere, dimensiuni, df)
        st.markdown("### 🔍 Deviz generat")
        st.markdown(raspuns)

        nume_fisier = export_excel_pdf(deviz_df, descriere)
        st.success(f"Fișier salvat: {nume_fisier}")

        with open(nume_fisier, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(nume_fisier)}">📥 Descarcă fișierul</a>'
            st.markdown(href, unsafe_allow_html=True)

# 4. Istoric devize
st.markdown("### 📂 Istoric oferte generate")
fisiere_istoric = lista_oferte_istoric()
if fisiere_istoric:
    selectat = st.selectbox("Alege un fișier PDF existent", fisiere_istoric)
    cale_fisier = os.path.join("output/istoric/", selectat)
    with open(cale_fisier, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{selectat}">📥 Descarcă {selectat}</a>'
        st.markdown(href, unsafe_allow_html=True)
else:
    st.info("Nu există oferte salvate încă.")
