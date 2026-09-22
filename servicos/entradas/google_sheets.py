# Ela Conversa com servidores na internet, desde: acessar sites;baixar imagens; baixar PDFs; baixar Excel; acessar APIs.
import requests

# Valida de o link é do google docs ou não
def validar_link(link):
    if "docs.google.com/spreadsheets" not in link:
            raise Exception("O link inserido não é um Google-Sheets")

def baixar_planilha(link):

# Substitui o final do link e o transforma em um arquivo baixável no navegador
    link_xlsx = link.replace("/edit?", "/export?format=xlsx&")

# requests.get(...): "Vá até esse endereço e me traga a resposta, um objeto que contém tudo que o servidor respondeu. 
# Enquanto isso o "resposta.content" irá guardar em bytes a informação no computador até ela ser usada"
    resposta = requests.get(link_xlsx)

# Variável para que possamos sempre usar o nome que será retornada, quando quisermos só alterando 1 linha
    caminho_arquivo = "planilha.xlsx"

# Crie (ou abra) um arquivo chamado planilha.xlsx, no modo de escrita binária, e quando eu terminar, feche-o automaticamente.
    with open(caminho_arquivo, "wb") as arquivo:
        arquivo.write(resposta.content)

    return caminho_arquivo