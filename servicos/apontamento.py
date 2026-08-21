from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
import os
from openpyxl.drawing.image import Image
from datetime import datetime

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
        if aba[f"D{linha}"].value == odp:
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

    primeira_ordem = ordens_operador[0]

    caminho_saida = f"temporario/ODP_{primeira_ordem['operador']}.xlsx"

    if os.path.exists(caminho_saida):
        planilha = load_workbook(caminho_saida)
    else:
        planilha = load_workbook("modelos/OdP's de cada funcionário.xlsx")

# Se a aba historico já existir na planilha ela é guardada na variável historico para ser usada mais pra frente
    if "historico" in planilha.sheetnames:
        historico = planilha["historico"]
    else:

# Se não tiver, procra por historico_modelo, que é o nome da aba no arquivo principal
# Historico_modelo guarda na variavel historico modelo pra ser usado mais pra frente
# Faz uma cópia da planilha da aba do historico_modelo na em historico
# O títuloda aba dessa planilha será historico
# Depois disso a planilha historico_modelo será apagada e o loop não passará mais por aqui porque a aba historico já existirá no arquivo
        if "historico_modelo" in planilha.sheetnames:
            historico_modelo = planilha["historico_modelo"]
            historico = planilha.copy_worksheet(historico_modelo)
            historico.title = "historico"
            planilha.remove(historico_modelo)

 # caso nenhuma das 2 abas forem achada ele cria uma aba vazia com o nome historico afim de evitar dar erro 
        else:
            historico = planilha.create_chartsheet(title="historico")

    data = primeira_ordem["data"].strftime("%d-%m-%Y")
    nome_aba = f"{data}_{primeira_ordem["turno"]}"

# Assim fica especificado pro programa sempre usar de parâmetro a aba com o nome "Modelo"
    aba_modelo = planilha["Modelo"]

    if nome_aba in planilha.sheetnames:
        aba = planilha[nome_aba]
    else:
        aba = planilha.copy_worksheet(aba_modelo)
        aba.title = nome_aba

        logo = Image("imagens/luari_logo_empresa.png")
        logo.width = 150
        logo.height = 60

        aba.add_image(logo, "B2")

    aba["D3"] = primeira_ordem["operador"]
    aba["D3"].font = FONTE_PADRAO
    aba["D3"].alignment = ALINHAMENTO_PADRAO

    aba["F3"] = primeira_ordem["maquina"]
    aba["F3"].font = FONTE_PADRAO
    aba["F3"].alignment = ALINHAMENTO_PADRAO

    aba["K3"] = primeira_ordem["data"]
    aba["K3"].number_format = "dd/mm/yyyy"
    aba["K3"].font = FONTE_PADRAO
    aba["K3"].alignment = ALINHAMENTO_PADRAO

    aba["M3"] = primeira_ordem["turno"]
    aba["M3"].font = FONTE_PADRAO
    aba["M3"].alignment = ALINHAMENTO_PADRAO

    linha = 6

    for ordem in ordens_operador:

        aba[f"C{linha}"] = ordem["numero_pedido"]
        aba[f"D{linha}"] = ordem["odp"]
        aba[f"J{linha}"] = ordem["cliente"]
        aba[f"K{linha}"] = ordem["padrao"]
        aba[f"L{linha}"] = ordem["filme"]
        aba[f"M{linha}"] = ordem["peso_tubete"]
        aba[f"N{linha}"] = ordem.get("observacao", "")

        aba[f"C{linha}"].font = FONTE_PADRAO
        aba[f"D{linha}"].font = FONTE_PADRAO
        aba[f"E{linha}"].font = FONTE_PADRAO
        aba[f"F{linha}"].font = FONTE_PADRAO
        aba[f"G{linha}"].font = FONTE_PADRAO
        aba[f"H{linha}"].font = FONTE_PADRAO
        aba[f"I{linha}"].font = FONTE_PADRAO
        aba[f"J{linha}"].font = FONTE_PADRAO
        aba[f"K{linha}"].font = FONTE_PADRAO
        aba[f"L{linha}"].font = FONTE_PADRAO
        aba[f"M{linha}"].font = FONTE_PADRAO
        aba[f"N{linha}"].font = Font(name="Arial", size=11, color="FF0000", bold=True)
        
        aba[f"C{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"D{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"E{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"F{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"G{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"H{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"I{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"J{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"K{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"L{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"M{linha}"].alignment = ALINHAMENTO_PADRAO
        aba[f"N{linha}"].alignment = ALINHAMENTO_PADRAO

        linha += 2  

    planilha.save(caminho_saida)
    planilha.close()

    print("SALVANDO O ARQUIVO:", os.path.abspath(caminho_saida))
    return caminho_saida

def atualizar_odp(caminho_arquivo,nome_aba,linha,identificador,dados):
    planilha = load_workbook(caminho_arquivo)

    aba = planilha[nome_aba]

    historico = planilha["historico"]

    campos = {
        "numero_pallet": 'E',
        "peso_liquido": "F",
        "peso_total": "G",
        "op_material": "H",
        "op_tubete": "I"
    }

    linha_histotico = historico.max_row + 1

    houve_alteracao = False

# Item faz uma lista onde campo é a chave e coluna valor
    for campo,coluna in campos.items():

# O .get() irá procurar se algum dos valores de campo está dados, se não tiver retornará None
        novo_valor = dados.get(campo)

# Se o operador não preencheu o campo ou deixou em branco, não altera nada, ele continua
        if novo_valor in (None,""):
            continue
# Acessa a célula exata da aba principal e lê o cionteúdo del através do .value()
        valor_anterior = aba[f"{coluna}{linha}"].value 

# Se os valores forem iguais o sistema continua, isso evita que o programa gaste processamento alterando valores iguais e acrescentando linhas de histórico inúteis 
        if str(valor_anterior) == str(novo_valor):
            continue

# Após passar pela filtragem as células da aba principal recebe o novo valor
        aba[f"{coluna}{linha}"] = novo_valor
        houve_alteracao = True

        agora = datetime.now()

        historico[f"C{linha_histotico}"] = agora.strftime("%d%m%Y")
        historico[f"D{linha_histotico}"] = agora.strftime("%H:%M:%S")
        historico[f"E{linha_histotico}"] = identificador
        historico[f"F{linha_histotico}"] = aba[f"D{linha}"].value
        historico[f"G{linha_histotico}"] = dados.get("acao", "")
        historico[f"H{linha_histotico}"] = valor_anterior
        historico[f"I{linha_histotico}"] = novo_valor

        linha_histotico += 1



    if houve_alteracao:
        planilha.save(caminho_arquivo)

    planilha.close() 

def registrar_historico(caminho_arquivo,identificador,odp,acao,valor_anterior,novo_valor):

    planilha = load_workbook(caminho_arquivo)

# Procura pela aba "historico"
    historico = planilha["historico"]

# Essa linha vizualiza qual a última linha preenchida da tabela +1 pra garantir que comece na linha em branco
    linha = historico.max_row + 1

    agora = datetime.now()

    historico[f"C{linha}"] = agora.strftime("%d%m%Y")
    historico[f"D{linha}"] = agora.strftime("%H:%M:%S")
    historico[f"E{linha}"] = identificador
    historico[f"F{linha}"] = odp
    historico[f"G{linha}"] = acao
    historico[f"H{linha}"] = valor_anterior
    historico[f"I{linha}"] = novo_valor

    planilha.save(caminho_arquivo)
    planilha.close()
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