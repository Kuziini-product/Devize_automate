
import openai
import pandas as pd
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # asigură-te că ai cheia în variabilă de mediu

def genereaza_deviz_AI(descriere, dimensiuni, baza_date_df):
    # Convertim CSV în text brut
    tabel_text = baza_date_df.to_csv(index=False)

    prompt = f"""
Avem următoarea bază de date cu materiale și prețuri:

{tabel_text}

Accesorii obligatorii:
  - Minim 4 balamale Blum (2 uși) sau mai multe, în funcție de înălțime (1 balama/350 mm per ușă)
  - Minifixuri HFL pentru asamblare (calculat pe colțuri și rafturi)
  - 4 picioare reglabile HFL
  - 2 mânere standard
  - Suporturi raft HFL (4 per raft)
  - Șuruburi și dibluri standard incluse

Pe baza acestei baze de date, generează un deviz complet în format tabelar Markdown cu coloanele:
Nume | Cantitate | UM | Preț unitar | Total

Descriere mobilier:
Dimensiuni: {dimensiuni}
{descriere}
"""

    raspuns = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )["choices"][0]["message"]["content"]

    # Convertim răspunsul în DataFrame
    linii = [linie for linie in raspuns.split("\n") if "|" in linie]
    curat = [[col.strip() for col in linie.split("|")] for linie in linii]
    if len(curat) > 1:
        header = curat[0]
        valori = curat[1:]
        df_deviz = pd.DataFrame(valori, columns=header)
    else:
        df_deviz = pd.DataFrame()

    return raspuns, df_deviz
