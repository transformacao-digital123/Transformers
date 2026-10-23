from openpyxl import load_workbook

from servicos.data import agora

def preencher_despacho(caminho_arquivo, nome_aba, linha,cancelar = False):

    planilha = load_workbook(caminho_arquivo)

    try:

        aba = planilha[nome_aba]
        celula = aba[f"E{linha}"]
        despacho_anterior = celula.value

        if cancelar:
            if despacho_anterior:
                celula.value = None

                planilha.save(caminho_arquivo)

                return {
                    "novo": False,
                    "hora_despacho": "",
                    "cancelar": True,
                    "cancelado": True
                }

# Se não houver despacho_anterior então não entrará nesse if pois o resultado será false (não confundir com o resultado do novo ali que fala false) e dará continuidade na função
# Já se houver um resultado em despacho_anterior ele entrará nesse if por ser True e terminará aqui
        if despacho_anterior:

            return {
                "novo": False,
                "hora_despacho": despacho_anterior,
                "cancelado": False
            }
   
        hora_despacho = agora().strftime("%H:%M:%S")

        celula.value = hora_despacho

        planilha.save(caminho_arquivo)

        return {
            "novo": True,
            "hora_despacho": hora_despacho,
            "cancelado": False}

    finally:
        planilha.close()