import zipfile

from servicos.data import agora

tempo = agora().strftime("%d%m%Y_%H%M%S")

def criar_zip(arquivos):

    nome_zip = f"Rastreabilidades_{tempo}.zip"

    with zipfile.ZipFile(nome_zip, "w") as zip:

        for arquivo in arquivos:
            zip.write(arquivo)

    return nome_zip