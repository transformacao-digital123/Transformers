import zipfile
import os

from servicos.conversao.data import agora
from servicos.entradas.armazenamento import pasta_arquivos

tempo = agora().strftime("%d-%m-%Y_%H:%M:%S")

def criar_zip(arquivos):

    nome_zip = f"Rastreabilidades_{tempo}.zip"

    caminho_zip = os.path.join(pasta_arquivos(), nome_zip)

    with zipfile.ZipFile(caminho_zip, "w") as zip:

        for arquivo in arquivos:
            zip.write(arquivo)

    return caminho_zip