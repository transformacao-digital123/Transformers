from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment

ALINHAMENTO_PADRAO = Alignment(horizontal="center", vertical="center",wrap_text=True)

FONTE_PADRAO = Font(name="Arial", size=11)

def encontrar_proxima_linha(aba):

    linha = 6

# Enquanto linha for mnor que a última linha preenchida ele continuaá analisano
    while linha < aba.max_row:

        linha_atual_vazia = aba[f"D{linha}"].value is None
        proxima_linha_vazia = aba[f"D{linha + 1}"].value is None

# Aqui é uma verificação, se a linha da odp e a linha seguinte estiverem vazias ele retorna o valor em que a linha parou + 1 para devolve o valor a quem o chamou da linha que irá começr a colocar a nova remessa, no caso será depois da última linha que tinha conteúdo e depois da linha seguinte dele que era uma linha espaço
# Caso contrário ele apenas adiciona + 1 ao Nº da linha e continua sua análise de linha em linha
        if linha_atual_vazia and proxima_linha_vazia:
            return linha + 1

        linha += 1

# Se caso ele tiver rodado a planilha inteira e não tiver encontrado uma sequência de 2 linhas seguidas vazias ele retornará para quem o chamou aba.max_row + 1 que significa que ele visualizou todas as linhas preenchidas + 1 que sempre tem o espaçamento de 1 linha em branco
    return aba.max_row + 1

def acrecentar_odps_por_remessa(caminho_remessa,ordens):

    planilha = load_workbook(caminho_remessa)

    aba = planilha.active

    linha = encontrar_proxima_linha(aba)

    for ordem in ordens:

        aba[f"C{linha}"] = ordem["numero_pedido"]
        aba[f"D{linha}"] = ordem["odp"]

# Despachamento
        aba[f"E{linha}"] = ""

# Valores que serão preenchidos na pesagem
        aba[f"F{linha}"] = ""
        aba[f"G{linha}"] = ""
        aba[f"H{linha}"] = ""
        aba[f"I{linha}"] = ""
        aba[f"J{linha}"] = ""

        aba[f"K{linha}"] = ordem["cliente"]
        aba[f"L{linha}"] = ordem["padrao"]
        aba[f"M{linha}"] = ordem["filme"]
        aba[f"N{linha}"] = ordem["peso_tubete"]
        aba[f"O{linha}"] = ordem.get("observacao","")
        aba[f"P{linha}"] = ordem["operador"]
        aba[f"Q{linha}"] = ordem["maquina"]

# Dados de rastreabilidade, para serem registrados no histórico
        aba[f"R{linha}"] = ""
        aba[f"S{linha}"] = ""
        aba[f"T{linha}"] = ""
        aba[f"U{linha}"] = ordem["identificador"]
        aba[f"V{linha}"] = ""
        aba[f"W{linha}"] = ""
        aba[f"X{linha}"] = ""

# Essas letras todas são todas as colunas que tem informação na nossa tabela na qual aplicaremos alguma mudança
        for coluna in "CDEFGHIJKLMNOPQRSTUVW":

            aba[f"{coluna}{linha}"].font = FONTE_PADRAO
            aba[f"{coluna}{linha}"].alignment = ALINHAMENTO_PADRAO

# OBS em vermelho
        aba[f"O{linha}"].font = Font(name="Arial", size=11, color="FF0000", bold=True)

        linha += 2

        planilha.save(caminho_remessa)
        planilha.close()

        return caminho_remessa