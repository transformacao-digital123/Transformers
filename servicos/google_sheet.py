# Essa biblioteca é como openpyxl mas mais pesado pois analis a planilha no navegador
import pandas as pd 

def converter_google_sheets(link):
    if "docs.google.com/spreadsheets" not in link:
        raise Exception("O link inserido não é um Google-Sheets")

# Substitui o final do link e o transforma em um arquivo baixável no navegador
    link_csv = link.replace("/edit?", "/export?format=csv&")

# Pega o arquivo no navegador (internet) ao acessá-lo, baixa e cria o dataframe
    df=pd.read_csv(link_csv)

    print(df)

    return link_csv