from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
import os
from openpyxl.drawing.image import Image

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

def localizar_odp(aba, odp):

# Aqui ele analisará cada linha desde a 1 até o final, mas devido ao python considerar que ele lerá somente até o valor antes do último colocamos o +1
    for linha in range(1, aba.max_row + 1):

# Se o valor da célula for igual a odp retornará linha
        if aba[f"C{linha}"].value == odp:
            return linha

# Se não retornará nada 
    return None

def preencher_expedição(aba,odp,numero_pallet,peso_total,peso_liquido):

    linha = localizar_odp(aba,odp)

    if linha is None:
        print(f"ODP não encontrada: {odp}")
        return False
    
    aba[f'D{linha}'] = numero_pallet
    aba[f'E{linha}'] = peso_total
    aba[f'F{linha}'] = peso_liquido

    print(f"ODP {odp} encontrada na linha {linha}")

    return True

def preencher_odps(ordens_operador):

    planilha = load_workbook("modelos/OdP's de cada funcionário.xlsx")

    primeira_ordem = ordens_operador[0]

    data = primeira_ordem["data"].strftime("%d-%m-%Y")
    nome_aba = f"{data}_{primeira_ordem["turno"]}"

    aba_modelo = planilha.active


    if nome_aba in planilha.sheetnames:
        aba = planilha[nome_aba]
    else:
        aba = planilha.copy_worksheet(aba_modelo)
        aba.title = nome_aba

        logo = Image("imagens/luari_logo_empresa.png")
        logo.width = 150
        logo.height = 60

        aba.add_image(logo, "A2")

    aba["C3"] = primeira_ordem["operador"]
    aba["C3"].font = FONTE_PADRAO
    aba["C3"].alignment = ALINHAMENTO_PADRAO

    aba["E3"] = primeira_ordem["maquina"]
    aba["E3"].font = FONTE_PADRAO
    aba["E3"].alignment = ALINHAMENTO_PADRAO

    aba["H3"] = primeira_ordem["data"]
    aba["H3"].number_format = "dd/mm/yyyy"
    aba["H3"].font = FONTE_PADRAO
    aba["H3"].alignment = ALINHAMENTO_PADRAO

    aba["J3"] = primeira_ordem["turno"]
    aba["J3"].font = FONTE_PADRAO
    aba["J3"].alignment = ALINHAMENTO_PADRAO

    linha = 6

    for ordem in ordens_operador:

        aba[f"B{linha}"] = ordem["numero_pedido"]
        aba[f"C{linha}"] = ordem["odp"]
        aba[f"G{linha}"] = ordem["cliente"]
        aba[f"H{linha}"] = ordem["padrao"]
        aba[f"I{linha}"] = ordem["filme"]
        aba[f"J{linha}"] = ordem["peso_tubete"]
        aba[f"K{linha}"] = ordem.get("observacao", "")

        aba[f"B{linha}"].font = FONTE_PADRAO
        aba[f"C{linha}"].font = FONTE_PADRAO
        aba[f"D{linha}"].font = FONTE_PADRAO
        aba[f"E{linha}"].font = FONTE_PADRAO
        aba[f"F{linha}"].font = FONTE_PADRAO
        aba[f"G{linha}"].font = FONTE_PADRAO
        aba[f"H{linha}"].font = FONTE_PADRAO
        aba[f"I{linha}"].font = FONTE_PADRAO
        aba[f"J{linha}"].font = FONTE_PADRAO
        aba[f"K{linha}"].font = Font(name="Arial", size=11, color="FF0000", bold=True)
        
        aba[f"B{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"C{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"D{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"E{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"F{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"G{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"H{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"I{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"J{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"K{linha}"].alignment = ALINHAMENTO_PADRAO

        linha += 2
        
# Serve para encontrar o título dentro arquivo, assim, sem esses ussents apagaria provavelmente a variável e ficaria sujeito a erro de tipagem devido a limitações do python
    if aba_modelo.title in planilha.sheetnames:
        planilha.remove(aba_modelo)

    caminho_saida = f"temporario/ODP_{primeira_ordem['operador']}.xlsx"

    planilha.save(caminho_saida)
    planilha.close()

    return caminho_saida

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