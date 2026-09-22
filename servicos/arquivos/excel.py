# OpenPyXL é uma biblioteca especializada em ler e escrever
from openpyxl import load_workbook

def abrir_planilha(caminho_arquivo):
        
# Abre a planilha salva no computador e carrega seu conteúdo para a memória, ou seja, abre a planilha salva no computador         
    planilha = load_workbook(caminho_arquivo)

    return planilha