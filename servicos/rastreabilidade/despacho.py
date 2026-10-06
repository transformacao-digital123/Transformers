from datetime import datetime
from openpyxl import load_workbook

def preencher_despacho(caminho_arquivo, nome_aba, linha):

    planilha = load_workbook(caminho_arquivo)

    aba = planilha[nome_aba]

    despacho_anterior = aba[f"E{linha}"].value

# Se não houver despacho_anterior então não entrará nesse if pois o resultado será false (não confundir com o resultado do novo ali que fala false) e dará continuidade na função
# Já se houver um resultado em despacho_anterior ele entrará nesse if por ser True e terminará aqui
    if despacho_anterior:
        planilha.close()

        return {
            "novo": False,
            "hora_despacho": despacho_anterior
        }

    agora = datetime.now()
    hora_despacho = agora.strftime("%H:%M:%S")

    aba[f"E{linha}"] = hora_despacho

    planilha.save(caminho_arquivo)
    planilha.close()

    return {
        "novo": True,
        "hora_despacho": hora_despacho}