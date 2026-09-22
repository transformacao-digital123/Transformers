from openpyxl import load_workbook
from openpyxl.styles import Font,Alignment
from openpyxl.drawing.image import Image
import os

from servicos.etiquetas.qrcode import gerar_qrcode

FONTE_PADRAO = Font(name="Arial", size=11)

ALINHAMENTO_PADRAO = Alignment(horizontal="center",vertical="center",wrap_text=True)

def preencher_etiqueta(ordem,rastreabilidade,numero_etiquetas,total_etiquetas):

        identificador = ordem["identificador"]

        dados_identificador = {
                "odp": ordem["odp"],
                "numero_pedido": ordem["numero_pedido"],
                "cliente": ordem["cliente"],
                "operador": ordem["operador"],
                "maquina": ordem["maquina"],
                "turno": ordem["turno"],
                "data": ordem["data"].strftime("%d%m%Y"),
        }

        rastreabilidade[identificador] = dados_identificador

# Carrega a planilha que queremos
        planilha = load_workbook("modelos/Modelo_Etiqueta_Luari.xlsx")

# Abre na 1º aba do arquivo
        aba = planilha.active

        aba["B6"] = ordem["odp"]
        aba["B6"].font = FONTE_PADRAO
        aba["B6"].alignment = ALINHAMENTO_PADRAO

        aba["B7"] = ordem["operador"]
        aba["B7"].font = FONTE_PADRAO
        aba["B7"].alignment = ALINHAMENTO_PADRAO

        aba["B8"] = ordem["maquina"]
        aba["B8"].font = FONTE_PADRAO
        aba["B8"].alignment = ALINHAMENTO_PADRAO

        aba["B9"] = ordem["data"]
        aba["B9"].number_format = "dd/mm/yy"
        aba["B9"].font = FONTE_PADRAO
        aba["B9"].alignment = ALINHAMENTO_PADRAO

# Aqui ele pega e transforma o texto em uma linguagem que o programa do QR code consiga ler,no caso formato de texto, esse comando ensure_ascii= False serve para caso seja escrito uma palavra com ~ ou ç o programa faça o texto ficar normal e não um conjunto de letras estranhas
        texto_qr = identificador

# Usa a função Gerar_qrcode para gerar o caminho da imagem PNG do QRcode. A odp aí é apenas pq a função gerar-qrcode exige esses 2 parâmetros
        caminho_qr = gerar_qrcode(texto_qr,ordem["odp"],ordem["operador"])

# Cria um objeto que pode ser inserido na planilha
        qr = Image(caminho_qr)

# Define os tamanhos 406x240(valores do espaço onde o QR code está inserido)
        qr.height = 240
        qr.width = 240


# Adiciona a imagem começando na célula especificada
        aba.add_image(qr,"B11")

        odp_limpo = ordem["odp"].replace("/","-")

        operario = ordem["operador"]

# Camiho da saída do nvo arquivo das etiqueta
        if total_etiquetas > 1:
                caminho = f"Etiqueta_{odp_limpo}_{operario}_Nº{numero_etiquetas}.xlsx"
        else:
                caminho = f"Etiqueta_{odp_limpo}_{operario}.xlsx"

        caminho_saida = os.path.join("temporario", caminho)

        planilha.save(caminho_saida)

        return caminho_saida