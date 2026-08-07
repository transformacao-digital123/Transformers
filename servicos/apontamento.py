from openpyxl import load_workbook
from datetime import datetime
import os

def agrupar_por_operador(ordens):

    grupos = {}

    for ordem in ordens:
        operador = ordem["operador"]

        if operador not in grupos:
            grupos[operador] = []

        grupos[operador].append(ordem)

    return grupos

def selecionar_apontamento(turno, operador,ordens_operador):

    if turno == "Manhã":
        caminho_modelo = "modelos/apontamneto_manha.xlsx"
    elif turno == "Noite":
        caminho_modelo = "modelos/apontamento_noite.xlsx"
    else:
        raise Exception(f"{turno} é um turno inválido   ")

    return preencher_apontamento(caminho_modelo, operador, ordens_operador)

def preencher_apontamento(caminho_modelo,operador,ordens_operador):

    planilha = load_workbook(caminho_modelo)

    aba = planilha.active

    primeira_ordem = ordens_operador[0]

    linha = 4

    aba["L2"] = primeira_ordem["data"]
    aba["M2"] = primeira_ordem["operador"]
    aba["O2"] = primeira_ordem["maquina"]

    for ordem in ordens_operador:
        aba[f"A{linha}"] = ordem["numero_pedido"]
        aba[f"B{linha}"] = ordem["odp"]

        print(f"C{linha}")
        aba[f"C{linha}"] = ordem["cliente"]

        print(f"D{linha}")
        aba[f"E{linha}"] = ordem["padrao"]

        linha += 1

    apontamento_arquivo = f"Apontamento_{operador}.xlsx"

    caminho = os.path.join("temporario", apontamento_arquivo)

    planilha.save(caminho)

    planilha.close()

    return caminho