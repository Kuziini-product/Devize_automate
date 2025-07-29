from openai import OpenAI
import pandas as pd

# Creează clientul OpenAI (cheia API este preluată automat din variabila OPENAI_API_KEY)
client = OpenAI()

def genereaza_deviz_AI(descriere, dimensiuni, baza_date_df):
    tabel_text = baza_date_df.to_csv(index=False)

    prompt = f"""
Avem următoarea bază de date cu materiale și prețuri:

{tabel_text}

Accesorii obligatorii:
  - Minim 4 balamale Blum (2 uși) sau mai multe, în funcție de înălțime (1 balama/350 mm per ușă)
  - Minifixuri HFL pentru asamblare
  - 4 picioare reglabile HFL
  - 2 mânere standard
  - Suporturi raft HFL (4 per raft)
  - Șuruburi și dibluri incluse

Generează un deviz tabelar Markdown cu: Nume | Cantitate | UM | Preț unitar | Total

Descriere:
Dimensiuni: {dimensiuni}
{descriere}
"""

    chat_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    raspuns = chat_response.choices[0].message.content

    linii = [linie for linie in raspuns.split("\n") if "|" in linie]
    curat = [[col.strip() for col in linie.split("|")] for linie in linii]
    df_deviz = pd.DataFrame(curat[1:], columns=curat[0]) if len(curat) > 1 else pd.DataFrame()

    return raspuns, df_deviz
