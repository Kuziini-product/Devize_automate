import streamlit as st
import pandas as pd
import base64
from PIL import Image
from ai_generator import genereaza_deviz_AI
from image_utils import extrage_dimensiuni_din_imagine
from deviz_exporter import export_excel_pdf, lista_oferte_istoric
import os

# Logo + titlu
st.set_page_config(page_title="Kuziini | Configurator Devize", layout="centered")
st.image("assets/Kuziini_logo_negru.png", width=300)
st.markdown("## Configurator Devize pentru Corpuri de Mobilier")

# Încărcare imagine (schiță)
st.markdown("### 1. Încarcă o poză cu corpul de mobilier (opțional)")
poza = st.file_uploader("Poză cu schiță (jpg/png)", type=["jpg", "png"])
dimensiuni_auto = ""
if poza:
    dimensiuni_auto = extrage_dimensiuni_din_imagine(poza)
    st.success(f"Dimensiuni extrase: {dimensiuni_auto}")

# Introducere manuală dimensiuni & descriere
st.markdown("### 2. Introdu dimensiuni și descriere")
dimensiuni = st.text_input("Dimensiuni (ex: 800x400x2000)", value=dimensiuni_auto or "")
descriere = st.text_area("Descriere corp mobilier", height=150)

# Încărcare fișier bază date accesorii
st.markdown("### 3. Încarcă baza de date Kuziini")
baza_date = st.file_uploader("Accesorii.csv", type="csv")

# Buton generare deviz
if st.button("🔧 Generează deviz"):
    if not descriere or not dimensiuni:
        st.warning("Te rugăm să introduci descrierea și dimensiunile.")
    elif not baza_date:
        st.warning("Încarcă fișierul Accesorii.csv.")
    else:
        df = pd.read_csv(baza_date)
        raspuns, deviz_df = genereaza_deviz_AI(descriere, dimensiuni, df)

        st.markdown("### 🔍 Deviz generat")
        st.markdown(raspuns)

        # Salvare deviz în output
        nume_fisier = export_excel_pdf(deviz_df, descriere)
        st.success(f"Fișier salvat: {nume_fisier}")

        # Link descărcare
        with open(nume_fisier, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(nume_fisier)}">📥 Descarcă fișierul</a>'
            st.markdown(href, unsafe_allow_html=True)

# Istoric oferte
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
