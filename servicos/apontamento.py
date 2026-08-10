from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from datetime import datetime
import os

ALINHAMENTO_PADRAO = Alignment(horizontal="center", vertical="center")

FONTE_PADRAO = Font(name="Arial", size=11)



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

    aba["M2"] = primeira_ordem["data"]
    aba["M2"].number_format = "dd/mm/yyyy"
    aba["M2"].font = FONTE_PADRAO
    aba["M2"].alignment = ALINHAMENTO_PADRAO

    aba["O2"] = primeira_ordem["operador"]
    aba["O2"].font = FONTE_PADRAO
    aba["O2"].alignment = ALINHAMENTO_PADRAO

    aba["Q2"] = primeira_ordem["maquina"]
    aba["Q2"].font = FONTE_PADRAO
    aba["Q2"].alignment = ALINHAMENTO_PADRAO

    for ordem in ordens_operador:
        aba[f"A{linha}"] = ordem["numero_pedido"]
        aba[f"B{linha}"] = ordem["odp"]
        aba[f"C{linha}"] = ordem["cliente"]
        aba[f"E{linha}"] = ordem["padrao"]

        aba[f"A{linha}"].font = FONTE_PADRAO
        aba[f"B{linha}"].font = FONTE_PADRAO
        aba[f"C{linha}"].font = FONTE_PADRAO
        aba[f"E{linha}"].font = FONTE_PADRAO

        aba[f"A{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"B{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"C{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"E{linha}"].alignment = ALINHAMENTO_PADRAO

        linha += 1

    apontamento_arquivo = f"Apontamento_{operador}.xlsx"

    caminho = os.path.join("temporario", apontamento_arquivo)

    planilha.save(caminho)

    planilha.close()

    return caminho