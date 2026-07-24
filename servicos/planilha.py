from openpyxl import load_workbook
from datetime import datetime
from openpyxl.styles import Font, Alignment

CELULAS = {
    "data": "B3",
    "numero_pedido": "B4",
    "cliente": "B6",
    "padrao": "B7",
    "filme": "B8",
    "peso_tubete": "B10",
    "observacoes": "B20"
}

FONTE_PADRAO = Font(name="Aptos Narrow",
        size=24)


FONTES = {
    "data": FONTE_PADRAO,
    "numero_pedido": FONTE_PADRAO,
    "cliente": FONTE_PADRAO,
    "padrao": FONTE_PADRAO,
    "filme": FONTE_PADRAO,
    "peso_tubete": FONTE_PADRAO
}

ALINHAMENTOS_PADRAO = Alignment(horizontal="center", vertical= "center")

ALINHAMENTOS = {
    "data": ALINHAMENTOS_PADRAO,
    "numero_pedido": ALINHAMENTOS_PADRAO,
    "cliente": ALINHAMENTOS_PADRAO,
    "padrao": ALINHAMENTOS_PADRAO,
    "filme": ALINHAMENTOS_PADRAO,
    "peso_tubete": ALINHAMENTOS_PADRAO,
}

# aplicação do Excel para abrir a planilha
def preencher_planilha(dados):

# Carrega o arquivo Excel anexado no programa dentro do sistema
    planilha = load_workbook("modelos/modelo.xlsx")

# Permite acessar a primeira página do arquivo Excel (Eu acho)
    aba = planilha.active

# Comando de repetição para que não precise toda vez acrescentar uma linha nova na função preencher_planilha toda vez que uma nova variável for acrescentada como essa, por exemplo: aba[CELULAS["cliente"]] = dados["cliente"] ,(que é a mesma coisa que) == aba[CELULAS["B6"]] = dados["FBR EMBALAGENS LTDA"]
# Ele funciona assim, o itens,  vai separar cada linha em 2 valores, ex: ("data", "20/07/2026"), para preencher a variável chave e valor respectivamente, já procurando os valores de uma vez, ao invés de ficar toda vez analisando o dicionário inteiro para encontrar a resposta
    for chave, valor in dados.items():
        celula = aba[CELULAS[chave]] # ou aba[CELULAS[chave]] = valor
        celula.value = valor 

        if chave in FONTES:
            celula.font = FONTES[chave]

        if chave in ALINHAMENTOS:
            celula.alignment = ALINHAMENTOS[chave]

# Comando para nomear a data e hora no arquivo
    nome = datetime.now().strftime("%d%m%Y_%H%M%S")

    arquivo = f"resultado_{nome}.xlsx"
    planilha.save(arquivo)

    return arquivo