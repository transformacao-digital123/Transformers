from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
import os

from servicos.entradas.armazenamento import pasta_arquivos

ALINHAMENTO_PADRAO = Alignment(horizontal="center", vertical="center",wrap_text=True)

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
        caminho_modelo = "modelos/apontamento_manha.xlsx"
    elif turno == "Noite":
        caminho_modelo = "modelos/apontamento_noite.xlsx"
    else:
        raise Exception(f"{turno} é um turno inválido   ")

    return preencher_apontamento(caminho_modelo, operador, ordens_operador)

def preencher_apontamento(caminho_modelo,operador,ordens_operador):

    apontamento_arquivo = f"Apontamento_{operador}.xlsx"

    caminho = os.path.join(pasta_arquivos(), apontamento_arquivo)

    if os.path.exists(caminho):
        planilha = load_workbook(caminho)
    else:
        planilha = load_workbook(caminho_modelo)

    aba = planilha.active

    primeira_ordem = ordens_operador[0]

    linha = 4

# Aqui fará a verificação, enquanto um dos requisitos for verdadeiro ele acrescentará uma linha até encontrar, caso esteja no modo de acrescentar OdP, a linha onde pôr as novas, que no caso será caso os 2 requisitos sejam falsos, em que as 2 linhas estarão vazia
# Agora se houver 2 linhas seguidas vazias, como dito antes, começará a partir daí a acrescentar as novas OdP, e se não estiver no modo acrescentar irá direto a acrescentar direto desde a linha 4 
    while (aba.cell(row = linha, column = 2).value is not None
           or aba.cell(row = linha + 1, column = 2).value is not None):
        linha += 1

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

    print(ordem["operador"])

    planilha.save(caminho)

    planilha.close()

    return caminho


# Como funciona o Apontamento

# app.py
#   │
#   │ converter_google_sheets(link)
#   ▼
# google_sheet.py
#   │
#   ├── validar_link()
#   │
#   ├── baixar_planilha()
#   │
#   ├── abrir_planilha()
#   │
#   ├── identificar_blocos()
#   │       │
#   │       └── retorna → ordens
#   │
#   ├── selecionar_interpretador()
#   │       │
#   │       └── retorna informações interpretadas
#   │
#   ├── preencher_planilha()
#   │       │
#   │       └── cria arquivo de rastreabilidade
#   │
#   ├── agrupar_por_operador(ordens)
#   │       │
#   │       └── retorna → grupos
#   │
#   └── para cada grupo:
#           │
#           ▼
#     selecionar_apontamento()
#           │
#           ├── verifica turno
#           │
#           ├── escolhe modelo
#           │
#           │   ├── Manhã → apontamento_manha.xlsx
#           │   └── Noite → apontamento_noite.xlsx
#           │
#           ▼
#     preencher_apontamento()
#           │
#           ├── load_workbook()
#           │
#           ├── pega aba
#           │
#           ├── pega primeira ordem
#           │
#           ├── preenche data
#           ├── preenche operador
#           ├── preenche máquina
#           │
#           ├── for ordem in ordens_operador
#           │       │
#           │       ├── número pedido
#           │       ├── ODP
#           │       ├── cliente
#           │       └── padrão
#           │
#           ├── planilha.save()
#           │
#           └── retorna nome do arquivo
#           │
#           ▼
#     arquivos.append(arquivo)
#           │
#           ▼
#     criar_zip(arquivos)
#           │
#           ▼
#     retorna arquivo_zip
#           │
#           ▼
#     app.py
#           │
#           ▼
#     send_file(arquivo_saida)
#           │
#           ▼
#     USUÁRIO RECEBE O ZIP