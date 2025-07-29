
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

ISTORIC_FOLDER = "output/istoric/"
os.makedirs(ISTORIC_FOLDER, exist_ok=True)

def get_next_offer_number():
    existente = [f for f in os.listdir(ISTORIC_FOLDER) if f.startswith("OF-") and f.endswith(".pdf")]
    numere = [int(f.split("-")[1]) for f in existente if f.split("-")[1].isdigit()]
    return max(numere + [0]) + 1 if numere else 1

def export_excel_pdf(df, descriere):
    nr_oferta = get_next_offer_number()
    client = "Client"
    nume_fisier_base = f"OF-2025-{str(nr_oferta).zfill(4)}_{client}"

    # Export Excel
    excel_path = os.path.join(ISTORIC_FOLDER, f"{nume_fisier_base}.xlsx")
    df.to_excel(excel_path, index=False)

    # Export PDF
    pdf_path = os.path.join(ISTORIC_FOLDER, f"{nume_fisier_base}.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Kuziini | Ofertă mobilier", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, descriere)
    pdf.ln(5)
    col_widths = [50, 25, 20, 30, 30]

    for i, col in enumerate(df.columns):
        pdf.cell(col_widths[i], 10, col, 1)
    pdf.ln()
    for _, row in df.iterrows():
        for i, val in enumerate(row):
            pdf.cell(col_widths[i], 10, str(val), 1)
        pdf.ln()

    pdf.output(pdf_path)
    return pdf_path

def lista_oferte_istoric():
    return sorted([f for f in os.listdir(ISTORIC_FOLDER) if f.endswith(".pdf")])
