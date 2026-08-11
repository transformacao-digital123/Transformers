import qrcode
from openpyxl.drawing.image import Image
from openpyxl.styles import Font,Alignment
from openpyxl import load_workbook
import os

FONTE_PADRAO = Font(name="Arial", size=11)

ALINHAMENTO_PADRAO = Alignment(horizontal="center",vertical="center",wrap_text=True)

# A ODP é o parâmetro obrigatório
def gerar_qrcode(odp):

# Pegue o conteúdo recebido em odp e transforme-o em uma imagem de QR Code.
        qr = qrcode.make(odp)

        odp_limpo = odp.replace("/","-")

 # Aqui você aproveitou a própria ODP para criar um nome único para a imagem       
        test = f"QR_{odp_limpo}.png"

        caminho = os.path.join("temporario", test)

# Agora a imagem que está na variável qr é realmente gravada no computador
        qr.save(caminho)

# A função não retorna o QR Code em si. Ela retorna o endereço onde a imagem foi salva
        return caminho

def preencher_etiqueta(ordem):

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

# Usa a função Gerar_qrcode para gerar o caminho da imagem PNG do QRcode
        caminho_qr = gerar_qrcode(ordem["odp"])

# Cia uma um objeto que pode ser inserido na planilha
        qr = Image(caminho_qr)

# Define os tamahos 406x240
        qr.height = 200
        qr.width = 200

# Adiciona a imagem começando na célula especificada
        aba.add_image(qr,"B12")

        odp_limpo = ordem["odp"].replace("/","-")

# Camiho da saída do nvo arquivo das etiqueta
        caminho = f"Etiqueta_{odp_limpo}.xlsx"

        caminho_saida = os.path.join("temporario", caminho)

        planilha.save(caminho_saida)

        return caminho_saida
